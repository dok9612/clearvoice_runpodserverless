# 1. Base image with PyTorch and CUDA
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

# 2. Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg

# 3. Set the main working directory inside the container
WORKDIR /app

# 4. Copy the entire repository from your workspace into the container's /app folder
COPY . /app

# 5. Install the global requirements
RUN pip install -r requirements.txt

# 6. Move inside the specific package folder
WORKDIR /app/clearvoice

# 7. Install the package and RunPod SDK
RUN pip install -e .
RUN pip install runpod

# 8. THE CACHE TRICK: Pre-download models into the image to prevent cold starts
RUN python3 -c "from clearvoice import ClearVoice; \
    ClearVoice(task='speech_enhancement', model_names=['MossFormer2_SE_48K']); \
    ClearVoice(task='speech_super_resolution', model_names=['MossFormer2_SR_48K'])"

# 9. Start the serverless API
CMD ["python3", "handler.py"]