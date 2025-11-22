import whisper
import wave
import sys
from pydub import AudioSegment
import pyaudio
CHUNK = 1024

if len(sys.argv) < 2:
    print(f'Plays a wave file. Usage: {sys.argv[0]} filename.wav')
    sys.exit(-1)

# Load your mp3 file (requires ffmpeg to be installed)
print(sys.argv[1])
audio = AudioSegment.from_mp3(sys.argv[1])

# Get raw PCM data
raw_data = audio.raw_data

# Instantiate PyAudio and initialize PortAudio system resources (1)
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(f"Device {i}: {info['name']}")

# Open stream (2)
stream = p.open(format=p.get_format_from_width(audio.sample_width),
                channels=audio.channels,
                rate=audio.frame_rate,
                output=True)

# Play samples from the wave file (3)
while len(data := audio.read_frame(CHUNK)):  # Requires Python 3.8+ for :=
    stream.write(data)

# Close stream (4)
stream.close()

# Release PortAudio system resources (5)
p.terminate()

model = whisper("turbo")
result = model.transcribe(sys.argv[1])
print(result["text"])