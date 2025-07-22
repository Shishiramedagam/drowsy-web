import numpy as np
from scipy.io.wavfile import write

# Settings for the sound
duration = 2  # seconds
frequency = 440  # Hz (A4 tone)
sample_rate = 44100  # samples per second

# Generate a sine wave
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
waveform = 0.5 * np.sin(2 * np.pi * frequency * t)

# Convert to 16-bit PCM
waveform_integers = np.int16(waveform * 32767)

# Save as WAV file
write("alarm.wav", sample_rate, waveform_integers)

print("alarm.wav file generated successfully!")
