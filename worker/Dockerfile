FROM linuxserver/blender:latest

WORKDIR /render

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Copy worker script
COPY worker.py /render/worker.py

ENTRYPOINT ["python3", "/render/worker.py"]
