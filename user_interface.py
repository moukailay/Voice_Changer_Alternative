import wave
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon

class VoiceRecorderUI(QWidget):
    def __init__(self):
        super().__init__()
        # Déclaration des attributs
        self.recordButton = None
        self.stopButton = None
        self.playButton = None
        self.uploadButton = None
        self.downloadButton = None
        self.messageLabel = None
        self.progressBar = None

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # Initialisation des Boutons
        self.recordButton = QPushButton("Enregistrer")
        self.stopButton = QPushButton("Arrêter")
        self.playButton = QPushButton("Jouer")
        self.uploadButton = QPushButton("Uploader")
        self.downloadButton = QPushButton("Télécharger")

        # Initialisation du Label et ProgressBar
        self.messageLabel = QLabel("Prêt à enregistrer")
        self.progressBar = QProgressBar()

        # Ajouter les widgets au layout
        self.layout.addWidget(self.recordButton)
        self.layout.addWidget(self.stopButton)
        self.layout.addWidget(self.playButton)
        self.layout.addWidget(self.uploadButton)
        self.layout.addWidget(self.downloadButton)
        self.layout.addWidget(self.messageLabel)
        self.layout.addWidget(self.progressBar)

        self.setLayout(self.layout)

        # Connecter les boutons à leurs fonctions
        self.recordButton.clicked.connect(self.onRecord)
        self.stopButton.clicked.connect(self.onStop)
        self.playButton.clicked.connect(self.onPlay)
        self.uploadButton.clicked.connect(self.onUpload)
        self.downloadButton.clicked.connect(self.onDownload)

    def onRecord(self):
        self.isRecording = True
        self.messageLabel.setText("Enregistrement en cours...")

        self.stream = self.pyaudio.open(format=self.format, channels=self.channels,
                                        rate=self.rate, input=True,
                                        frames_per_buffer=self.chunk_size)
        self.frames = []

        while self.isRecording:
            data = self.stream.read(self.chunk_size)
            self.frames.append(data)

    def onStop(self):
        self.isRecording = False
        self.messageLabel.setText("Enregistrement arrêté")

        self.stream.stop_stream()
        self.stream.close()

        self.pyaudio.terminate()

        # Sauvegarde de l'enregistrement dans un fichier
        with wave.open('enregistrement.wav', 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.pyaudio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))

    def onPlay(self):
        self.messageLabel.setText("Lecture de l'enregistrement")

        # Jouer le fichier 'enregistrement.wav'
        with wave.open('enregistrement.wav', 'rb') as wf:
            stream = self.pyaudio.open(format=self.pyaudio.get_format_from_width(wf.getsampwidth()),
                                       channels=wf.getnchannels(),
                                       rate=wf.getframerate(),
                                       output=True)

            data = wf.readframes(self.chunk_size)
            while data:
                stream.write(data)
                data = wf.readframes(self.chunk_size)

            stream.stop_stream()
            stream.close()

    def onUpload(self):
        self.messageLabel.setText("Upload en cours...")

        # Remplacer par l'URL de votre API ou service d'upload
        url = "http://monapi.com/upload"
        files = {'file': open('enregistrement.wav', 'rb')}

        response = requests.post(url, files=files)

        if response.status_code == 200:
            self.messageLabel.setText("Upload réussi")
        else:
            self.messageLabel.setText("Erreur d'upload")

    def onDownload(self):
        self.messageLabel.setText("Téléchargement en cours...")

        # TODO: Remplacer par l'URL du fichier à télécharger
        url = "http://monapi.com/enregistrement.wav"
        response = requests.get(url)

        if response.status_code == 200:
            with open('enregistrement_telecharge.wav', 'wb') as f:
                f.write(response.content)
            self.messageLabel.setText("Téléchargement réussi")
        else:
            self.messageLabel.setText("Erreur de téléchargement")
if __name__ == '__main__':
    app = QApplication([])
    ex = VoiceRecorderUI()
    ex.show()
    app.exec_()
