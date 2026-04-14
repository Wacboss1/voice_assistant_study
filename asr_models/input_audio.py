from transformers import AutoProcessor, CohereAsrForConditionalGeneration
from transformers.audio_utils import load_audio
from huggingface_hub import hf_hub_download
import sounddevice as sd
from scipy.io.wavfile import write

# This part takes time so do it once a the beginning of the program
processor = AutoProcessor.from_pretrained("CohereLabs/cohere-transcribe-03-2026")
model = CohereAsrForConditionalGeneration.from_pretrained("CohereLabs/cohere-transcribe-03-2026", device_map="auto")

# TODO Create a wav file from the input audio and save it to a temporary location
sampling_rate = 16000
seconds = 3
filename = "out.wav"
print("Recording Started")
recording = sd.rec(int(seconds*sampling_rate), samplerate=sampling_rate, channels=1)
sd.wait()

# TODO Pass nparray file to ASR
processed_recording = load_audio(recording.ravel(), sampling_rate=sampling_rate)
print(processed_recording)
inputs = processor(processed_recording, sampling_rate=sampling_rate, return_tensors="pt", language="en")
inputs.to(model.device, dtype=model.dtype)

outputs = model.generate(**inputs, max_new_tokens=256)
cohere_text = processor.decode(outputs, skip_special_tokens=True)
print(cohere_text)

