from faster_whisper import WhisperModel
m=WhisperModel("medium",device="cpu",compute_type="int8")
segs,_=m.transcribe(__import__("numpy").fromfile("v16.raw",dtype="float32"),language="ar",vad_filter=True)
for s in segs: print(f"[{s.start:6.1f}-{s.end:6.1f}] {s.text}")
