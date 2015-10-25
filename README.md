# Jaba's Audio Tools

Some Python scripts for recording and synthesizing audio. Also, a script for drawing spectrograms from a WAV file.

- src/audioPlay.py: Play a 4 second 440 Hz (A4) tone. Demonstrates how to generate samples and play audio from Python.
- src/jsynth.py: Reads a simple text format that lets you specify note pitches and durations. Generates samples, and outputs a WAV file. A super simple and limited synthesizer.
- src/recordAudio.py: Command-line program to record audio. Can start and stop recording by pressing 'r'.
- src/spectrogram.py: Read a WAV file, and produce a PNG of the spectrogram. Does not use a log-scale for pitch, so the images are very tall.
- data/: various synthesized scales and also recorded ambient background noise
