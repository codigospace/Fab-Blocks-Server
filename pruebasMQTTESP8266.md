# Documentación de Pruebas de Software

## Caso de Prueba: Recepción y escritura  de archivos en ESP8266 

### Descripción
Este caso de prueba evalúa el peso, veces enviado, veces recibido y veces recibido incompletamente
de la recepción de archivos en un ESP8266 desde un servidor broker MQTT

### Pasos de Ejecución
1. Conectar el ESP8266 a la PC para una alimentación.
2. Configuración del microcontrolador por medio de Arduino IDE.
3. Visualización de respuestas de ESP8266 por el monitor serie.
4. Envio de archivos por medio de un script en Python para el broker MQTT.
5. Revisión los archivos enviados, recibidos, recibidos con error y calcular el peso total.

### Criterios de Aceptación
- El archivo se recibe correctamente.
- Todos los archivos son enviados y recibidos correctamente.
- No se registra ningún error en la carga de archivos.
- Cantidad de veces que el ESP8266 puede manejar los archivos.

## Resultados de Pruebas

| Caso | Peso (KB) | Enviados | Recibidos | Incompletos | Archivo Incompleto (Bytes) | Error | Espacio libre (Bytes) | Espacio usado (Bytes) | Observaciones                                                                                  |
|------|-----------|----------|-----------|-------------|----------------------------|-------|-----------------------|-----------------------|------------------------------------------------------------------------------------------------|
| 1    | 13        | 10       | 3         | 1           | 3071                       | 6     | 10761                 | 40352                 | El cuarto archivo fallo                                                                        |
| 2    | 3.6       | 10       | 10        | 0           | 3071                       | 0     | 17401                 | 32489                 | El onceavo archivo fallo                                                                       |
| 2    | 3.6       | 10       | 10        | 0           | 3514                       | 0     | 17443                 | 36395                 | Se eliminó el decimo archivo se envia uno diferente de 6962 Bytes, solo se escriben 3514 Bytes | 
| 3    | 5.5       | 10       | 7         | 1           | 1024                       | 2     | 13556                 | 38381                 | Luego del 8vo archivo ya no se puede escribir                                                  |
| 4    | 7.5       | 10       | 5         | 1           | 2048                       | 3     | 13308                 | 37605                 | El sexto archivo no se escribió correctamente                                                  |
| 5    | 25.1      | 10       | 0         | 0           | 0                          | 0     | 52961                 | 0                     | Lo leyó el servidor, pero no el ESP8266, posible maximo de recepción                           |
| 6    | 18        | 10       | 0         | 0           | 0                          | 0     | 52961                 | 0                     | Solo recibió el servidor MQTT, no ESP8266                                                      |
| 7    | 15.7      | 10       | 2         | 1           | 11263                      | 7     | 9500                  | 43,461                | El tercer archivo fallo en la escritura                                                        |