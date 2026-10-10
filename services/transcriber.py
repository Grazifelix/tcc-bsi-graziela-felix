from faster_whisper import WhisperModel

class AudioTranscriber:
    def __init__(self, model_size="small", device="cpu", compute_type="int8"):
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)

    def transcribe(self, audio_path, beam_size=5):
        segments_generator, info = self.model.transcribe(audio_path, beam_size=beam_size)
        
        segments_list = []
        full_text_parts = []

        for segment in segments_generator:
            clean_text = segment.text.strip()
            full_text_parts.append(clean_text)
            
            segments_list.append({
                "start": round(segment.start, 2),
                "end": round(segment.end, 2),
                "text": clean_text
            })

        # Monta a estrutura otimizada para LLMs
        return {
            "metadata": {
                "language": info.language,
                "duration_seconds": round(info.duration, 2)
            },
            # Texto contínuo sem timestamps (Ideal para economizar tokens em sumarizações)
            "full_text": " ".join(full_text_parts),
            # Texto formatado com timestamps inline (Ideal para LLM citar trechos exatos)
            "formatted_transcript": "\n".join(
                [f"[{s['start']}s -> {s['end']}s] {s['text']}" for s in segments_list]
            ),
            # Segmentos brutos caso vá alimentar um banco vetorial (RAG)
            "segments": segments_list
        }

# from faster_whisper import WhisperModel

# model_size = "small"

# # Run on GPU with FP16
# model = WhisperModel(model_size, device="cpu", compute_type="int8")

# # or run on GPU with INT8
# # model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# # or run on CPU with INT8
# # model = WhisperModel(model_size, device="cpu", compute_type="int8")

# segments, info = model.transcribe("audio2.m4a", language="pt", beam_size=5)

# print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

# for segment in segments:
#     print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))