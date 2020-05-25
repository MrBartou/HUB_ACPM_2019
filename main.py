import pyaudio
from tkinter import *
import wave
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile as wf
from scipy import fft

sons =["test.wav"]

def record():
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 10
    WAVE_OUTPUT_FILENAME = "test.wav"
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
    print ("Enregistrement en cours...")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print ("Fin d'enregistrement")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

def traitement(son):
    sampFreq, snd = wf.read(son)
    snd = snd / (2.**15)
    shap = snd.shape[0]
    try:
        s1 = snd[:,0]
    except:
        s1 = snd
    timeArray = np.arange(0, shap, 1)
    timeArray = timeArray / sampFreq
    timeArray = timeArray * 1000
    plt.plot(timeArray, s1, color='b')
    plt.ylabel('Amplitude')
    plt.xlabel('Temps (ms)')
    plt.show()
    n = len(s1)
    p = fft(s1)
    nUniquePts = int(np.ceil((n+1)/2.0))
    p = p[0:nUniquePts]
    p = abs(p)
    p = p / float(n)
    p = p**2
    if n % 2 > 0:
        p[1:len(p)] = p[1:len(p)] * 2
    else:
        p[1:len(p) -1] = p[1:len(p) - 1] * 2
    freqArray = np.arange(0, nUniquePts, 1.0) * (sampFreq / n)
    plt.plot(freqArray/50, 10*np.log10(p), color='r')
    plt.xlabel('Frequence (kHz)')
    plt.ylabel('Puissance (dB)')
    plt.show()
    song_value = np.sqrt(np.mean(s1**2))
    song_value = round(song_value,4)
    return song_value

def drawcircle(canv, x, y, rad, back):
    canv.create_oval(x - rad, y - rad, x + rad, y + rad, width = 0, fill = back)

def interpret_message(message):
    window = Tk()
    window.title("ACPM")
    window.geometry("800x600")
    position = 4
    if (message == "urgent"):
        back = 'red'
    elif (message == "klaxon"):
        back = 'yellow'
    elif (message == "ambiant"):
        back = 'green'

    if (position == 0):
        x = 50
        y = 300
    elif (position == 1):
        x = 133
        y = 300
    elif (position == 2):
        x = 275
        y = 300
    elif (position == 3):
        x = 500
        y = 300
    elif (position == 4):
        x = 644
        y = 300
    elif (position == 5):
        x = 735
        y = 300
    canvas = Canvas(window, width = 800, height = 600, bg = 'white')
    photo = PhotoImage(file = 'voiture.png')
    canvas.create_image(400, 300, image = photo)
    canvas.pack()
    drawcircle(canvas, x, y, 20, back)
    window.mainloop()

for i in range(len(sons)):
    record()
    song_value = traitement(sons[i])
    if song_value == 0.2076:
        message = "urgent"
        interpret_message(message)
    if song_value == 0.1925:
        message = "urgent"
        interpret_message(message)
    if song_value == 0.2394:
        message = "klaxon"
        interpret_message(message)
