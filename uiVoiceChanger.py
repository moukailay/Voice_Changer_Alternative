import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class VoiceChangerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Voice Changer')
        self.setFixedSize(400, 300)

        self.live_btn = QPushButton('Live Test', self)
        self.record_btn = QPushButton('Record', self)
        self.play_btn = QPushButton('Play', self)
        self.pitch_slider = QSlider(Qt.Horizontal) 
        self.speed_slider = QSlider(Qt.Horizontal)
        self.volume_slider = QSlider(Qt.Horizontal) 
        self.pitch_slider.setRange(50, 300)
        self.pitch_slider.setValue(100)
        self.speed_slider.setRange(1,3)
        self.volume_slider.setRange(0, 50)
        self.pitch_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.volume_slider.setTickPosition(QSlider.TicksBelow)
        
        self.pitch_slider.setTickInterval(20)
        self.speed_slider.setTickInterval(30)
        self.volume_slider.setTickInterval(5)
        
        self.pitch_label = QLabel('Pitch:')
        self.speed_label = QLabel('Speed:')
        self.volume_label = QLabel('Volume:')
        self.save_btn = QPushButton('Save Audio', self)
        self.status_label = QLabel('Status:')
        self.status_label.setStyleSheet("color: black")
        self.status_icon = QLabel(self)
        self.status_icon.setPixmap(QIcon('red_circle_icon.png').pixmap(20, 20))
        self.status_icon.hide()

        vbox = QVBoxLayout()

        vbox.addWidget(self.live_btn)
        vbox.addWidget(self.record_btn)
        vbox.addWidget(self.play_btn)

        hbox_pitch = QHBoxLayout()
        hbox_pitch.addWidget(self.pitch_label)
        hbox_pitch.addWidget(self.pitch_slider)
        self.pitch_value_label = QLabel(str(self.pitch_slider.value()))
        hbox_pitch.addWidget(self.pitch_value_label)
        vbox.addLayout(hbox_pitch)

        hbox_speed = QHBoxLayout()
        hbox_speed.addWidget(self.speed_label)
        hbox_speed.addWidget(self.speed_slider)
        self.speed_value_label = QLabel(str(self.speed_slider.value()))
        hbox_speed.addWidget(self.speed_value_label)
        vbox.addLayout(hbox_speed)

        hbox_volume = QHBoxLayout()
        hbox_volume.addWidget(self.volume_label)
        hbox_volume.addWidget(self.volume_slider)
        self.volume_value_label = QLabel(str(self.volume_slider.value()))
        hbox_volume.addWidget(self.volume_value_label)
        vbox.addLayout(hbox_volume)

        vbox.addWidget(self.save_btn)

        hbox_status = QHBoxLayout()
        hbox_status.addWidget(self.status_label)
        hbox_status.addWidget(self.status_icon)
        vbox.addLayout(hbox_status)

        self.setLayout(vbox)
        
        # Bouton onClick
        self.live_btn.clicked.connect(self.toggle_live)
        self.record_btn.clicked.connect(self.toggle_record)
        self.play_btn.clicked.connect(self.toggle_play)  

        #Changer valeurs slider
        self.pitch_slider.valueChanged.connect(self.update_pitch_value)
        self.speed_slider.valueChanged.connect(self.update_speed_value)
        self.volume_slider.valueChanged.connect(self.update_volume_value)

    def toggle_live(self):
        if self.live_btn.text() == 'Live Test':
            self.live_btn.setText('Stop Live')
            self.status_label.setText('Status: Live Testing')
            self.status_icon.show()
        else:
            self.live_btn.setText('Live Test')
            self.status_label.setText('Status:')
            self.status_icon.hide()

    def toggle_record(self):
        if self.record_btn.text() == 'Record':
            self.record_btn.setText('Stop')
            self.status_label.setText('Status: Recording')
            self.status_icon.show()
        else:
            self.record_btn.setText('Record')
            self.status_label.setText('Status:')
            self.status_icon.hide()

    def toggle_play(self):
        if self.play_btn.text() == 'Play':
            self.play_btn.setText('Stop')
            self.status_label.setText('Status: Playing')
            self.status_icon.show()
        else:
            self.play_btn.setText('Play')
            self.status_label.setText('Status:')
            self.status_icon.hide()

    def update_pitch_value(self, value):
        self.pitch_value_label.setText(str(value))

    def update_speed_value(self, value):
        self.speed_value_label.setText(str(value))

    def update_volume_value(self, value):
        self.volume_value_label.setText(str(value))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VoiceChangerUI()
    ex.show()
    sys.exit(app.exec_())
