import pyaudio
import wave
from math import sin, pi
import struct
from selcald.binsize import SelcalParams


selcal_params = SelcalParams()


def playwav(fn, chunksize=1024):
    wf = wave.open(fn, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(chunksize)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(chunksize)

    stream.stop_stream()
    stream.close()
    p.terminate()


def genfreq(freqencies, duration, amplitudes=None, samprate=8000):
    amplitudes = amplitudes or [1]*len(freqencies)
    amplitudes = [x*2**15-1 for x in amplitudes]
    n = 0
    while n < samprate*duration:
        samp = 0
        for a,f in zip(amplitudes, freqencies):
            samp += a*(sin((2*pi)/(samprate/f)*n))
        yield struct.pack('h', int(samp/len(freqencies)))
        n += 1


def buffer(samp, chunksize=1024):
    data = b''.join([next(samp) for i in range(chunksize)])
    while len(data)>0:
        yield data
        data = b''.join([next(samp) for i in range(chunksize)])


def playsound(samp, samprate=8000):
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(2), channels=1,
                    rate=samprate, output=True)

    for data in samp:
        stream.write(data)

    stream.stop_stream()
    stream.close()
    p.terminate()


def playSELCALTone(tone, duration, amplitude, samprate=8000):
    freq = selcal_params.selcal_tones[tone]
    b = buffer(genfreq(freq, duration, amplitude, samprate))
    playsound(b)


