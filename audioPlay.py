import math
import numpy
import pygame
import pygame.mixer

fs = 44100

def sinSamples(frequency, seconds):
	"""Returns numpy array of signed samples in the range -1.0 to 1.0."""
	numSamples = int( math.ceil(seconds * fs) )
	xs = (2.0 * frequency * math.pi / fs) * numpy.arange( numSamples )
	samples = numpy.sin( xs )
	return samples

soundSeconds = 4
samples = sinSamples(440, soundSeconds)

pygame.mixer.pre_init( channels = 1, frequency = fs, size = -16 ) # must be signed on OS X
pygame.init()

samples = 32767 * samples
samples = samples.astype( numpy.int16 )

sound = pygame.sndarray.make_sound( samples )
sound.play(-1)
pygame.time.delay(1000 * soundSeconds)
sound.stop()
