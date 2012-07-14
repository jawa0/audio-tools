import numpy
import pyaudio
import sys

import pygame
import pygame.mixer

sampleRate = 44100
sampleFormat = pyaudio.paInt16
recordingChannels = 2
RECORD_SECONDS = 60

pygame.mixer.pre_init( channels = 1, frequency = sampleRate, size = -16 ) # must be signed on OS X
pygame.init()

p = pyaudio.PyAudio()

print 'PyAudio Devices:'
for di in range(p.get_device_count()):
	print ' ', di, p.get_device_info_by_index(di)['name']

print
print 'Using default input device:', p.get_default_input_device_info()['name']

stream = p.open(format = sampleFormat,
                channels = recordingChannels,
                rate = sampleRate,
                input = True)

print "* recording"

data = stream.read( RECORD_SECONDS * sampleRate )

print "* done"

stream.stop_stream()
stream.close()
p.terminate()


if 1 == recordingChannels:
	sampleType = numpy.int16
elif recordingChannels > 1:
	# column-vector of individual channels' samples. I.e. for stereo, each element of the sample array is
	# itself a 2x1 array.
	sampleType = numpy.dtype( (numpy.int16, (recordingChannels, 1)) )
	
interleavedSamples = numpy.frombuffer( data, dtype = sampleType )
leftSamples = numpy.ndarray.flatten( interleavedSamples[:,0] )
rightSamples = numpy.ndarray.flatten( interleavedSamples[:,1] )


sound = pygame.sndarray.make_sound( leftSamples )
sound.play(-1)
pygame.time.delay(1000 * RECORD_SECONDS)
sound.stop()
