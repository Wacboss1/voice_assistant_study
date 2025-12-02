import whisper
import pyaudio
import numpy as np
import threading
import queue
import time
import sys

# Audio recording parameters
RATE = 16000
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
# Buffer threshold in seconds to trigger transcription
TRANSCRIPTION_INTERVAL = 2.0 

class AudioTranscriber:
    def __init__(self, model_name="tiny"):
        print(f"Loading Whisper model '{model_name}'...")
        self.model = whisper.load_model(model_name)
        print("Model loaded.")
        
        self.audio_queue = queue.Queue()
        self.running = False
        self.p = pyaudio.PyAudio()
        
    def start_recording(self):
        self.running = True
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=CHUNK)
        
        # Start recording thread
        self.record_thread = threading.Thread(target=self._record_loop)
        self.record_thread.start()
        
        # Start transcription thread
        self.transcribe_thread = threading.Thread(target=self._transcribe_loop)
        self.transcribe_thread.start()
        
        print("Recording... Press Ctrl+C to stop.")
        
    def stop_recording(self):
        self.running = False
        if hasattr(self, 'record_thread'):
            self.record_thread.join()
        if hasattr(self, 'transcribe_thread'):
            self.transcribe_thread.join()
            
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        print("Recording stopped.")

    def _record_loop(self):
        while self.running:
            try:
                data = self.stream.read(CHUNK, exception_on_overflow=False)
                self.audio_queue.put(data)
            except Exception as e:
                print(f"Error recording: {e}")
                break

    def _transcribe_loop(self):
        audio_buffer = b""
        # Calculate bytes needed for the interval
        # 2 bytes per sample (int16) * RATE samples/sec * seconds
        bytes_per_interval = 2 * RATE * TRANSCRIPTION_INTERVAL
        
        while self.running or not self.audio_queue.empty():
            try:
                # Get data from queue
                # Use a timeout so we can check self.running periodically
                data = self.audio_queue.get(timeout=0.5)
                audio_buffer += data
                
                if len(audio_buffer) >= bytes_per_interval:
                    # Process the buffer
                    self._process_buffer(audio_buffer)
                    # Clear buffer (simple approach: just drop it. 
                    # For better results, one might keep some overlap)
                    audio_buffer = b""
                    
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error in transcription loop: {e}")

    def _process_buffer(self, buffer_data):
        # Convert raw bytes to numpy array
        # Whisper expects float32 audio, normalized to [-1, 1]
        audio_array = np.frombuffer(buffer_data, dtype=np.int16).flatten().astype(np.float32) / 32768.0
        
        # Transcribe
        result = self.model.transcribe(audio_array, fp16=False) # fp16=False for CPU compatibility if needed
        text = result["text"].strip()
        if text:
            print(f"Transcribed: {text}")

if __name__ == "__main__":
    transcriber = AudioTranscriber(model_name="base")
    try:
        transcriber.start_recording()
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        transcriber.stop_recording()
