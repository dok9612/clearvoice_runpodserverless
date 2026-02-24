import base64
import json

# Read the audio and encode it
with open("./input/test.wav", "rb") as f:
    encoded_audio: str = base64.b64encode(f.read()).decode("utf-8")

# Format it exactly how RunPod expects it
payload = {
    "input": {
        "audio_base64": encoded_audio
    }
}

# Save it to test_input.json
with open("test_input.json", "w") as f:
    json.dump(payload, f)
    
print("Successfully created test_input.json!")