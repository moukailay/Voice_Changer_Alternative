import os
from tkinter import *
from tkinter import ttk
import speech_recognition as sr
import pyaudio
import wave
import tkinter as tk
import threading
from elevenlabs import voices, generate, play, Voice, VoiceSettings, set_api_key

set_api_key("9067b87bb61456e68b587b6c037b1cd9")
wf = None
stream = None
chunk = 1024  # Nombre de frames par bloc
sample_format = pyaudio.paInt16  # 16 bits par échantillon
channels = 1  # Un canal pour l'enregistrement mono
fs = 44100  # Fréquence d'échantillonnage (en Hz)
p = pyaudio.PyAudio()
en_cours = False
racine = tk.Tk()
bouton_joue_enregistrement = None
progress = ttk.Progressbar(racine, length=300, mode='determinate')
image_start = tk.PhotoImage(file="./images/Start-Button.png")
recording_thread = None
audio_thread = None
can_read_audio = False


def get_default_mic():
    default_mic = p.get_default_input_device_info()
    return default_mic


def play_sound():
    global wf, stream, en_cours
    if not en_cours:
        en_cours = True
        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )
        data = wf.readframes(chunk)

        while data:
            stream.write(data)
            data = wf.readframes(chunk)
        stream.stop_stream()
    else:
        print("Vous ne pouvez pas jouer un son quand il y a un enregistrement en cours.")


def audio_file_exists():
    global bouton_joue_enregistrement
    print(os.path.isfile("enregistrement.wav"))
    if os.path.isfile("enregistrement.wav"):
        bouton_joue_enregistrement.config(state=tk.NORMAL)
    else:
        bouton_joue_enregistrement.config(state=tk.DISABLED)


def update_progress():
    global stream, wf, progress, en_cours
    progress['value'] = wf.tell() / wf.getnframes() * 100  # Met à jour la barre de progression avec la position de la musique
    if wf.tell() < wf.getnframes():
        racine.after(100, update_progress)  # Appelle la fonction après 100 millisecondes
    else:
        print("Fin de la lecture")
        progress['value'] = 0  # Met à 100% lorsque le son est terminé
        stream.stop_stream()
        en_cours = False


def play_audio_in_thread():
    global audio_thread, wf, en_cours
    wf = wave.open("enregistrement.wav", 'rb')
    audio_thread = threading.Thread(target=play_sound)
    audio_thread.start()
    update_progress()


def graphic_interface():
    global progress, en_cours, bouton_joue_enregistrement
    mic = get_default_mic()
    bouton_enregistrement = tk.Button(racine, image=image_start, command=lambda: start_recording_thread(mic['index']))
    bouton_arret_enregistrement = tk.Button(racine, text="Fin de l'enregistrement", command=stop_recording)
    bouton_joue_enregistrement = tk.Button(racine, text="Jouer Enregistrement", command=play_audio_in_thread,
                                           state=tk.DISABLED)
    voice_menu = OptionMenu(racine, selected_voice, *data['name'])
    transcribe_button = tk.Button(racine, text="Jouer Audio AI", command=play_audio)
    label_stability = tk.Label(racine, text="Stabilité : ")
    label_similarity = tk.Label(racine, text="Similarité : ")
    label_style = tk.Label(racine, text="Style : ")

    def quitter():
        if not en_cours:
            racine.quit()
            racine.destroy()
            exit()
        else:
            print("Vous ne pouvez pas quitter l'application quand il y a un enregistrement en cours.")

    bouton_quitter = tk.Button(racine, text="Quitter", command=quitter)

    bouton_enregistrement.grid(row=0, column=0, padx=(0, 10))
    bouton_arret_enregistrement.grid(row=2, column=0, padx=(0, 10))
    bouton_joue_enregistrement.grid(row=3, column=0, padx=(0, 10))
    progress.grid(row=3, column=1, padx=(0, 10))
    voice_menu.grid(row=5, column=0, padx=(0, 10))
    voice_menu.config(width=20)
    slider_stability.grid(row=6, column=1, padx=(0, 10))
    slider_similarity.grid(row=7, column=1, padx=(0, 10))
    slider_style.grid(row=8, column=1, padx=(0, 10))
    label_stability.grid(row=6, column=0, padx=(0, 10))
    label_similarity.grid(row=7, column=0, padx=(0, 10))
    label_style.grid(row=8, column=0, padx=(0, 10))
    transcribe_button.grid(row=9, column=0, padx=(0, 10))
    bouton_quitter.grid(row=10, column=0, padx=(0, 10))
    racine.mainloop()


def start_recording_thread(microphone_index):
    global recording_thread
    recording_thread = threading.Thread(target=record_audio, args=(microphone_index,))
    recording_thread.start()


def stop_recording():
    global en_cours, recording_thread
    try:
        en_cours = False
        if recording_thread.is_alive():
            recording_thread.join()
            recording_thread = None
            audio_file_exists()
    except AttributeError:
        print("Vous ne pouvez pas arêter un enregistrement quand il n'y a pas d'enregistrement.")


def record_audio(microphone_index):
    global en_cours
    if not en_cours:
        en_cours = True
        print("Enregistrement en cours...")
        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True,
                        input_device_index=microphone_index)
        frames = []
        try:
            while en_cours:
                data = stream.read(chunk)
                frames.append(data)
        except KeyboardInterrupt:
            pass
        stream.stop_stream()
        print("Enregistrement terminé !")
        save_audio(frames)
    else:
        print("Vous ne pouvez pas partir un enregistrement quand il y a déjà un enregistrement en cours.")


def save_audio(frames):
    global wf, can_read_audio
    wf = wave.open('enregistrement.wav', 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

### Lou

voices_list = voices()

data = {
    'name': [voice.name for voice in voices_list],
}

selected_voice = tk.StringVar()
selected_voice.set(voices_list[0].name)
slider_stability = ttk.Scale(
    racine,
    from_=0,
    to=1,
    orient='horizontal',
)
slider_similarity = ttk.Scale(
    racine,
    from_=0,
    to=1,
    orient='horizontal',
)
slider_style = ttk.Scale(
    racine,
    from_=0,
    to=1,
    orient='horizontal',
)

def transcribe_audio():
    global can_read_audio
    if can_read_audio:
        r = sr.Recognizer()
        with sr.AudioFile('enregistrement.wav') as source:
            audio = r.record(source)
        try:
            text = r.recognize_google(audio, language="fr-FR")
            print("Vous avez dit: " + text)
            return text
        except sr.UnknownValueError:
            print("Une erreur est survenue")
        except sr.RequestError as e:
            print("Une erreur est survenue")
    else:
        print("Vous ne pouvez pas transcrire un enregistrement quand il n'y a pas d'enregistrement.")

def get_voice_id():
    for voice in voices_list:
        if voice.name == selected_voice.get():
            return voice.voice_id

def play_audio():
    stability_value = float("%.2f" % slider_stability.get())
    similarity_value = float("%.2f" % slider_similarity.get())
    style_value = float("%.2f" % slider_style.get())

    audio = generate(
        text=transcribe_audio(),
        voice=Voice(
            voice_id=get_voice_id(),
            settings=VoiceSettings(
                stability=stability_value,
                similarity_boost=similarity_value,
                style=style_value,
                use_speaker_boost=True
            ),
        ),
        model="eleven_multilingual_v2"
    )
    play(audio)

graphic_interface()