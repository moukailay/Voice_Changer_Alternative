from pyo import *  # Importation de la bibliothèque pyo pour le traitement audio
from time import sleep  # Importation de la fonction sleep pour faire des pauses
import math  # Importation de la bibliothèque math pour des calculs mathématiques
from pydub import AudioSegment  # Importation d'AudioSegment pour manipuler des fichiers audio
from pydub.playback import play  # Importation de play pour jouer des fichiers audio
import pyaudio

recordedSoundPath = 'outputs/output.wav'  # Chemin du fichier audio enregistré
modifiedSoundPath = 'outputs/outputModified.wav'  # Chemin du fichier audio modifié
s = Server().boot()  # Initialisation du serveur
mic = Input(mul=0.2)  # Création d'un objet Input pour récupérer le son du micro avec un multiplicateur d'amplitude
isRecording = False  # Flag pour vérifier si l'enregistrement est en cours
s.start()  # Démarrage du serveur
global modifiedSound  # Variable globale pour le son modifié


# Fonction pour changer la voix en temps réel
def liveVoiceChanger(input_stream):
    x = Harmonizer(input_stream, transpo=5)  # Harmoniseur pour modifier le ton
    x2 = Delay(x, delay=0.002, feedback=0.1)  # Délai pour ajouter un effet d'écho
    return Biquad(x2, freq=40000, q=20000, type=0)  # Filtre Biquad pour modifier le timbre


# Fonction pour jouer le son enregistré
def playRecordedSound():
    audio = AudioSegment.from_file(recordedSoundPath, format="wav")  # Chargement du fichier audio
    play(audio)  # Jouer le son


# Fonction pour jouer le son modifié
def playModifiedSound():
    audio = AudioSegment.from_file(modifiedSoundPath, format="wav")  # Chargement du fichier audio modifié
    play(audio)  # Jouer le son modifié


# Fonction pour enregistrer le son
def recordSound(RecordingTime):
    print('Recording started')  # Affichage de début d'enregistrement
    isRecording = True
    mic = Input(mul=1)  # Création d'un objet Input avec amplitude maximale
    recording = Record(mic, filename="outputs/output.wav", chnls=1)  # Enregistrement du son
    sleep(RecordingTime)  # Pause pendant la durée d'enregistrement
    recording.stop()  # Arrêt de l'enregistrement
    isRecording = False
    print('Record saved')  # Affichage de fin d'enregistrement


# Fonction pour modifier le ton du son
def pitch(audio, pitchValue):
    new_frame_rate = int(audio.frame_rate * pitchValue)  # Calcul du nouveau taux d'échantillonnage
    pitch_shifted_audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": new_frame_rate})  # Modification du son avec le nouveau taux
    return pitch_shifted_audio  # Retour du son modifié


# Fonction pour changer la vitesse du son
def speed(audio, speedValue):
    return audio.speedup(playback_speed=speedValue)  # Modification de la vitesse du son


# Fonction pour changer le volume du son
def volume(audio, volumeValue):
    return audio + volumeValue  # Augmentation ou diminution du volume


# Preset pour appliquer une série de modifications sur le son
def preset1(audio):
    x = pitch(audio, 1.5)  # Modification du ton
    x1 = speed(x, 1.7)  # Modification de la vitesse
    play(x1)  # Jouer le son modifié


# Fonction pour exporter le son modifié
def exportModifiedSound(audio):
    audio.export("outputs/outputModified.wav", format="wav")  # Exportation du son modifié


    # Exemple d'utilisation du script pour enregistrer et modifier un son


recordSound(3)  # Enregistrement d'un son pendant 3 secondes (décommenter pour utiliser)

sound = AudioSegment.from_file(recordedSoundPath, format="wav")  # Chargement du son enregistré

# Application d'une modification de ton et lecture du son
x = pitch(sound, 2)  # Modification du ton
play(x)  # Lecture du son modifié

preset1(sound)  # Application d'un preset de modifications sur le son (décommenter pour utiliser)

# Section pour le traitement de la voix en direct
x1 = liveVoiceChanger(mic)  # Application du changeur de voix en direct
x1.out()  # Sortie audio du résultat (décommenter pour utiliser)

# Fin du script

# Explications supplémentaires :
# Ce script est conçu pour enregistrer, modifier et jouer des sons en temps réel ou à partir d'un fichier.
# Il utilise la bibliothèque pyo pour la manipulation audio en temps réel et pydub pour le traitement de fichiers audio.
# Les fonctions fournies permettent d'enregistrer un son, de le modifier (changer le ton, la vitesse, le volume),
# et de jouer le son original ou modifié.
# Il est également possible de changer la voix en direct en utilisant la fonction 'liveVoiceChanger'.
# Ce script peut être utilisé pour des applications de traitement audio basiques, telles que la création d'effets sonores,
# la modification de fichiers audio enregistrés ou encore la manipulation de la voix en temps réel.
