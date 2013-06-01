import Image
from itertools import izip_longest
import math
import numpy
from scipy.io import wavfile
import sys


def main():
	wavFilename = sys.argv[1]
	samplingFrequency, samples = wavfile.read(wavFilename)
	
	# print samples.shape

	print 'Sampling Frequency:', samplingFrequency, 'Hz'
	print 'Number of Samples: ', len(samples)
	print 'Sample Data Type:', samples.dtype

	scale = max(numpy.iinfo(samples.dtype).max, -numpy.iinfo(samples.dtype).min)
	normalizedSamples = (1.0 / scale) * samples

	# print normalizedSamples.shape

	windowDurationSeconds = 0.1
	samplesPerWindow = int(math.floor(windowDurationSeconds * samplingFrequency))
	numUniqueFrequencySamples = 1 + samplesPerWindow // 2

	print
	print 'Gap between frequency samples:', samplingFrequency / samplesPerWindow

	startingIndicesOfWindowsWithinSampleArray = range(0, len(normalizedSamples), samplesPerWindow)
	windowCount = len(startingIndicesOfWindowsWithinSampleArray)

	A = numpy.empty((numUniqueFrequencySamples, windowCount))

	for iStart in startingIndicesOfWindowsWithinSampleArray:
		windowSamples = normalizedSamples[iStart : iStart + samplesPerWindow]
		if len(windowSamples) < samplesPerWindow:	# For the last one?
			leftPadSize = samplesPerWindow - len(windowSamples)
			rightPadSize = 0

			# print (leftPadSize, rightPadSize)

			# @note @bug: Numpy throws an exception if I try to pad with size 0 on either
			# the left or the right. This is too bad, because I only want to pad one side
			# So, we'll do this the less convenient way...

			# windowSamples = numpy.pad(windowSamples, (leftPadSize, rightPadSize), 'constant', constant_values=(0,))
			windowSamples = padLeft(windowSamples, leftPadSize)

		# print windowSamples.shape
		
		frequencySamples = numpy.fft.rfft(windowSamples)		# Each one is a complex number
		assert(len(frequencySamples) == numUniqueFrequencySamples)

		amplitudeSamples = numpy.absolute(frequencySamples)		# Each one is a real number

		indexOfWindow = iStart // samplesPerWindow
		A[:,indexOfWindow] = amplitudeSamples

	# Currently, the array has float values in the range [0.0, maxAmplitude]
	# We want to scale these to integers in the range [0, 255] so we can output the
	# array as an image.

	print '\nSpectrogram array:'
	print 'min amplitude =', numpy.min(A), 'max amplitude =', numpy.max(A)

	A = ((256 - 1e-6) / numpy.max(A)) * A

	print '\nRescaling to range [0, 256):'
	print 'min amplitude =', numpy.min(A), 'max amplitude =', numpy.max(A)

	A = A.astype(numpy.uint8)

	print '\nConverting to integers to range [0, 256):'
	print 'min amplitude =', numpy.min(A), 'max amplitude =', numpy.max(A)

	# Need to do some flipping of the array...
	# In a spectrogram, we want to show higher pitches (frequencies) above lower ones, even though
	# y is increasing downwards, so we need to flip vertically.

	im = Image.fromarray(numpy.flipud(A))
	print im.size
	im.save('spectrogram.png')


def padLeft(a, padSize):
	# NOTES:
	# >>> import numpy as np
	# >>> a = np.array([1, 2, 3])
	# >>> z = np.zeros(4)
	# >>> np.hstack((a,z))
	# array([ 1.,  2.,  3.,  0.,  0.,  0.,  0.])
	# >>> np.hstack((z,a))
	# array([ 0.,  0.,  0.,  0.,  1.,  2.,  3.])
	return numpy.hstack((numpy.zeros(padSize), a))


if __name__ == '__main__':
	main()
