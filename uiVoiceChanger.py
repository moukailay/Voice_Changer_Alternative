import threading
from time import sleep

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider
from pydub.playback import play
from pyo import *

from logic import pitch, speed, volume, exportModifiedSound, recordSound, playRecordedSound, playModifiedSound, \
    liveVoiceChanger, preset1


class VoiceChangerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.liveVoiceChanger = None
        self.initUI()
        self.initAudio()

    def initUI(self):
        self.setWindowTitle('Voice Changer')
        self.setFixedSize(400, 300)

        # Boutons
        self.live_btn = QPushButton('Live Test', self)
        self.record_btn = QPushButton('Record', self)
        self.play_btn = QPushButton('Play', self)

        # Sliders
        self.pitch_slider = QSlider(Qt.Horizontal)
        self.speed_slider = QSlider(Qt.Horizontal)
        self.volume_slider = QSlider(Qt.Horizontal)
        self.setupSlider(self.pitch_slider, 50, 300, 100, 20)
        self.setupSlider(self.speed_slider, 10, 30, 10, 10)
        self.setupSlider(self.volume_slider, 0, 50, 0, 5)

        # Labels
        self.pitch_label = QLabel('Pitch:')
        self.speed_label = QLabel('Speed:')
        self.volume_label = QLabel('Volume:')
        self.pitch_value_label = QLabel(str(self.pitch_slider.value()))
        self.speed_value_label = QLabel(str(self.speed_slider.value()))
        self.volume_value_label = QLabel(str(self.volume_slider.value()))
        self.save_btn = QPushButton('Save Audio', self)
        self.status_label = QLabel('Status:')
        self.status_label.setStyleSheet("color: black")
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
            thread = threading.Thread(target=self.liveVoiceChanger)
            thread.start()
        else:
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
        self.isRecording = True
        mic = Input(mul=1)
        recording = Record(mic, filename=self.recordedSoundPath, chnls=1)
        sleep(3)  # Record for 3 seconds
        recording.stop()
        self.isRecording = False
        print('Record saved')

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
        if self.sound is not None:
            play(self.sound)

    def update_pitch_value(self, value):
        self.pitch_value_label.setText(str(value))
        if self.sound is not None:
            self.sound = pitch(self.sound, value / 100.0)

    def update_speed_value(self, value):
        self.speed_value_label.setText(str(value))
        if self.sound is not None:
            self.sound = speed(self.sound, value / 10.0)

    def update_volume_value(self, value):
        self.volume_value_label.setText(str(value))
        if self.sound is not None:
            self.sound = volume(self.sound, value)

    def save_audio(self):
        if self.sound is not None:
            exportModifiedSound(self.sound)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VoiceChangerUI()
    ex.show()
    sys.exit(app.exec_())


