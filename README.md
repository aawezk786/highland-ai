# STEPS:

1.pip3 install -r requirements.txt

2.pip3 install "git+https://github.com/openai/whisper.git"

3.apt-get install -y ffmpeg / brew install ffmpeg

# DOCKER:

1.docker build -t highland-ai .
2.docker run -p 5000:5000 highland-ai
