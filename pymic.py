import numpy
import pyaudio
import analyse

pyaud = pyaudio.PyAudio()

stream = pyaud.open(
		format = pyaudio.paInt16,
		channels = 1,
		rate = 44100,
		input_device_index = 0,
		input = True)

while True:
	rawsamps = stream.read(1024)
	samps = numpy.fromstring(rawsamps, dtype=numpy.int16)
	print analyse.loudness(samps), analyse.musical_detect_pitch(samps)
