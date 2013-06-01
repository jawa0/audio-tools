#!/bin/sh

python spectrogram.py C1-major.wav
mv spectrogram.png spectrum-C1-major.png

python spectrogram.py C2-major.wav
mv spectrogram.png spectrum-C2-major.png

python spectrogram.py C3-major.wav
mv spectrogram.png spectrum-C3-major.png

python spectrogram.py C4-major.wav
mv spectrogram.png spectrum-C4-major.png

python spectrogram.py C5-major.wav
mv spectrogram.png spectrum-C5-major.png

python spectrogram.py C6-major.wav
mv spectrogram.png spectrum-C6-major.png

python spectrogram.py C7-major.wav
mv spectrogram.png spectrum-C7-major.png

python spectrogram.py C8-major.wav
mv spectrogram.png spectrum-C8-major.png
