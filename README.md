# Laboratorio-4_Fatiga
## Descripción:

En esta práctica de laboratorio se abordó el análisis de señales electromiográficas (EMG) como herramienta para detectar la fatiga muscular, mediante la aplicación de técnicas de procesamiento digital de señales. Se emplearon electrodos de superficie conectados a un sistema de adquisición de datos, registrando la señal EMG durante una contracción sostenida del músculo del antebrazo. Posteriormente, la señal fue filtrada utilizando filtros pasa altas y pasa bajas con el fin de reducir el ruido de baja frecuencia y eliminar interferencias de alta frecuencia. La señal procesada fue segmentada en ventanas utilizando una función de Hamming, y en cada una se aplicó la transformada rápida de Fourier (FFT) para obtener el espectro de frecuencias. Como parte del análisis, se evaluó la variación de la frecuencia mediana en el tiempo, considerando su disminución como un indicador fisiológico de fatiga. Finalmente, se aplicó una prueba de hipótesis para determinar si los cambios observados eran estadísticamente significativos, integrando así conocimientos tanto de señal como de análisis estadístico para interpretar fenómenos fisiológicos.

### Adquisición de la señal
En este apartado de la guía, para realizar la adquisición de la señal EMG se utilizó una DAQ para capturar la señal del musculo, un módulo ECG para tomar la señal y electrodos. De esta manera se colocaron los electrodos para tomar la señal EMG del musculo del antebrazo.

 ![image](https://github.com/user-attachments/assets/3ada8aba-aaca-4aa5-bba5-0b1b91f33c41)
*Ubicación de los electrodos para toma de la señal*

Esto, con el propósito de observar las contracciones musculares posibles hasta la fatiga, en nuestro caso la persona realizo 70 contracciones en 60 segundos, pero no fue posible llegar a la fatiga debido a que no se utilizo suficiente fuerza para que en este tiempo se agotara el musculo. 
De esta manera se realizó un código especifico para capturar la señal y convertir los datos en un archivo de Excel para que el análisis sea mas sencillo. 

![image](https://github.com/user-attachments/assets/b91652ff-2f00-47a4-8685-7889c4965830)
*Codigo para adquisición de la señal*

En el siguiente código estas dos funciones realizan principalmente la adquisición de datos por medio de la frecuencia de muestreo y el tiempo en el que se quiere tomar la señal, en este caso 60 seg. Posteriormente lee los datos y los procesa por medio de la función procesar_datos que crea un vector basado en la frecuencia de muestreo y luego se muestra la grafica por medio de una imagen  y un archivo en Excel con todos los datos adquiridos.
Para implementar la señal en el código para posteriormente filtrarla, crear las ventanas, el análisis espectral y la prueba de hipótesis se utilizo un código que crea una ventana con diferentes botones, como seleccionar el archivo, mostrar los filtros, las ventas y FFT. 

![image](https://github.com/user-attachments/assets/d4809431-8630-431f-8554-026a10e4e163)
*Código para crear el marco contenedor*


Con el siguiente código se crea un marco contenedor, con los botones de selección por el usuario ya mencionados anteriormente y de igual manera mantiene la interfaz abierta para escoger las diferentes opciones.

![image](https://github.com/user-attachments/assets/d4bc1de0-c7d9-4a99-8194-f5cbe514205b)
*Código para cargar los datos de excel*

Luego de seleccionar el botón de seleccionar archivo se sube el Excel de datos con los valores obtenidos de la señal EMG, de esta manera busca la ruta del archivo y la columna que se busca analizar del archivo que en este caso es el voltaje y convierte estos datos een un array (datos del mismo tipo)  y los convierte en la siguiente señal:

![image](https://github.com/user-attachments/assets/7837c3e9-f2ba-4620-943a-e9bf2f11cee2)
*Señal EMG original*
 
La señal EMG mostrada en la imagen representa la actividad eléctrica de un músculo en respuesta a estímulos nerviosos. Se observa una variabilidad en la amplitud, lo que indica que el músculo está siendo activado con diferente intensidad a lo largo del tiempo. 
También se aprecia que la señal tiene una apariencia irregular y con variaciones en la densidad de los picos. Esto puede deberse a cambios en la fuerza de contracción del músculo o a variaciones en la fatiga. En algunos momentos, la amplitud parece disminuir, lo que podría indicar un posible indicio de fatiga muscular.
Para una mejor evaluación de la fatiga muscular, es ideal analizar la evolución de las frecuencias a lo largo del tiempo mediante una transformada de Fourier (FFT) que se hará mas adelante.


### Filtrado de la señal
Para esta parte de la guia, una vez la señal tomada se analiza para poder realizar el filtrado de dicha señal,para lograr observar una señal mas clara, esto por medio de un friltro pasa altos y un filtro pasa bajos. De igual manera se sieñan con un filtro llamado  filtro butterworth que es un tipo de filtro de procesamiento de señales diseñado para tener una respuesta en frecuencia lo más plana posible en la banda de paso.  

Con esta definición evaluamos que un filtro pasa altos es un tipo de filtro diseñado para cortar las frecuencias bajas extrañas en un punto de corte específico y por otro lado el filtro pasa bajos permite el paso de las frecuencias bajas, y atenúa todas las altas frecuencias a partir de una frecuencia de corte fc. De esta manera se implementa en el codigo para filtrar la señal:

![image](https://github.com/user-attachments/assets/b6e411dc-4ac6-468c-815c-282649b9ad90)


*Codigo para diseño de filtro Butterworth*

Se debe tener en cuenta el orden de ambos filtros y posteriormente calcular la frecuencia de nyquist la cual se calcula como la mitad de la frecuencia de muestreo. Luego de ello, se normaliza la fc(frecuencia de corte), una vez calculados estos datos se realiza el diseño de los filtros pasa altos y pasa bajos cn la función *Butter*.

Por otra parte, como detalle importante para el diseño de estos filtros en el codigo tambien se establece lo siguiente:

![image](https://github.com/user-attachments/assets/f8fc0f2b-64ff-4685-acf1-648ac7926651)

*Datos de frecuencias en filtros*

En este caso se establece la frecuencia de muestreo de 1000Hz (es decir 1000 muestras por segundo) y con la frecuencia de nyquiz se determina que el maximo contenido en frecuencia que podemos analizar es 500Hz. De igualmanera, la frecuencia de corte ya mencionada anteriormente se le aplica el valor de 20Hz para el filtro pasa altas evidencia que bloquea las frecuencias menores a este valor y para el filtro pasa bajas se determina la frecuencia de corte como 450Hz, es decir bloquea la frecuencias mayores a este valor y deja pasar las inferiores (se elimina ruido de alta frecuencia). 



Al implementar este codigo a la señal EMG tomada, se obtiene lo siguiente:

![image](https://github.com/user-attachments/assets/97d353a6-5077-41ca-afd9-5609848c18d6)
*Señal EMG con filtros de pasa altas y pasa bajas*

Obtenemos que se toman 60000 muestras en 60 s es decir la frecuencia de muestreo multiplicado por el tiempo de la señal, observamos las graficas por medio de muestras.
Analizando la grafica de filtro pasa altos obtenemos que se elimina la baja frecuencia de la señal observando cambios mas bruscos y rapidos en la forma de onda. 

La grfica de pasa bajos elimina variaciones rapidas, solo se conservan las frecuencias bajas y la estructura es muy parecida a la señal original pero sin cambios rapidos, elimina las frecuencias altas sinperder la infromación útil. El hecho de que las señales filtradas aún muestren apariencia de ruido significa que: El ruido tiene componentes en el rango de paso del filtro, por lo que no puede ser eliminado completamente. El filtrado puede amplificar ciertas características de la señal, como las oscilaciones rápidas, dándole un aspecto ruidoso.


### Aventanamiento

Por otro lado, encontramos una parte fundamental del desarrollo de esta práctica que es el proceso de aventanamiento que es de una técnica importante para el procesamiento de la señal electromiografica y se emplean para analizar el cambio de las características espectrales de una señal cualquiera, en nuestro caso EMG a lo largo del tiempo. 
Una pregunta importante que nos planteamos es: ¿Por qué dividir la señal en ventanas?
Esto es porque la señal EMG es no estacionaria, esto quiere decir que sus características estadísticas cambian con el tiempo por ejemplo está variando con cada contracción muscular, por ende, no tiene mucho sentido analizar una señal como si fuera constante por eso se divide la señal en segmentos o ventanas pequeñas de tiempo, esto facilita porque cada ventana capturara solo una parte de la señal. 

Para el desarrollo de las ventanas, se dio uso de las ventanas Hamming puesto que esta se usa para suavizar los extremos de una señal cunado se divide en fragmentos. Se uso este tipo de ventanas porque la señal es no estacionaria y contienen muchos componentes de alta frecuencia. Si se quiere analizar una parte específica, como una contracción se debe recortar ese fragmento, sin embargo, cortar en ventanas rectangulares genera bordes abruptos, que genera un efecto en el dominio de la frecuencia denominado fuga espectral. 

La fuga espectral ocurre cuando una señal no termina en un punto de cero o cambia abruptamente al final del segmento. Esto hace que la energía de una frecuencia aparezca distribuida en muchas otras frecuencias no reales cuando aplicamos la FFT.

Se uso la ventana de haming por estas razones:
1.	Reducción efectiva de la fuga espectral.





• Eso significa que minimiza el ruido espectral no deseado.







• Preserva mucho mejor la forma real del espectro que queremos analizar.

2.	Buena resolución espectral:
la de Hamming preserva mejor la amplitud de las frecuencias principales, lo cual es importante si analizamos la intensidad de una contracción muscular.

3.	Suaviza la señal sin distorsionarla.
4.	Es estándar en análisis EMG: En muchos estudios de señales biomédicas, la ventana de Hamming es una de las más utilizadas porque equilibra precisión espectral y conservación de energía.

Esa era la parte teórica, ahora, para la parte práctica lo primero que se tuvo que realizar fue aplicar la transformada de Hilbert a la señal puesto que al realizar el análisis de la cantidad de contracciones realizadas en un minuto por medio de un sensor ecg se evidencio que cualquier pico lo estaba tomando como contracción y así no debe ser, por ende, se hizo en análisis por medio de Hilbert ya que esta toma tu señal y la transforma en una especie de “versión completa” que te permite analizar cómo cambia su amplitud y su fase con el tiempo y así mismo para que realizara una envolvente a la señal y dejara solo las contracciones o picos más elevados, pero aun así seguían siendo bastantes “contracciones” en poco tiempo, entonces por medio de la observación se estableció un umbral de referencia y que así por medio de código todos los picos de la señal que estuvieran por encima de 0,2 voltios los tomara como contracción y lo demás no. Gracias a esto se redujo el número de contracciones y por ende la cantidad de ventanas, dejando 70 contracciones en 60 segundos. 

![image](https://github.com/user-attachments/assets/989bcd76-081f-4d73-a353-5d13ae2e58df)



Función que detecta contracciones.



Luego de detectar las contracciones se procede a aplicar las ventanas Hamming para cada una de las contracciones, para el desarrollo de esta lo que se busco fue el eje de simetría de la ventana coincidiera con el máximo pico de la contracción puesto que dicho eje siempre tiene una amplitud de 1 por ende se convoluciono la ventana con la señal que en palabras más fáciles estas se multiplicara por 1 y como los demás valores van entre 0 y 1 todos los demás valores de la  señal se van a atenuar. 



![image](https://github.com/user-attachments/assets/7163d5a8-95ed-41c8-9b86-014dca9d29f3)




Función que detecta las ventanas.





![image](https://github.com/user-attachments/assets/697fcc25-166a-487f-90c4-cf575d6917f4)


Función para mostrar las ventanas.



Como se puede evidenciar en este fragmento de código se estableció que por cada interfaz gráfica se mostraran 10 ventanas ya que como se menciona con anterioridad salieron bastantes contracciones. 




![image](https://github.com/user-attachments/assets/db7451fb-4fb0-4efe-9ea4-4a9f479b7221)



Selecciona opción “mostrar ventanas”.




Esta opción permite mostrar las diferentes ventanas creadas por cada contracción. 






![image](https://github.com/user-attachments/assets/dd08a8ad-d4fc-4b35-b40d-377dfe20abc3)





Grafico de las ventanas obtenidas. 



Como se puede ver en la imagen así es como se ve cada una de las interfaces que contienen las ventanas de nuestra señal, donde la línea morada indica la ventana y la liena punteada roja el pico máximo de la señal. Se observa que algunas ventanas presentan picos altos y claros, indicando contracciones fuertes, mientras que otras muestran menor actividad, sugiriendo relajación muscular. Además, la distribución temporal de los picos no es uniforme, lo que indica variabilidad en la ocurrencia de los momentos de máxima activación. Si la gráfica representa la envolvente de la señal obtenida mediante la Transformada de Hilbert, esto permitiría visualizar la variación de la amplitud en el tiempo, facilitando el análisis sin depender de las fluctuaciones de alta frecuencia.






### Análisis espectral
El análisis espectral se realiza una vez se determinan las ventanas de la señal que en este caso se obtuvieron 70, es decir se realizaron 70 contracciones en un tiempo de 60 segundos, se utilizando la Transformada de Fourier (FFT) para obtener el espectro de frecuencias en intervalos específicos de la señal EMG.

Analisis espectral:  consiste en descomponer una señal en sus componentes de frecuencia. Para ello, se usa la Transformada Rápida de Fourier (FFT, Fast Fourier Transform), que convierte la señal del dominio del tiempo al dominio de la frecuencia.  El resultado del análisis de Fourier es un espectro de amplitud, con las mismas unidades de amplitud que tenía la señal en el tiempo. 

De esta manera se implementa el codigo para realizar el análisis espectral de cada ventana por medio de la Transformada de Fourier para analizar como cambian las frecuencias a lo largo del tiempo, asi:

![image](https://github.com/user-attachments/assets/8457bb65-5ba1-4f5c-8411-84516d873bf9)
*Codigo para realizar analisis espectral*

La función calcular_fft_ventanas() tiene la función de realiizar fft por varias ventanas y devuelve el espectro de frecuencias para cada ventana, en primer lugar se analizan las ventanas ya determinadas anteriormentente y se crea un vector para guardar las transformadas. Se utiliza el pico de cada ventana y la señal EMG completa y se revisa el tamaño por ventana para evitar errores en la FFT.

Por otro lado, se analiza que el tipo de ventana usada fue Hamming y se realiza el calculo de la FFT y normaliza este resultado para que la amplitud este entre 0 y 1. Se obtienen las frecuencias a cada valor del espectro y se define el intervalo de muestreo y por ultimo se guardan los calculos realizados. Se obtienen las siguientes graficas.

![image](https://github.com/user-attachments/assets/2706de4b-2327-4487-a8b2-174ee466489d)
*Graficas de analisis espectral*

Se observa mediante las primeras 10 graficas de análisis espectral de las primeras ventas que la mayor parte de la energía se concentra en las frecuencias bajas, esto debido a que las señales EMG se caracterizan por mantenerar un rango de 20 a 450Hz, indicando que la frecuencias altas son menos significativas.


De igual manera podemos observar que todas las graficas son bastante similares entre si. concluyendo que la señal EMG es consistente en el tiempo. Por otro lado, como se configuro en el codigo estan normalizadas para que su amplitud este entre 0 y 1, esto para observar la comparación de todas las gráficas. 

Logramos deducir que en la mayoría de ventanas la energía cae despues de los 100Hz, y por otra parte el pico que se indica en la parte superior de las gráficas indica el momento en el que ocurrió una activación importante, es decir el momento de la activación muscular. 

Frecuencias de pico: En las primeras ventanas (1-10), los valores de pico están en un rango más bajo (entre 5500 y 7000). Conforme avanza la numeración de las ventanas, los picos van aumentando progresivamente. En las últimas ventanas analizadas (61-70), los valores de los picos están por encima de 53000.

Atenuación y dispersión: Al inicio, la señal muestra una concentración más definida de energía en frecuencias más bajas. Sin embargo, conforme se acerca la fatiga muscular (en ventanas más avanzadas), la energía se dispersa más, y el espectro parece perder intensidad en las frecuencias más altas.

Fenómeno de Fatiga Muscular: Este cambio en el espectro es característico de la fatiga muscular. A medida que la fatiga se instala, hay un desplazamiento de la frecuencia pico hacia valores más bajos, y la señal pierde energía en las altas frecuencias. Esto se debe a que, con la fatiga, las unidades motoras de contracción rápida dejan de activarse, lo que provoca una mayor presencia de componentes de baja frecuencia en la señal EMG.


### Prueba de hipotesis

El objetivo principal de realizar este test es determinar, de forma estadística, si existe una diferencia significativa entre dos condiciones de la señal EMG: en este caso, entre la primera ventana (estado inicial) y la última ventana (estado de fatiga). En otras palabras, se busca confirmar, con un nivel de confianza definido (en este caso, α = 0.05), si la disminución en la amplitud de la señal que se espera teóricamente cuando el músculo se fatiga es realmente significativa y no se debe al azar.

Este análisis permite respaldar la hipótesis alternativa y refutar la hipótesis nula, que plantea que, a medida que se produce la fatiga, la mediana (o medida central) de la amplitud de la señal permanece igual. De este modo, se proporciona una base objetiva para interpretar los cambios en la señal y, en consecuencia, comprender mejor la respuesta muscular frente a la fatiga.

Para comenzar con la prueba de hipótesis, se inició buscando funciones que ayuden a realizar este análisis.

![image](https://github.com/user-attachments/assets/2f0b1ba5-1945-483f-b49d-bd20af925191)
*Librerias*

Se establece el valor de alfa (α) como el nivel de significancia y se verifica la presencia de al menos dos ventanas. Se extrae la información de ambas ventanas y se realiza una prueba estadística utilizando el test t pareado para compararlas. El objetivo es obtener el estadístico de prueba (t_stat) y el p_value asociado, que indica la probabilidad de observar una diferencia al menos tan extrema como la encontrada, en caso de que la hipótesis nula sea cierta.

A continuación, se calculan los grados de libertad, asumiendo que la cantidad de datos en ambas ventanas es similar, y se determina el valor crítico de t (t_crit) para una prueba bilateral. Finalmente, se llega a una conclusión en función del valor obtenido de t en relación con los límites establecidos por t_crit y su representación gráfica.

![image](https://github.com/user-attachments/assets/3a25a12c-fe04-4989-a1b1-3ccc30e2d126)
*Código de los pasos realizados*

Para finalizar se grafica la informacion para su visualización

![image](https://github.com/user-attachments/assets/2c8e5b17-2bd3-48ef-bc8c-33242f981397)
*Código para visualización de señal*

![image](https://github.com/user-attachments/assets/902b68b4-ffdb-4fe2-9ade-57251c9bbfdd)
*Gráfica  señal*

Con esto, podemos concluir que, al ser el valor de t mayor que el valor crítico positivo, se considera que se encuentra dentro de la región de rechazo. En términos prácticos, se rechaza la hipótesis nula. Relacionando este resultado con la afirmación de que la señal tenía mayor intensidad al inicio que al final, se concluye que existe evidencia estadísticamente significativa para respaldar que la intensidad de la señal en la primera ventana es mayor que en la última. Esto indica que la disminución en la amplitud de la señal (asociada con la fatiga muscular) es real y no atribuible al azar.

El análisis espectral confirma la presencia de fatiga muscular, evidenciada por la reducción de la energía en altas frecuencias y el desplazamiento de la frecuencia de pico hacia valores menores conforme avanza el tiempo.

## Requisitos:
Python 3.9
Numpy
Pandas
Matplotlib.pyplot
Scipy.signal import butter, filtfilt, find_peaks, hilbert, windows
Tkinter

## Contactanos:
est.mariajose.perez@unimilitar.edu.co
est.melany.gonzalez@unimilitar.edu.co
est.david.smoreno@unimilitar.edu.co








