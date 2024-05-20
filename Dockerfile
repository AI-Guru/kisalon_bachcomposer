# Use the official PyTorch image as the base image.
FROM pytorch/pytorch:2.3.0-cuda12.1-cudnn8-runtime

# Set working directory inside the container.
WORKDIR /app

# Install everything around fluidsynth.
RUN apt-get update -qq && apt-get install -qq fluidsynth libfluidsynth-dev build-essential libasound2-dev libjack-dev 

# Copy the requirements.txt file into the container and install the dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all scripts and binaries into the container
COPY source/ ./source
COPY static/ ./static
COPY templates/ ./templates
COPY app.py .

# Set the entrypoint.
ENTRYPOINT FLASK_APP=/app/app.py FLASK_ENV=production flask run --host=0.0.0.0 --port=5001