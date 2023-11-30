# voice_recorder.py

import os
import time
import wave
import pyo
import threading
from pyo import Server, pa_list_devices, pa_list_host_apis, pa_get_default_input, pa_get_default_output, pm_list_devices, pm_get_default_input, pm_get_default_output


class VoiceRecorder:
    def __init__(self):
        self.server = Server(duplex=1)
        self.server.start()
        time.sleep(1)
        self.recorder = None
        self.stream = None
        self.en_cours = False
        self.file_path = "enregistrement.wav"

    def get_audio_apis(self):
        # Exemple d'adaptation si pa_list_host_apis retourne une liste de dictionnaires
        host_apis = pa_list_host_apis()
        if host_apis is not None:
            return [api_dict['name'] for api_dict in host_apis]
        else:
            return []

    def get_audio_devices(self):
        # Cette méthode retourne une liste de dictionnaires, chacun représentant un périphérique audio.
        devices_info = pm_list_devices()
        if devices_info is None:  # Vérification si devices_info n'est pas None
            return []  # Retour d'une liste vide si aucun périphérique n'est trouvé

        default_input = pm_get_default_input()
        default_output = pm_get_default_output()
        # Structurer les informations des périphériques de manière à ce qu'elles soient faciles à utiliser dans l'interface utilisateur
        devices = []
        for i, device in enumerate(devices_info):
            device_dict = {
                "index": i,
                "name": device[1],
                "is_input": device[2],
                "is_output": device[3],
                "is_default_input": i == default_input,
                "is_default_output": i == default_output
            }
            devices.append(device_dict)
        return devices

    def set_audio_host_api(self, api_name):
        # Définit l'API hôte audio (par exemple: "asio", "wasapi", etc.)
        self.server.setInOutDevice(api_name)

    def set_input_device(self, device_id):
        # Définit le périphérique d'entrée audio par son ID
        self.server.setInputDevice(device_id)

    def set_output_device(self, device_id):
        # Définit le périphérique de sortie audio par son ID
        self.server.setOutputDevice(device_id)

    def start_server(self):
        # Démarre le serveur avec les paramètres configurés
        self.server.boot()
        self.server.start()

    def start_recording(self):
        if not self.en_cours:
            self.en_cours = True
            self.recorder = pyo.Record(self.stream)
            self.recorder.record()


    def stop_recording(self):
        if self.en_cours:
            self.en_cours = False
            self.recorder.stop()
            self.recorder.saveToFile(self.file_path, 'WAV')
            self.recorder = None

    def play_sound(self):
        if not self.en_cours:
            self.stream = pyo.SfPlayer(self.file_path, speed=1, loop=False).out()

    def audio_file_exists(self):
        return os.path.isfile(self.file_path)



    def run(self):
        self.server.gui(locals())
        self.server.stop()
