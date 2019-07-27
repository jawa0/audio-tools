import math
from multiprocessing import Process, Queue, cpu_count
import numpy
import os
import pygame.mixer
import sys


sampleRate = 44100
recordingChannels = 2


#=============================================================================
def info( msg ):
    print(os.getpid(), msg)

#=============================================================================
def recordingProcessMain( commandQueue, outputQueue ):
	UNINITIALIZED = 1
	INITIALIZED = 2
	RECORDING = 3
	
	state = UNINITIALIZED
	stream = None

	info( 'Recording sub-process started.' )

	import pyaudio

	sampleFormat = pyaudio.paInt16
	p = pyaudio.PyAudio()
	
	state = INITIALIZED

	info( 'Waiting for commands.' )

	while True:
		cmd = commandQueue.get()	# Block until we get a command.
		info( "Got command: '" + cmd + "'" )
		if cmd == 'r':
			if state < INITIALIZED:
				info( 'Command ignored: not initialized.' )
				continue
			elif state == RECORDING:
				info( 'Command ignored: already recording.' )
				continue
				
			stream = p.open(format = sampleFormat,
							channels = recordingChannels,
							rate = sampleRate,
							input = True)
		
			state = RECORDING
			info( '* Started recording.' )
			
			data = b''
			while state == RECORDING:
				numFramesAvailable = stream.get_read_available()
				if numFramesAvailable:
					data += stream.read( numFramesAvailable )
					
				# Annoyed that I need to use exceptions here.
				# Will it drop audio frames?
				try:
					cmd = commandQueue.get_nowait()
					if cmd == 'r':
						stream.stop_stream()
						stream.close()
						info( '* Stopped recording.' )
						state = INITIALIZED
						
				except:
					pass
			
			print(len(data))
			outputQueue.put( data )

	p.terminate()

#=============================================================================
if __name__ == '__main__':
	info( 'Main process start.' )
	info( 'Detected %d cpu(s).' % (cpu_count()) )
	
	# Need to start recording sub-process (but not actually start recording)
	# before initializing pygame.mixer. Otherwise, recording process can't
	# get any recording devices.
	
	commandQ = Queue()
	recordingQ = Queue()
	
	info( 'Starting recording sub-process.' )
	recordingProcess = Process( target = recordingProcessMain,
							    args = ( commandQ, recordingQ))
	recordingProcess.start()

	pygame.mixer.pre_init( channels = 1, frequency = sampleRate, size = -16 )
	pygame.init()
	info( 'PyGame initialized.' )
	
	pygame.display.set_mode( (800, 600),
							 pygame.DOUBLEBUF |
							 pygame.OPENGL |
							 pygame.RESIZABLE )
	
	samples = None
	while True:
		event = pygame.event.wait()
		if event.type == pygame.QUIT:
			break
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or event.unicode == u'q':
				break
			elif event.unicode == u'r':	# toggle recording
				commandQ.put('r')
			elif event.unicode == u'p': # play recording
				try:
					recordedData = recordingQ.get_nowait()
					print(len(recordedData))
				except:
					if not samples:
						info( 'No completed recordings to play.' )
						continue
					
				# Finished recording. Make the data nice.
				if 1 == recordingChannels:
					sampleType = numpy.int16
				elif recordingChannels > 1:
					# column-vector of individual channels' samples. I.e. for stereo,
					# each element of the sample array is itself a 2x1 array.
					sampleType = numpy.dtype( (numpy.int16, (recordingChannels, 1)) )
				
				interleavedSamples = numpy.frombuffer( recordedData, dtype = sampleType )
				del recordedData
				
				leftSamples = numpy.ndarray.flatten( interleavedSamples[:,0] )
				#			rightSamples = numpy.ndarray.flatten( interleavedSamples[:,1] )
				
				samples = leftSamples
				sound = pygame.sndarray.make_sound( samples )
				sound.play(-1)
				pygame.time.delay(1000 * int(math.ceil(len(samples) / float(sampleRate))))
				sound.stop()
				
				
	recordingProcess.terminate()

	
#	
#