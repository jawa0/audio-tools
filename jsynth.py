import math
import numpy
import string
import struct
import sys
import wave

# USAGE: python jsynth.py song.txt out.wav

# @todo notes change abruptly from one sample to the next, causing cliks and pops.
# Need to multiply by a windowing function (envelope) to bring amplitude down to 0
# near the end of a note.

def semisOffsetFromC0(noteName):
	"""Given a 2 or 3 character long note name like "C3" or "E#4" or "Db3", return
	an integer denoting the distance in semitones from C0."""
	
	nameToSemitone  = {'C':0, 'C#':1, 'Db':1, 'D':2, 'Eb':3, 'D#':3, 'E':4, 'F':5, 'F#':6, 'Gb':6, 'G':7, 'G#':8, 'Ab':8, 'A':9, 'A#':10, 'Bb':10, 'B':11}
	
	if len(noteName) == 2:
		semi = nameToSemitone[noteName[0]]
		octave = int(noteName[1])
	elif len(noteName) == 3:
		semi = nameToSemitone[noteName[:2]]
		octave = int(noteName[2])

	return 12 * octave + semi
	
def semisDifference(firstNote, secondNote):
	"""Return a signed number denoting how many semitones secondNote is away from firstNote.
	E.g. semisDifference('C4', 'A4') returns 9. semisDifference('C4', 'C3') returns -12."""
	
	return semisOffsetFromC0(secondNote) - semisOffsetFromC0(firstNote)
	
def pitchFromOffsetToA4(numSemitones):
	"""Return a frequency in Hz for the note that is numSemitones semitones away from
	A4 (440 Hz). Assume twelve-tone equal temperament. 
	See http://en.wikipedia.org/wiki/Piano_key_frequencies"""
	
	return 440.0 * 2.0 ** (numSemitones / 12.0)

def pitch( noteName ):
	"""Return the frequency in Hz for the named note. E.g. pitch('A4') return 440.0"""
	offsetFromA4 = semisDifference( 'A4', noteName )
	return pitchFromOffsetToA4( offsetFromA4 )

	
def synthSin(frequency, durationSeconds, samplingFrequency):
	"""Returns a discrete-time sine-wave with frequency f, as a NumPy array of signed float 
	samples in the range -1.0 to 1.0."""

	numSamples = int( math.ceil(durationSeconds * samplingFrequency) )
	xs = (2.0 * frequency * math.pi / samplingFrequency) * numpy.arange( numSamples )
	samples = numpy.sin( xs )
	return samples


def smooshStartAndEnd(samples):
	"""Given a 1D NumPy array of samples, apply a windowing function (envelope) that
	crushes the first and last samples to 0. This will mean the sound samples fade in and
	then out, but will prevent clicking when transitioning from one sound to another."""

	return samples * numpy.hanning(len(samples))


def waveWrite(filename, fs, samples):
	"""Write the given samples to a WAV file named by filename.
	Samples are assumed to be in the range -1.0 to 1.0."""
	
	sample_width = 2

	w = wave.open(filename, 'wb')
	w.setnchannels(1)
	w.setsampwidth(sample_width)
	w.setframerate(fs)

	int16_samples = [max(-32768, min(32767, 65536 * 0.5 * s_)) for s_ in samples]

	buffer = ''
	for s16 in int16_samples:
		buffer += struct.pack( '<h', int( math.floor( s16 )))

	w.writeframes( buffer )
	w.close()

if __name__=='__main__':
	if len(sys.argv) != 3:
		print 'USAGE: python jsynth.py song.txt out.wav'
		exit(1)
		
	songfile = sys.argv[1]
	outfile = sys.argv[2]
	
	samples = numpy.array([], dtype = numpy.float)
	fs = 44100
	t = 0.0
	
	lines = open(songfile, 'r').readlines()
	for rawline in lines:
		line = string.strip(rawline)
		if 0 == len(line):
			continue
		(note, duration) = tuple(string.split(line))
		
		samples = numpy.append(samples, smooshStartAndEnd(synthSin( pitch(note), float(duration), fs )))
		
	waveWrite( outfile, fs, samples )
	
		
		

	
