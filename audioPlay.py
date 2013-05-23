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

# Fade in at start, and out at end. Basically, we want to multiply by another function whose range is [0.0 to 1.0],
# that is shaped so that our samples are forced to be 0 at start and end. Non-zero start and end samples could
# lead to audible "clicking". See http://en.wikipedia.org/wiki/Window_function
# @note @note @note: We're using a Hanning window (with an "n"), not a Hamming window (with an "m"). The Hamming
# window doesnt' go to zero at beginning and end, just around 0.1.
samples = samples * numpy.hanning(len(samples))

# Pad with zeros at start and end.
padSeconds = 0.2
padWidth = int(padSeconds * samplingFrequency)
samples = numpy.pad(samples, (padWidth, padWidth), 'constant', constant_values=(0.0,))	# Requires NumPy 1.7+

totalSeconds = int(math.ceil(soundSeconds + 2 * padSeconds))

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
sound.play()

MILLISECONDS_PER_SECOND = 1000
pygame.time.delay(totalSeconds * MILLISECONDS_PER_SECOND)
# sound.stop()
