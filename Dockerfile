# 1. Base image with PyTorch and CUDA
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

# 2. Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg

# 3. Set the main working directory inside the container
WORKDIR /app

# 4. Copy the entire repository from your workspace into the container's /app folder
COPY . /app

# 4.5 Install critical system dependencies and audio libraries
# The rm -rf command clears the apt cache to keep the final image size small
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# 5. Install the global requirements
# Using --no-cache-dir prevents pip from storing massive wheel files, saving GBs of space
RUN pip install --no-cache-dir -r requirements.txt

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