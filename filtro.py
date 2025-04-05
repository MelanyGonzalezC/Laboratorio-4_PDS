import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, find_peaks, hilbert, windows
import tkinter as tk
from tkinter import ttk, filedialog

# ***** IMPORTACIONES PARA LA PRUEBA DE HIPÓTESIS *****
from scipy.stats import ttest_rel, t, ttest_ind  # t: para obtener valores críticos (ppf)

# Función para cargar datos desde Excel
def cargar_datos_excel(ruta_archivo, columna):
    try:
        df = pd.read_excel(ruta_archivo, engine="openpyxl")
        datos = df[columna].dropna().values
        return datos
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return None

# Filtro pasa altas con Butterworth
def filtro_pasa_altas(datos, fc, fs, orden=2):
    nyquist = 0.5 * fs
    normal_cutoff = fc / nyquist
    b, a = butter(orden, normal_cutoff, btype='high', analog=False)
    return filtfilt(b, a, datos)

# Filtro pasa bajas con Butterworth
def filtro_pasa_bajas(datos, fc, fs, orden=2):
    nyquist = 0.5 * fs
    normal_cutoff = fc / nyquist
    b, a = butter(orden, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, datos)

# Función para detectar contracciones usando Hilbert
def detectar_contracciones_hilbert(envolvente, umbral, fs):
    picos, _ = find_peaks(envolvente, height=umbral)
    return picos

# Función para aplicar ventanas en contracciones detectadas
def aplicar_ventanas(picos, envolvente, fs):
    ventanas = []
    tamano_ventana = int(0.5 * fs)  # 500 ms

    for pico in picos:
        inicio = max(pico - tamano_ventana // 2, 0)
        fin = min(pico + tamano_ventana // 2, len(envolvente))
        ventana = envolvente[inicio:fin] * windows.hamming(fin - inicio)
        ventanas.append((ventana, inicio, fin, pico))

    return ventanas

# Función para mostrar las ventanas detectadas
def mostrar_ventanas(ventanas):
    if not ventanas:
        print("No se detectaron contracciones.")
        return

    ventanas_por_interfaz = 10
    total_interfaces = (len(ventanas) + ventanas_por_interfaz - 1) // ventanas_por_interfaz

    for j in range(total_interfaces):
        fig, axes = plt.subplots(min(10, len(ventanas) - j * 10), 1, figsize=(12, 25), sharex=True)
        if not isinstance(axes, np.ndarray):
            axes = [axes]

        for i in range(len(axes)):
            idx = j * 10 + i
            if idx >= len(ventanas):
                break
            ventana, inicio, fin, pico = ventanas[idx]
            axes[i].plot(np.arange(inicio, fin), ventana, label=f"Ventana {idx + 1}", color='purple')
            axes[i].axvline(x=pico, color='red', linestyle='--', label="Pico")
            axes[i].legend()
            axes[i].grid()

        plt.suptitle(f"Ventanas {j*10+1} - {min((j+1)*10, len(ventanas))}")
        plt.xlabel("Muestras")
        plt.tight_layout()
        plt.show()

# FFT 
def calcular_fft_ventanas(ventanas, fs):
    fft_resultados = []
    for ventana, _, _, pico in ventanas:
        N = len(ventana)

        # Padding si es necesario
        if N < fs:
            ventana = np.pad(ventana, (0, fs - N), mode='constant')

        # Ventana de Hamming
        ventana_hamming = ventana * windows.hamming(len(ventana))

        # FFT y normalización
        espectro = np.abs(np.fft.rfft(ventana_hamming))
        espectro /= np.max(espectro)  # Normalización
        frecuencias = np.fft.rfftfreq(len(ventana), d=1/fs)

        fft_resultados.append((frecuencias, espectro, pico))
    return fft_resultados

# Mostrar FFTs
def mostrar_fft_ventanas(fft_resultados):
    if not fft_resultados:
        print("⚠ No hay FFTs que mostrar.")
        return

    ventanas_por_interfaz = 10
    total_interfaces = (len(fft_resultados) + ventanas_por_interfaz - 1) // ventanas_por_interfaz

    for j in range(total_interfaces):
        fig, axes = plt.subplots(min(10, len(fft_resultados) - j * 10), 1, figsize=(12, 25), sharex=True)
        if not isinstance(axes, np.ndarray):
            axes = [axes]

        for i in range(len(axes)):
            idx = j * 10 + i
            if idx >= len(fft_resultados):
                break
            freqs, espectro, pico = fft_resultados[idx]
            axes[i].plot(freqs, espectro, label=f"Ventana {idx + 1} - Pico {pico}", color='darkorange')
            axes[i].set_xlim(0, 500)
            axes[i].legend()
            axes[i].grid()

        plt.suptitle(f"FFT - Ventanas {j*10+1} - {min((j+1)*10, len(fft_resultados))}")
        plt.xlabel("Frecuencia (Hz)")
        plt.tight_layout()
        plt.show()

# Mostrar señal filtrada y envolvente
def mostrar_filtros():
    if datos is None:
        print("No hay datos cargados.")
        return

    fig, ax = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
    ax[0].plot(datos, label="Señal Original", color="black")
    ax[1].plot(datos_pasa_altas, label="Pasa Altas", color="red")
    ax[2].plot(datos_pasa_bajas, label="Pasa Bajas", color="blue")
    ax[3].plot(envelope, label="Envolvente Hilbert", color="green")
    ax[3].scatter(picos, envelope[picos], color='red', marker='o', label="Contracciones")

    for i in range(4):
        ax[i].legend()
        ax[i].grid()

    ax[0].set_title("Señal Original")
    ax[1].set_title("Filtro Pasa Altas")
    ax[2].set_title("Filtro Pasa Bajas")
    ax[3].set_title("Envolvente (Hilbert)")

    plt.xlabel("Muestras")
    plt.tight_layout()
    plt.show()

#FUNCIÓN PARA LA PRUEBA DE HIPÓTESIS ENTRE LA PRIMERA Y LA ÚLTIMA VENTANA 
def prueba_hipotesis_ventanas(ventanas, alpha=0.05):
    """
    Realiza una prueba de hipótesis t-test (pareado) entre la primera y la última ventana.
    Grafica la distribución t y muestra t_obs, ±t_crítico y la conclusión.
    """

    # Verificar que haya al menos dos ventanas
    if len(ventanas) < 2:
        print("⚠ No hay suficientes ventanas para realizar la prueba de hipótesis.")
        return

    # Extraer la primera y la última ventana
    primera_ventana = ventanas[0][0]   # amplitudes de la primera ventana
    ultima_ventana = ventanas[-1][0]   # amplitudes de la última ventana

    # 1) Estadístico de prueba y p-valor (t-test pareado)
    t_stat, p_value = ttest_rel(primera_ventana, ultima_ventana)

    # Grados de libertad: df = n - 1 (asumiendo que tienen el mismo tamaño)
    n = len(primera_ventana)
    df = n - 1

    # 2) Cálculo de t_crítico (para alpha=0.05, prueba bilateral)
    t_crit = t.ppf(1 - alpha/2, df)

    # 3) Conclusión
    if abs(t_stat) > t_crit:
        conclusion = (f"Se RECHAZA la hipótesis nula (|t_obs| = {t_stat:.3f} > t_crítico = {t_crit:.3f}).\n"
                      f"Existe diferencia estadísticamente significativa (p = {p_value:.5f}).")
    else:
        conclusion = (f"No se rechaza la hipótesis nula (|t_obs| = {t_stat:.3f} <= t_crítico = {t_crit:.3f}).\n"
                      f"No hay evidencia de diferencia estadísticamente significativa (p = {p_value:.5f}).")

    # 4) Graficar la distribución t y las líneas de referencia
    x = np.linspace(-4, 4, 300)  # rango para la curva t
    y = t.pdf(x, df)

    plt.figure(figsize=(8, 4))
    plt.plot(x, y, label=f"Distribución t (df={df})", color="blue")
    plt.axvline(x=t_stat, color='red', linestyle='--', label=f"t_obs = {t_stat:.3f}")
    plt.axvline(x=t_crit, color='green', linestyle='--', label=f"+/- t_crítico = {t_crit:.3f}")
    plt.axvline(x=-t_crit, color='green', linestyle='--')
    plt.title("Prueba de Hipótesis: t-test pareado (Primera vs. Última Ventana)")
    plt.xlabel("Valores de t")
    plt.ylabel("Densidad de probabilidad")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # 5) Imprimir la conclusión en consola
    print("========== RESULTADOS DE LA PRUEBA DE HIPÓTESIS ==========")
    print(f"t_obs = {t_stat:.4f}, p_value = {p_value:.6f}, t_crítico = ±{t_crit:.4f}, df = {df}")
    print(conclusion)
    print("==========================================================")

# --------------------------------------------------
# PARÁMETROS INICIALES
# --------------------------------------------------
ruta_excel = "datos.xlsx"
columna_datos = "Señal"
frecuencia_muestreo = 1000
frecuencia_corte_alta = 20
frecuencia_corte_baja = 450
umbral_contraccion = 0.2

# Procesamiento de datos
datos = cargar_datos_excel(ruta_excel, columna_datos)
if datos is not None:
    datos_pasa_altas = filtro_pasa_altas(datos, frecuencia_corte_alta, frecuencia_muestreo)
    datos_pasa_bajas = filtro_pasa_bajas(datos_pasa_altas, frecuencia_corte_baja, frecuencia_muestreo)
    envelope = np.abs(hilbert(datos_pasa_bajas))
    picos = detectar_contracciones_hilbert(envelope, umbral_contraccion, frecuencia_muestreo)
    ventanas = aplicar_ventanas(picos, envelope, frecuencia_muestreo)
    fft_resultados = calcular_fft_ventanas(ventanas, frecuencia_muestreo)

# --------------------------------------------------
# GUI
# --------------------------------------------------
root = tk.Tk()
root.title("Procesamiento de Señales EMG")

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0)

def seleccionar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx")])
    if archivo:
        global ruta_excel
        ruta_excel = archivo
        label_archivo.config(text=f"Archivo: {archivo.split('/')[-1]}")

ttk.Button(frame, text="Seleccionar Archivo", command=seleccionar_archivo).grid(row=0, column=0)
label_archivo = ttk.Label(frame, text="Archivo: Ninguno")
label_archivo.grid(row=1, column=0)

ttk.Button(frame, text="Mostrar Filtros", command=mostrar_filtros).grid(row=2, column=0)
ttk.Button(frame, text="Mostrar Ventanas", command=lambda: mostrar_ventanas(ventanas)).grid(row=3, column=0)
ttk.Button(frame, text="Mostrar FFT", command=lambda: mostrar_fft_ventanas(fft_resultados)).grid(row=4, column=0)

# ***** NUEVO BOTÓN: PRUEBA DE HIPÓTESIS *****
ttk.Button(frame, text="Prueba de Hipótesis",
           command=lambda: prueba_hipotesis_ventanas(ventanas, alpha=0.05)).grid(row=5, column=0)

root.mainloop()
