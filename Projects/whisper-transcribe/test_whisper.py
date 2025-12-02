import whisper
import wave
import sys
from pydub import AudioSegment
import pyaudio
import numpy as np

CHUNK = 20000 

if len(sys.argv) < 2:
    print(f'Plays a wave file. Usage: {sys.argv[0]} filename.wav')
    sys.exit(-1)

# Load your mp3 file (requires ffmpeg to be installed)
print(sys.argv[1])
audio = AudioSegment.from_mp3(sys.argv[1]).set_frame_rate(16000).set_channels(1)

# Get raw PCM data
raw_data = audio.raw_data

# Instantiate PyAudio and initialize PortAudio system resources (1)
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(f"Device {i}: {info['name']}")

# Open stream (2)
print("open stream")
stream = p.open(format=p.get_format_from_width(audio.sample_width),
                channels=audio.channels,
                rate=audio.frame_rate,
                output=True,
                output_device_index=6)

model = whisper.load_model("tiny")
# Play samples from the wave file (3)
chunk_length = CHUNK * audio.frame_width
for i in range(0, len(raw_data), chunk_length):
    chunk_data = raw_data[i:i+chunk_length]
    # Convert to numpy array for Whisper (float32, -1 to 1)
    audio_array = np.frombuffer(chunk_data, dtype=np.int16).flatten().astype(np.float32) / 32768.0
    
    result = model.transcribe(audio_array)
    print(result["text"])
    stream.write(chunk_data)

# Close stream (4)
stream.close()

# Release PortAudio system resources (5)
p.terminate()



