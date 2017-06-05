from tkinter import *
import wave
import pyaudio

running = True  # Global flag
CHUNK = 1024
wf = wave.open('playme.wav', 'rb')

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# open stream (2)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

data = wf.readframes(CHUNK)


def scanning():
    global data
    if running:  # Only do this if the Stop button has not been clicked
        stream.write(data)
        data = wf.readframes(CHUNK)
        if data == b'':
            print('rewind')
            wf.rewind()

    # After 1 second, call scanning again (create a recursive loop)
    root.after(1000, scanning)


def start():
    """Enable scanning by setting the global flag to True."""
    global running
    running = True


def stop():
    """Stop scanning by setting the global flag to False."""
    global running
    running = False


root = Tk()
root.title("Title")
root.geometry("500x500")

app = Frame(root)
app.grid()

start = Button(app, text="Start Scan", command=start)
stop = Button(app, text="Stop", command=stop)

start.grid()
stop.grid()

root.after(1000, scanning)  # After 1 second, call scanning
root.mainloop()
