# user_interface.py

from PyQt5 import QtWidgets
from voice_recorder import VoiceRecorder
from evenlabs_api import ElevenLabsAPI

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.recorder = VoiceRecorder()
        self.init_ui()
        self.elevenlabs_api = ElevenLabsAPI("9e2b57ba0bd6f9835009f410e69189bd")
        self.load_voices()
        self.voice_combo = QtWidgets.QComboBox(self)


        # contrôles pour les paramètres audio
        self.rate_label = QtWidgets.QLabel("Taux d'échantillonnage: 44100 Hz", self)
        self.rate_input = QtWidgets.QLineEdit(self)
        self.rate_input.setText("44100")

        # contrôles pour interagir avec ElevenLabsAPI
        self.text_to_synthesize = QtWidgets.QTextEdit(self)
        self.synthesize_button = QtWidgets.QPushButton("Synthétiser", self)
        self.synthesize_button.clicked.connect(self.synthesize_speech)

    def init_ui(self):
        self.setWindowTitle("Enregistreur vocal")
        self.setGeometry(100, 100, 400, 200)

        self.text_to_synthesize = QtWidgets.QTextEdit(self)
        self.text_to_synthesize.move(20, 60)
        self.text_to_synthesize.resize(200, 100)

        self.synthesize_button = QtWidgets.QPushButton('Synthétiser', self)
        self.synthesize_button.move(230, 60)
        self.synthesize_button.clicked.connect(self.synthesize_speech)

        self.voice_combo = QtWidgets.QComboBox(self)
        self.voice_combo.move(230, 100)
        self.voice_combo.resize(200, 30)

        self.stop_button = QtWidgets.QPushButton('Arrêter', self)
        self.stop_button.clicked.connect(self.stop_recording)
        self.stop_button.move(150, 20)

        self.play_button = QtWidgets.QPushButton('Jouer', self)
        self.play_button.clicked.connect(self.play_sound)
        self.play_button.move(280, 20)

        # Ajoutez un ComboBox pour sélectionner l'API hôte
        self.api_combo = QtWidgets.QComboBox(self)
        self.api_combo.move(230, 140)
        self.api_combo.resize(200, 30)
        self.api_combo.addItems(
        self.recorder.get_audio_apis())  # Supposons que cette méthode retourne une liste des API hôtes disponibles
        self.api_combo.currentIndexChanged.connect(
        self.update_audio_host)  # Connectez le signal à la méthode appropriée

        devices = self.recorder.get_audio_devices()
        if devices:  # Ajoutez cette vérification pour vous assurer que devices n'est pas None
            for device in devices:
                self.input_combo.addItem(device['name'], device['index'])
                self.output_combo.addItem(device['name'], device['index'])

        # Ajoutez des ComboBox pour les périphériques d'entrée et de sortie
        self.input_combo = QtWidgets.QComboBox(self)
        self.input_combo.move(230, 180)
        self.input_combo.resize(200, 30)
        self.output_combo = QtWidgets.QComboBox(self)
        self.output_combo.move(230, 220)
        self.output_combo.resize(200, 30)

        # Populez les ComboBox avec les périphériques audio disponibles
        devices = self.recorder.get_audio_devices()
        for device in devices:
            self.input_combo.addItem(device['name'], device['index'])
            self.output_combo.addItem(device['name'], device['index'])

    def update_audio_host(self):
        # Mettez à jour l'API hôte en fonction de la sélection de l'utilisateur
        selected_api = self.api_combo.currentText()
        self.recorder.set_audio_host_api(selected_api)

    def update_audio_devices(self):
        # Mettez à jour les périphériques d'entrée et de sortie en fonction de la sélection de l'utilisateur
        input_device_id = self.input_combo.currentData()
        output_device_id = self.output_combo.currentData()
        self.recorder.set_input_device(input_device_id)
        self.recorder.set_output_device(output_device_id)

    def synthesize_speech(self):
        text = self.text_to_synthesize.toPlainText()
        voice_id = self.voice_combo.currentData()  # Récupérer l'ID de la voix sélectionnée
        resultat = self.elevenlabs_api.synthesize_speech(text, voice_id)
        print(resultat)

    def load_voices(self):
        voices = self.elevenlabs_api.get_available_voices()
        for voice in voices:
            voice_id = voice.get('voice_id')
            if voice_id is not None:
                self.voice_combo.addItem(voice['description'], voice_id)
            else:
                print("Voice ID missing for", voice)


    def start_recording(self):
        # Mettez à jour les périphériques sélectionnés
        self.update_audio_devices()
        self.recorder.start_server()

        # Démarrer le serveur audio
        self.recorder.start_server()
        # Commencer l'enregistrement audio
        self.recorder.start_recording()

    def stop_recording(self):
        # Arrêter l'enregistrement audio
        self.recorder.stop_recording()

    def play_sound(self):
        # Jouer l'audio enregistré
        self.recorder.play_sound()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
