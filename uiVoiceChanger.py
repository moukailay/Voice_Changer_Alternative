import threading
from datetime import datetime
from time import sleep

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider, QListWidget
from pydub import AudioSegment
from pydub.playback import play
from pyo import *

from logic import pitch, speed, volume, exportModifiedSound, recordSound, playRecordedSound, playModifiedSound, \
    liveVoiceChanger, preset1


class VoiceChangerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.recordingsList = None
        self.liveVoiceChanger = None
        self.initUI()
        self.initAudio()
        self.initServer()
        self.load_recordings()
        self.pitch_val = 5
        self.delay_val = 0.002
        self.feedback_val = 0.1
        self.freq_val = 40000
        self.q_val = 20000


    def initServer(self):
        try:
            self.server = Server().boot()
            self.server.start()
        except Exception as e:
            print("Erreur lors du démarrage du serveur audio:", e)
            # Gérer l'erreur ou fermer l'application si nécessaire

    def initUI(self):
        self.setWindowTitle('Voice Changer')
        self.setFixedSize(800, 600)



        # Style de l'application
        self.live_btn = QPushButton('Live Test', self)
        self.live_btn.setStyleSheet("background-color: #5D5D5D; border-radius: 10px; padding: 10px;")
        self.record_btn = QPushButton('Record', self)
        self.setStyleSheet("background-color: #282828; color: white; font-size: 16px;")
        self.setWindowIcon(QIcon('icon.png'))

        # Boutons
        self.live_btn = QPushButton('Live Test', self)
        self.live_btn.setStyleSheet("background-color: light-gray ;border-radius: 10px; padding: 10px; font-size: 30px;")
        self.record_btn = QPushButton('Record', self)
        self.record_btn.setStyleSheet("background-color: light-gray ;border-radius: 10px; padding: 10px; font-size: 30px;")
        self.play_btn = QPushButton('Play', self)
        self.play_btn.setStyleSheet("background-color: light-gray ;border-radius: 10px; padding: 10px; font-size: 30px;")

        # Sliders
        self.pitch_slider = QSlider(Qt.Horizontal)
        self.pitch_slider.setStyleSheet("QSlider::handle:horizontal {background-color: #FF5733;}")
        self.pitch_slider = QSlider(Qt.Horizontal)
        self.speed_slider = QSlider(Qt.Horizontal)
        self.volume_slider = QSlider(Qt.Horizontal)
        self.setupSlider(self.pitch_slider, -1200, 1200, 0, 100)  # de -12 à 12 (valeurs * 100 pour précision)
        self.setupSlider(self.speed_slider, 0, 1000, 500, 50)  # de 0s à 1s pour le delay
        self.setupSlider(self.volume_slider, 0, 100, 50, 10)  # de 0 à 1 pour le feedback

        # Labels

        self.pitch_label = QLabel('Pitch:')
        self.pitch_label.setStyleSheet("font-size: 30px;")

        self.speed_label = QLabel('Speed:')
        self.speed_label.setStyleSheet("font-size: 30px;")

        self.volume_label = QLabel('Volume:')
        self.volume_label.setStyleSheet("font-size: 30px;")

        self.pitch_value_label = QLabel(str(self.pitch_slider.value()))
        self.speed_value_label = QLabel(str(self.speed_slider.value()))
        self.volume_value_label = QLabel(str(self.volume_slider.value()))
        self.save_btn = QPushButton('Save Audio', self)
        self.save_btn.setStyleSheet("background-color: light-gray ;border-radius: 10px; padding: 10px; font-size: 30px;")
        self.status_label = QLabel('Status:')
        self.status_label.setStyleSheet("font-size: 30px;")
        self.status_label.setStyleSheet("font-size: 30px;")
        self.status_label.setStyleSheet("color: white; font-size: 16px;")
        self.status_icon = QLabel(self)

        self.status_icon.setPixmap(QIcon('red_circle_icon.png').pixmap(20, 20))
        self.status_icon.hide()

        # Layouts
        vbox = QVBoxLayout()
        self.addWidgetsToLayout(vbox, [self.live_btn, self.record_btn, self.play_btn])
        self.addSliderToLayout(vbox, self.pitch_label, self.pitch_slider, self.pitch_value_label)
        self.addSliderToLayout(vbox, self.speed_label, self.speed_slider, self.speed_value_label)
        self.addSliderToLayout(vbox, self.volume_label, self.volume_slider, self.volume_value_label)
        vbox.addWidget(self.save_btn)
        hbox_status = QHBoxLayout()
        hbox_status.addWidget(self.status_label)
        hbox_status.addWidget(self.status_icon)
        vbox.addLayout(hbox_status)
        self.setLayout(vbox)

        # Connect signals
        self.live_btn.clicked.connect(self.toggle_live)
        self.record_btn.clicked.connect(self.toggle_record)
        self.play_btn.clicked.connect(self.toggle_play)
        self.save_btn.clicked.connect(self.save_audio)
        self.pitch_slider.valueChanged.connect(self.update_pitch_value)
        self.speed_slider.valueChanged.connect(self.update_speed_value)
        self.volume_slider.valueChanged.connect(self.update_volume_value)

        # Liste des enregistrements
        self.recordingsList = QListWidget(self)
        self.recordingsList.setStyleSheet("""
                    QListWidget {background-color: #282828; color: white;} 
                    QListWidget::item {border-bottom: 1px solid #505050;} 
                    QListWidget::item:selected {background-color: #505050;}
                """)
        vbox.addWidget(self.recordingsList)

        self.recordingsList.itemDoubleClicked.connect(self.play_sound)


        self.delete_btn = QPushButton('Supprimer', self)
        self.delete_btn.clicked.connect(self.delete_selected_recording)
        vbox.addWidget(self.delete_btn)

    def delete_selected_recording(self):
        selected_item = self.recordingsList.currentItem()
        if selected_item:
            audio_path = selected_item.text()

            # Suppression du fichier audio
            if os.path.exists(audio_path):
                os.remove(audio_path)
                print(f"Le fichier {audio_path} a été supprimé.")

            # Suppression de l'élément de la liste
            row = self.recordingsList.row(selected_item)
            self.recordingsList.takeItem(row)
            self.save_recording_list()

    def save_recording_list(self, new_recording=None):
        with open("recordings_list.txt", "a" if new_recording else "w") as file:
            if new_recording:
                file.write(new_recording + "\n")
            else:
                for index in range(self.recordingsList.count()):
                    file.write(self.recordingsList.item(index).text() + "\n")

    def load_recordings(self):
        if os.path.exists("recordings_list.txt"):
            with open("recordings_list.txt", "r") as file:
                for line in file:
                    self.recordingsList.addItem(line.strip())

    def initAudio(self):
        self.recordedSoundPath = 'outputs/output.wav'
        self.modifiedSoundPath = 'outputs/outputModified.wav'
        self.server = Server().boot()
        self.server.start()
        self.mic = Input(mul=0.2)
        self.sound = None

    def setupSlider(self, slider, min_val, max_val, init_val, tick_interval):
        slider.setRange(min_val, max_val)
        slider.setValue(init_val)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(tick_interval)

    def addWidgetsToLayout(self, layout, widgets):
        for widget in widgets:
            layout.addWidget(widget)

    def addSliderToLayout(self, layout, label, slider, value_label):
        hbox = QHBoxLayout()
        hbox.addWidget(label)
        hbox.addWidget(slider)
        hbox.addWidget(value_label)
        layout.addLayout(hbox)

    def toggle_live(self):
        if self.live_btn.text() == 'Live Test':
            self.live_btn.setText('Stop')
            self.status_label.setText('Status: Live')
            self.status_icon.show()

            # Utilisez les valeurs actuelles des sliders pour les effets en direct
            threading.Thread(target=liveVoiceChanger, args=(
                self.mic, self.pitch_val, self.speed_val, self.volume_val)).start()
        else:
            # Arrêtez le traitement audio en direct ici
            self.live_btn.setText('Live Test')
            self.status_label.setText('Status:')
            self.status_icon.hide()

    def toggle_record(self):
        if self.record_btn.text() == 'Record':
            self.record_btn.setText('Stop')
            self.status_label.setText('Status: Recording')
            self.status_icon.show()
            thread = threading.Thread(target=self.record_sound)
            thread.start()
        else:
            self.record_btn.setText('Record')
            self.status_label.setText('Status:')
            self.status_icon.hide()

    def record_sound(self):
        # Générer un nom de fichier unique
        now = datetime.now()
        unique_filename = f"outputs/recording_{now.strftime('%Y%m%d%H%M%S')}.wav"

        # Enregistrement de l'audio
        self.isRecording = True
        mic = Input(mul=1)
        recording = Record(mic, filename=unique_filename, chnls=1)
        sleep(3)  # Record for 3 seconds
        recording.stop()
        self.isRecording = False
        print('Record saved')


        # Ajouter le nom de fichier à la liste
        self.recordingsList.addItem(unique_filename)
        self.save_recording_list(unique_filename)

    def toggle_play(self):
        if self.play_btn.text() == 'Play':
            self.play_btn.setText('Stop')
            self.status_label.setText('Status: Playing')
            self.status_icon.show()
            thread = threading.Thread(target=self.play_sound)
            thread.start()
        else:
            self.play_btn.setText('Play')
            self.status_label.setText('Status:')
            self.status_icon.hide()

    def play_sound(self):
        # Jouer l'audio sélectionné
        selected_item = self.recordingsList.currentItem()
        if selected_item:
            audio_path = selected_item.text()
            self.sound = AudioSegment.from_file(audio_path)
            play(self.sound)

    def update_pitch_value(self, value):
        self.pitch_val = value / 100.0  # Ajuster l'échelle pour pitch
        self.pitch_value_label.setText(str(value))
        # Pas d'application directe à self.sound ici

    def update_speed_value(self, value):
        self.speed_val = value / 10.0  # Ajuster l'échelle pour speed
        self.speed_value_label.setText(str(value))
        # Pas d'application directe à self.sound ici

    def update_volume_value(self, value):
        self.volume_val = value  # Ajuster l'échelle pour volume
        self.volume_value_label.setText(str(value))
        # Pas d'application directe à self.sound ici

    def save_audio(self):
        if self.sound is not None:
            exportModifiedSound(self.sound)
            self.status_label.setText('Status: Saved')

    # Audio manipulation functions
    def pitch(audio, pitchValue):
        new_frame_rate = int(audio.frame_rate * (pitchValue / 100.0))
        return audio._spawn(audio.raw_data, overrides={"frame_rate": new_frame_rate})

    def speed(audio, speedValue):
        return audio.speedup(playback_speed=speedValue)

    def volume(audio, volumeValue):
        return audio + volumeValue

    def exportModifiedSound(audio):
        audio.export("outputs/outputModified.wav", format="wav")

    def closeEvent(self, event):
        self.server.stop()
        self.server.shutdown()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VoiceChangerUI()
    ex.show()
    sys.exit(app.exec_())


