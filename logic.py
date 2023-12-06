from pyo import *
from time import sleep
import math
from pydub import AudioSegment
from pydub.playback import play

recordedSoundPath = 'outputs/output.wav'
modifiedSoundPath = 'outputs/outputModified.wav'
s = Server().boot()
mic = Input(mul=0.5)
isRecording = False
s.start()
global modifiedSound

def playRecordedSound():
     audio = AudioSegment.from_file(recordedSoundPath, format="wav")
     play(audio)

def playModifiedSound():
    audio = AudioSegment.from_file(modifiedSoundPath, format="wav")
    play(audio)
    
def recordSound(RecordingTime):
    print('Recording started')
    isRecording = True
    # mul is l'amplitude
    mic = Input(mul=1)
    # save the recording in outputs folder
    recording = Record(mic, filename="outputs/output.wav", chnls=1)
    sleep(RecordingTime)
    recording.stop()
    isRecording = False
    print('Record saved')
    
# change voice pitch. Use values between ~0.5 to ~2.5
def pitch(pitchValue):
    global modifiedSound
    audio = AudioSegment.from_file(recordedSoundPath, format="wav")
    new_frame_rate = int(audio.frame_rate * pitchValue)
    pitch_shifted_audio = audio._spawn(audio.raw_data, overrides={
    "frame_rate": new_frame_rate})
    modifiedSound = pitch_shifted_audio
    exportModifiedSound()
    
def speed(speedValue):
    global modifiedSound
    audio = AudioSegment.from_file(recordedSoundPath, format="wav")
    audio1 = audio.speedup(playback_speed=speedValue)
    modifiedSound = audio1
    audio.export("outputs/outputModified.wav", format="wav")


def exportModifiedSound():
    modifiedSound.export("outputs/outputModified.wav", format="wav")
     
#recordSound(3)
#speed(4)
#play(modifiedSound)







    