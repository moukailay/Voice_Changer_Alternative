import tkinter as tk
from tkinter import ttk
from tkinter.constants import DISABLED, NORMAL
import pyaudio


class App:
    def __init__(self, master):
        self.master = master
        self.racine = tk.Tk()
        self.image_start = tk.PhotoImage(file="./images/Start-Button.png")
        self.image_end = tk.PhotoImage(file="./images/Pause-Button.png")
        self.p = pyaudio.PyAudio()
        self.mic = self.p.get_default_input_device_info()
        self.bouton_enregistrement = tk.Button(self.racine,
                                               image=self.image_start,
                                               command=lambda: self.start_recording_thread(self.mic['index']),
                                               state=NORMAL)
        self.bouton_arret_enregistrement = tk.Button(self.racine,
                                                     text="Fin de l'enregistrement",
                                                     command=self.stop_recording,
                                                     state=DISABLED)
        self.bouton_quitter = tk.Button(self.racine,
                                        text="Quitter",
                                        command=self.quitter,
                                        state=NORMAL)
        self.progress = ttk.Progressbar(self.racine,
                                        length=300,
                                        mode='determinate')
        self.bouton_joue_enregistrement = tk.Button(self.racine,
                                                    text="Jouer l'enregistrement",
                                                    command=self.play_audio_in_thread,
                                                    state=DISABLED)

        self.bouton_enregistrement.grid(row=0, column=0, padx=(0, 10))
        self.bouton_arret_enregistrement.grid(row=2, column=0, padx=(0, 10))
        self.bouton_joue_enregistrement.grid(row=3, column=0, padx=(0, 10))
        self.progress.grid(row=3, column=1, padx=(0, 10))
        self.bouton_quitter.grid(row=4, column=0, padx=(0, 10))