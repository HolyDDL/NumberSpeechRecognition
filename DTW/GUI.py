# -----------------------------------------
# @Description: This file uses tkinter to make a GUI
# @Author: Yiwei Ren.
# @Date: 十一月 01, 2023, 星期三 14:45:55
# @Copyright (c) 2023 Yiwei Ren. All rights reserved.
# -----------------------------------------


import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pyaudio
import wave
from DTW import DTW
import os

globalfont = ('Times New Roman', 20)
global pattern_path
pattern_path = None

root = tk.Tk()
root.title("Speech Recognization")

window_width = 600
window_height = 250

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

root.geometry("%dx%d+%d+%d" % (window_width, window_height, position_right, position_top))

# choose file label
label = tk.Label(root, text='Choose root path of patterns', font=globalfont)
label.pack()

def select_directory():
    global pattern_path 
    pattern_path = filedialog.askdirectory()
    label.config(text=f'Choosed root path is: {pattern_path}', font=globalfont)

# choose file button
select_button = tk.Button(root, text="Choose", command=select_directory, font=globalfont)
select_button.pack()

# blank sapce
blank_space = tk.Label(root, text="", height=2)
blank_space.pack()

# recognization parogress bar
progress = ttk.Progressbar(root, length=400, mode='determinate')
progress.pack()

# recongnization label
progresslabel = tk.Label(root, text='Press button to record', font=globalfont)
progresslabel.pack()

def record_audio():
    global pattern_path
    if pattern_path:
        folder = os.path.exists('temp')
        if not folder:                 
            os.mkdir('temp')
        WAVE_OUTPUT_FILENAME = os.path.join('temp','temp.wav')
        progresslabel.config(text='Recording...')
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 8000
        RECORD_SECONDS = 2
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
            progress['value'] = (i+1) / (RATE / CHUNK * RECORD_SECONDS) * 100
            root.update_idletasks()

        stream.stop_stream()
        stream.close()
        p.terminate()
        
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        progresslabel.config(text=f'Recognizing...')
        recognizer = DTW(pattern_root=pattern_path)
        predict_num = recognizer(WAVE_OUTPUT_FILENAME)
        progresslabel.config(text=f'Predicted number is: {predict_num}')
        
        def del_files(path):
            for i in os.listdir(path):
                if os.path.isdir(os.path.join(path,i)):
                    del_files(os.path.join(path,i))
                os.remove(os.path.join(path,i))
        del_files('temp')
    else:
        messagebox.showwarning('Warning!', 'Did not Choose patterns!')

record_button = tk.Button(root, text='Record', command=record_audio, font=globalfont)
record_button.pack()
root.mainloop()
