import scipy
from transformers import AutoProcessor, SeamlessM4Tv2Model
from transformers import MusicgenForConditionalGeneration
import torchaudio

processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")

inputs = processor(
    text=["A Wonderful land"],
    padding=True,
    return_tensors="pt",
)

audio_values = model.generate(**inputs, max_new_tokens=1024)


sampling_rate = model.config.audio_encoder.sampling_rate
scipy.io.wavfile.write("./audio_gen-out.wav", rate=sampling_rate, data=audio_values[0, 0].numpy())