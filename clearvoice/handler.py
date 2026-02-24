import base64
import tempfile
import os
from typing import Dict, Any
import runpod
from clearvoice import ClearVoice

print("Loading models into VRAM...")
myClearVoice_SE: ClearVoice = ClearVoice(task='speech_enhancement', model_names=['MossFormer2_SE_48K'])
myClearVoice_SR: ClearVoice = ClearVoice(task='speech_super_resolution', model_names=['MossFormer2_SR_48K'])

def process_audio(job: Dict[str, Any]) -> Dict[str, str]:
    """RunPod synchronous entry point."""
    job_input: Dict[str, Any] = job.get("input", {})
    base64_string: str = job_input.get("audio_base64", "")
    
    # 1. Decode the incoming base64 string to raw bytes
    audio_bytes: bytes = base64.b64decode(base64_string)
    
    # 2. Create an isolated, self-deleting folder for this request
    with tempfile.TemporaryDirectory() as temp_dir:
        
        # Define the exact file paths inside our temporary folder
        input_path: str = os.path.join(temp_dir, "input.wav")
        se_out_path: str = os.path.join(temp_dir, "enhanced.wav")
        final_out_path: str = os.path.join(temp_dir, "enhanced_supersolutioned.wav")
        
        # Write the raw bytes to our temporary input file
        with open(input_path, "wb") as f:
            f.write(audio_bytes)
        
        # 3. Process through Speech Enhancement
        print("Running Speech Enhancement...")
        se_wav = myClearVoice_SE(input_path=input_path, online_write=False)
        myClearVoice_SE.write(se_wav, output_path=se_out_path)
        
        # 4. Process through Super Resolution
        print("Running Super Resolution...")
        sr_wav = myClearVoice_SR(input_path=se_out_path, online_write=False)
        myClearVoice_SR.write(sr_wav, output_path=final_out_path)
        
        # 5. Prepare the output payload
        with open(final_out_path, "rb") as f:
            output_bytes: bytes = f.read()
            
        # Convert bytes back to a base64 string and decode it to standard text
        final_base64: str = base64.b64encode(output_bytes).decode("utf-8")
        
    return {"status": "success", "audio_base64": final_base64}

if __name__ == "__main__":
    runpod.serverless.start({"handler": process_audio})