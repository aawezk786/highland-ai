from flask import Flask, abort, request
from tempfile import NamedTemporaryFile
import whisper
import torch

# Check if NVIDIA GPU is available
torch.cuda.is_available()
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
task = 'translate'
langauge = 'english'
# Load the Whisper model:
model = whisper.load_model("base", device=DEVICE)

app = Flask(__name__)


@app.route("/healthcheck")
def hello():
    return {
        'message': 'Service Running'
    }


@app.route('/asr', methods=['POST'])
def handler():
    print(request)
    if not request.args:
        abort(400)
    if not request.files:
        # If the user didn't submit any files, return a 400 (Bad Request) error.
        abort(400)

    # For each file, let's store the results in a list of dictionaries.
    results = []

    # Loop over every file that the user submitted.
    for filename, handle in request.files.items():
        # Create a temporary file.
        # The location of the temporary file is available in `temp.name`.
        temp = NamedTemporaryFile()
        # Write the user's uploaded file to the temporary file.
        # The file will get deleted when it drops out of scope.
        handle.save(temp)
        # Let's get the transcript of the temporary file.
        # if request.args.get('task') == 'translate':
        #     result = model.transcribe(temp.name, task=task)
        # if not request.args.get('language'):
        #     print(request.args.get('language'))
        #     langaugeTranscribe = model.transcribe(
        #         temp.name, task=task, langauge=langauge)
        result = model.transcribe(temp.name, task=task)
        print(result)
        # Now we can store the result object for this file.
        results.append({
            'filename': filename,
            'transcript': result['text'],
            'language': result['language']
        })

    # This will be automatically converted to JSON.
    return {'results': results}
