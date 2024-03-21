from django.http import JsonResponse
import os
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import subprocess
from projects.models import Project
from django.conf import settings
import shutil
import random
import time
from paho.mqtt import client as mqtt_client

broker = '192.168.0.10'
port = 1883
topic = "Modular/3"
client_id = f'publish-{random.randint(0, 1000)}'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def read_hex_file(file_path):
    hex_content = ""
    with open(file_path, 'r') as file:
        for line in file:
            hex_content += line.strip() + '\\'
    return hex_content

def publish_hex_file(client, hex_file_path, topic):
    hex_content = read_hex_file(hex_file_path)
    print("Bytes enviados:", len(hex_content) + len(topic))
    time.sleep(1)
    result = client.publish(topic, hex_content)
    status = result[0]
    if status == 0:
        print(f"Send to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

class ConfigManager:
    def __init__(self, filename='config.json'):
        self.filename = filename
        self.data = {}
        self.load_config()

    # Cargar la configuración desde el archivo JSON
    def load_config(self):
        try:
            with open(self.filename, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            pass

    # Guardar la configuración en el archivo JSON
    def save_config(self):
        with open(self.filename, 'w') as file:
            json.dump(self.data, file)

    # Obtener el valor de una clave de configuración
    def get_value(self, key):
        return self.data.get(key)

    # Establecer el valor de una clave de configuración
    def set_value(self, key, value):
        self.data[key] = value
        self.save_config()

@csrf_exempt
def compile(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '')
        placa = request.POST.get('placa', '')
        print("Placa seleccionada: ", placa)

        if not codigo:
            return JsonResponse({'success': False, 'message': 'El texto es obligatorio para escribir en el archivo .ino'})

        fqbn_map = {
            "uno": "arduino:avr:uno",
            "nano": "arduino:avr:nano:cpu=atmega328",
            "mega": "arduino:avr:mega:cpu=atmega2560",
            "modular": "arduino:avr:uno"
        }
        fqbn = fqbn_map.get(placa, "arduino:avr:uno")

        # arduino_dev = "/usr/share/arduino/hardware"
        arduino_dev = "D:/Proyectos/modulinoDev/arduinoDev"
        arduino_folder = 'inohub/ino'

        
        folder_actual = os.path.join(os.getcwd(), arduino_folder)
        
        # Rutas para los archivos de salida
        output_path = os.path.join(folder_actual, 'stdout.txt')
        error_path = os.path.join(folder_actual, 'stderr.txt')

        extracted_code_path = os.path.join(folder_actual, 'extracted_code.ino')
        with open(extracted_code_path, 'w') as extracted_code_file:
            extracted_code_file.write(codigo)

        # command = f"/usr/bin/arduino-builder -compile -logger=machine -hardware {arduino_dev} -tools /usr/share/arduino/tools  -tools {arduino_dev}/tools/avr -built-in-libraries {arduino_dev}/arduino/avr/libraries/ -fqbn {fqbn} -vid-pid 1A86_7523 -ide-version=10815 -build-path {folder_actual}/build -warnings=none -build-cache {folder_actual}/Temp -prefs=build.warn_data_percentage=75 -prefs=runtime.tools.arduinoOTA.path={arduino_dev}/tools/avr -prefs=runtime.tools.arduinoOTA-1.3.0.path={arduino_dev}/tools/avr -prefs=runtime.tools.avrdude.path={arduino_dev}/tools/avr -prefs=runtime.tools.avrdude-6.3.0-arduino17.path={arduino_dev}/tools/avr -prefs=runtime.tools.avr-gcc.path={arduino_dev}/tools/avr -prefs=runtime.tools.avr-gcc-7.3.0-atmel3.6.1-arduino7.path={arduino_dev}/tools/avr -verbose {folder_actual}/extracted_code.ino"
        
        command = f"{arduino_dev}/arduino-builder -compile -logger=machine -hardware {arduino_dev}/hardware -tools {arduino_dev}/tools-builder -tools {arduino_dev}/hardware/tools/avr -built-in-libraries {arduino_dev}/libraries -fqbn {fqbn} -vid-pid 1A86_7523 -ide-version=10815 -build-path {folder_actual}/build -warnings=none -build-cache {folder_actual}/Temp -prefs=build.warn_data_percentage=75 -prefs=runtime.tools.arduinoOTA.path={arduino_dev}/hardware/tools/avr -prefs=runtime.tools.arduinoOTA-1.3.0.path={arduino_dev}/hardware/tools/avr -prefs=runtime.tools.avrdude.path={arduino_dev}/hardware/tools/avr -prefs=runtime.tools.avrdude-6.3.0-arduino17.path={arduino_dev}/hardware/tools/avr -prefs=runtime.tools.avr-gcc.path={arduino_dev}/hardware/tools/avr -prefs=runtime.tools.avr-gcc-7.3.0-atmel3.6.1-arduino7.path={arduino_dev}/hardware/tools/avr -verbose {folder_actual}/extracted_code.ino"

        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
            
            # Escribiendo la salida estándar y de error en archivos
            with open(output_path, 'w') as output_file:
                output_file.write(result.stdout)
            with open(error_path, 'w') as error_file:
                error_file.write(result.stderr)

            #shutil.rmtree(os.path.join(folder_actual,'build','sketch','build'))
                
            if result.returncode == 0:
                return JsonResponse({'success': True, 'message': 'Compilación exitosa'})
            else:
                return JsonResponse({'success': False, 'message': 'Error al compilar, verifique los archivos de salida para más detalles'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Método no permitido'})

@csrf_exempt
@login_required(login_url="/auth/login/")
def upload(request):
    fab_file_path = 'inohub/ino/build/extracted_code.ino.hex'
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '')
        if not codigo:
            return JsonResponse({'success': False, 'message': 'El código es obligatorio'})
        try:
            client = connect_mqtt()
            client.loop_start()
            publish_hex_file(client, fab_file_path,topic)
            client.loop_stop()
            client.disconnect()
            return JsonResponse({'success': True, 'message': "Archivo enviado al ESP8266"})
        except Project.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'El proyecto no existe'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Método no permitido'})

@login_required(login_url="/auth/login/")
@csrf_exempt
def saveData(request):
    if request.method == 'POST':
        codigo = request.POST.get('content_data', '')
        name_project = request.POST.get('project', '')
        user_id = request.POST.get('user', '')
        
        if not codigo:
            return JsonResponse({'success': False, 'message': 'El contenido XML es obligatorio'})
        
        try:
            project = Project.objects.get(name=name_project, owner_id=int(user_id))
            fab_file_path = os.path.join(settings.MEDIA_ROOT, 'projects', str(user_id), name_project, f"{name_project}.fab")
            with open(fab_file_path, "w") as fab_file:
                fab_file.write(codigo)
                
            return JsonResponse({'success': True, 'message': "Archivo .fab actualizado exitosamente"})
        except Project.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'El proyecto no existe'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Método no permitido'})

# def run_command_upload():
#     arduino_dev = config_manager.get_value('compiler_location')
#     arduino_dev_folder = os.path.dirname(arduino_dev)
#     folder_actual = os.getcwd()
#     selected_board = 'Modular'
#     selected_port = 'COM1'
#     cpu_mapping = {
#         'Arduino Uno': {'TEXT_CPU': 'atmega328p', 'PROCESSOR': 'arduino', 'BAUD': '115200'},
#         'Arduino Nano': {'TEXT_CPU': 'atmega328p', 'PROCESSOR': 'arduino', 'BAUD': '115200'},
#         'Modular': {'TEXT_CPU': 'atmega328p', 'PROCESSOR': 'arduino', 'BAUD': '115200'},
#         'Robot Betto': {'TEXT_CPU': 'atmega328p', 'PROCESSOR': 'arduino', 'BAUD': '115200'},
#         'Arduino Mega': {'TEXT_CPU': 'atmega2560', 'PROCESSOR': 'wiring', 'BAUD': '115200'}
#     }
#     board_info = cpu_mapping.get(selected_board)

#     text_cpu = board_info['TEXT_CPU']
#     processor = board_info['PROCESSOR']
#     baud = board_info['BAUD']
#     command = f'''{arduino_dev_folder}/hardware/tools/avr/bin/avrdude -C{arduino_dev_folder}/hardware/tools/avr/etc/avrdude.conf -v -p{text_cpu} -c{processor} -P{selected_port} -b115200 -D -Uflash:w:{folder_actual}/build/extracted_code.ino.hex:i'''

#     # Aquí ejecutas el comando
#     os.system(command)