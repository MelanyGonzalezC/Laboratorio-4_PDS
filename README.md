# Laboratorio-4_Fatiga
## Descripción:

### Adquisición de la señal

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

La grfica de pasa bajos elimina variaciones rapidas, solo se conservan las frecuencias bajas y la estructura es muy parecida a la señal original pero sin cambios rapidos, elimina las frecuencias altas sinperder la infromación útil. 

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



