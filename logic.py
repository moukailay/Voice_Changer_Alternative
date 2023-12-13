from pyo import *
from time import sleep
import math
from pydub import AudioSegment
from pydub.playback import play


recordedSoundPath = 'outputs/output.wav'
modifiedSoundPath = 'outputs/outputModified.wav'
s = Server().boot() # On démarre le serveur
mic = Input(mul=0.2) # On crée un objet Input pour récupérer le son du micro
isRecording = False
s.start()
global modifiedSound


def liveVoiceChanger(input_stream, pitch_val, delay_val, feedback_val, freq_val, q_val):
    x = Harmonizer(input_stream, transpo=pitch_val)
    x2 = Delay(x, delay=delay_val, feedback=feedback_val)
    return Biquad(x2, freq=freq_val, q=q_val, type=0)

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
def pitch(audio, pitchValue):
    new_frame_rate = int(audio.frame_rate * pitchValue)
    pitch_shifted_audio = audio._spawn(audio.raw_data, overrides={
    "frame_rate": new_frame_rate})
    return pitch_shifted_audio
    
def speed(audio, speedValue):
    return audio.speedup(playback_speed=speedValue) 

def volume(audio, volumeValue):
        return audio + volumeValue   

def preset1(audio):
    x = pitch(audio, 1.5)
    x1 = speed(x, 1.7)
    play(x1)
    
# sauvegarder le son
def exportModifiedSound(audio):
    audio.export("outputs/outputModified.wav", format="wav")

# Si il n'y a aucun son enregistrer enlever ca de commentaire
# 3 = nombre de secondes

#recordSound(3)

sound = AudioSegment.from_file(recordedSoundPath, format="wav")

# on affecte la valeur de return de la fonction pour pouvoir jouer le audio
x = pitch(sound, 2)
play(x)

#preset1(sound)

# live ->

#x1 = liveVoiceChanger(mic)
#x1.out()









    