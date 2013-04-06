import math
import numpy
import pygame
import pygame.mixer


samplingFrequency = 44100	# Hz == samples per second


def sinSamples(frequency, seconds):
	"""Returns a discrete-time sine-wave as a NumPy array of signed float samples in the range -1.0 to 1.0."""
	numSamples = int( math.ceil(seconds * samplingFrequency) )
	xs = (2.0 * frequency * math.pi / samplingFrequency) * numpy.arange( numSamples )
	samples = numpy.sin( xs )
	return samples


soundSeconds = 4
samples = sinSamples(440, soundSeconds)

# Pre-initialize the PyGame Mixer before the general PyGame init, so we can set the expected sample size.
# We need to set the sample size, because samples need to be signed-ints on Mac OS X. To denote this, we
# pass in a negative value for the sample size.

pygame.mixer.pre_init( channels = 1, frequency = samplingFrequency, size = -16 )
pygame.init()

# The signal returned by our signal-generating function varies between -1.0 and 1.0. We need to scale
# these values to fit into a signed 16-bit integer. So, multiply by the largest 16-bit int. Note that this
# means that we're not using one level: -32768 so we lose a tiny bit of dynamic range (one part in 65536).
# This is because a signed 16-bit int can represent the range [-32768, 32767] but we're only using [-32767, 32767]
# There's not a great reason why I'm doing this. I just did it to make the code simpler.

INT16_LARGEST = 32767
samples = INT16_LARGEST * samples
samples = samples.astype( numpy.int16 )

sound = pygame.sndarray.make_sound( samples )
sound.play(-1)

MILLISECONDS_PER_SECOND = 1000
pygame.time.delay(soundSeconds * MILLISECONDS_PER_SECOND)
sound.stop()
