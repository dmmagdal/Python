# Docker file to run a container that will run the download.py in
# Python 3.

# Load Python 3.7 image.
FROM python:3.7.14

# Set locale for variable (pulled from dockerfile in original OpenAI
# GPT2 repository).
ENV LANG=C.UTF-8

# Create a directory in the docker container. Set the working directory
# in the container to that newly created directory and then add all
# files from the current directory in the host to the working directory
# in the container.
RUN mkdir /yt2mp3
WORKDIR /yt2mp3
ADD . /yt2mp3/

# Set up a volume so that the current directory in the host is
# connected to the working directory in the container.

# Uncomment to download model to local storage and run it from there
# instead of relying on Huggingface Hub.
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y ffmpeg

# Install all required modules in the requirements.txt file.
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

# Run the download.py program.
CMD ["python3", "download.py"]