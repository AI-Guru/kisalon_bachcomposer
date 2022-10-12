# Copyright 2022 Tristan Behrens.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3

from ast import Pass
from flask import (
    Flask,
    render_template,
    request,
    send_file,
    jsonify,
    redirect,
    url_for,
    send_from_directory
)
from flask_security import current_user, auth_token_required

import os
from transformers import AutoTokenizer, AutoModelForCausalLM
from source.midihelpers import program_to_name
import json
from source.compose import Composer
from source.music import (
    token_sequence_to_note_sequence,
    play_note_sequence, 
    note_sequence_to_svg,
    note_sequence_to_audio,
    encode_audio_base64,
    save_token_sequence_to_midi
)
import tempfile
import time
from source import logging
import torch
import traceback
import datetime
from waitress import serve


# Create the logger.
logger = logging.create_logger(__name__)


# Get the device.
device = "cuda" if torch.cuda.is_available() else "cpu"
logger.info(f"PyTorch Device: {device}")


# Get the soundfont.
sound_font_path = "bin/soundfont.sf2"
if not os.path.exists(sound_font_path):
    sound_font_path = None


# Load the tokenizer.
tokenizer_path = "TristanBehrens/js-fakes-4bars"
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

# Load the model.
model_path = "TristanBehrens/js-fakes-4bars"
model = AutoModelForCausalLM.from_pretrained(model_path).to(device)

min_pitch = 24
max_pitch = 96
scale_x = 1000.0
scale_y = 500.0


# Get all the tokens in the tokenizer.
all_tokens = tokenizer.get_vocab()

# 0, 24, 32, 48.

# Create the composer.
song_composer = Composer(tokenizer, model, device)


# Default instruments.
default_instruments = ["INST=0", "INST=24", "INST=32", "INST=48"]

# Get the densities data from the densities tokens.
#densities_data = []
#for token in [token for token in all_tokens if token.startswith("DENSITY=")]:
#    density = token.split("=")[1]
#    densities_data.append({"name": density, "token": token})
#densities_data = sorted(densities_data, key=lambda x: str(x["name"]))

app = Flask(__name__)

# Load all the active tokens from the file.
def get_active_tokens_dict():
    active_tokens_dict = {}
    with open("active_tokens.txt", "r") as f:
        lines = f.read().splitlines()
        for line in lines:
            token, user_id = line.split(",")
            active_tokens_dict[token.strip()] = user_id.strip()

    return active_tokens_dict


def is_authorized(authorization_token):

    active_tokens_dict = get_active_tokens_dict()

    if not authorization_token:
        return False
    else:
        if authorization_token.startswith("Bearer "):
            authorization_token = authorization_token.split(" ")[1]
        authorization_token = authorization_token.strip()
        if authorization_token == "":
            return False
        elif authorization_token in active_tokens_dict.keys():
            return True
        else: 
            return False
    return False


def get_user_name(authorization_token):

    active_tokens_dict = get_active_tokens_dict()

    if not authorization_token:
        return None
    else:
        if authorization_token.startswith("Bearer "):
            authorization_token = authorization_token.split(" ")[1]
        authorization_token = authorization_token.strip()
        if authorization_token != "" and authorization_token in active_tokens_dict:
            return active_tokens_dict[authorization_token]
    return None


@app.route("/")
def index():
    return render_template("login.html")

@app.route("/auth", methods=["POST"])
def auth():
    logger.info("Authenticating...")
    
    # Get the form data.
    form_data = request.form
    authorization_token = form_data["auth_token"]
    
    # Check authorization.
    if is_authorized(authorization_token):
        logger.info(f"Authorized user: {get_user_name(authorization_token)}")
        redirect_url = url_for("composer")
        return redirect(redirect_url)
    else:
        logger.info("Unauthorized token: " + authorization_token)
        return "Unauthorized", 401


# Route for the loading page.
@app.route("/composer")
def composer():

    number_of_instruments = 4
    number_of_bars = 8
    number_of_rows = number_of_instruments + 1
    number_of_columns = number_of_bars + 2

    return render_template(
        "composer.html",
        #number_of_columns=number_of_columns,
        #cells_data=cells_data,
        #chord_progressions_data=chord_progressions,
        #chords_data=chords_data,
        #densities_data=densities_data,
        #instruments_data=instruments_data
    )


def get_auth_token_from_request(header):
    if not header:
        return None
    else:
        return header.split(" ")[1]

# Route for executing a command. Uses POST.
@app.route("/command", methods=["POST"])
def command():

    # Handle authentication.
    authorization_token = get_auth_token_from_request(request.headers.get("Authorization"))
    if authorization_token is None:
        return "", 401
    if not is_authorized(authorization_token):
        return "Unauthorized", 401

    # Get the user name.
    user_name = get_user_name(authorization_token)
    
    # Get the command as JSON from the request.
    json_data = request.get_json()
    command_name = json_data["command_name"]
    command_parameters = json_data["command_parameters"]

    logger.info(f"{user_name} executing command: {command_name}...")

    try:
        return execute_command(command_name, command_parameters, authorization_token)
    except Exception as exception:
        write_exception(exception, authorization_token, command_name, command_parameters)
        logger.error(traceback.format_exc())
        return "Error", 500


def execute_command(command_name, command_parameters, authorization_token):

    # Compose some music.
    if command_name == "compose" or command_name == "redo":

        # Compose a song.
        start_time = time.time()
        if command_name == "compose":
            token_sequence = song_composer.compose_song(command_parameters)
        else:
            token_sequence = song_composer.redo_track(command_parameters)
        elapsed_time = time.time() - start_time
        number_of_tokens = len(token_sequence.split())
        tokens_per_second = number_of_tokens / elapsed_time
        status_string = f"{number_of_tokens} tokens in {elapsed_time:.2f} seconds ({tokens_per_second:.2f} tokens per second)"

        # Turn it into a note sequence.
        bpm = float(command_parameters["bpm"])
        note_sequence = token_sequence_to_note_sequence(token_sequence, bpm)

        # Set the instrument.
        instrument = int(command_parameters["instrument"])
        for note in note_sequence.notes:
            note.program = instrument

        # Convert into audio.
        audio_data, sample_rate = note_sequence_to_audio(note_sequence)

        # Encode to base64.
        audio_data_base64 = encode_audio_base64(audio_data, sample_rate)

        # Turn the note sequence into a svg.
        svg_string = note_sequence_to_svg(note_sequence, bpm, min_pitch=min_pitch, max_pitch=max_pitch, scale_x=scale_x, scale_y=scale_y)

        # Play the note sequence.
        #play_note_sequence(note_sequence, sound_font_path)

        # Return the svg as a JSON object.
        return jsonify(
            {
                "status": "OK",
                "svg": svg_string,
                "audio_data": audio_data_base64,
                "token_sequence": token_sequence,
                "status_string": status_string
            }
        )

    # Play the token sequence. Returns the audio data and the SVG.
    elif command_name == "play":
        token_sequence = command_parameters["token_sequence"]
        bpm = float(command_parameters["bpm"])
        note_sequence = token_sequence_to_note_sequence(token_sequence, bpm)
        instrument = int(command_parameters["instrument"])
        for note in note_sequence.notes:
            note.program = instrument
        audio_data, sample_rate = note_sequence_to_audio(note_sequence)
        audio_data_base64 = encode_audio_base64(audio_data, sample_rate)
        svg_string = note_sequence_to_svg(note_sequence, bpm, min_pitch=min_pitch, max_pitch=max_pitch, scale_x=scale_x, scale_y=scale_y)
        return jsonify(
            {
                "status": "OK",
                "svg": svg_string,
                "audio_data": audio_data_base64
            }
        )

    # Generate MIDI.
    elif command_name == "midi":
        
        # Get the token sequence.
        token_sequence = command_parameters["token_sequence"]
        bpm = float(command_parameters["bpm"])

        # Get the timestamp as YYYYMMDD-HHMMSS.
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

        # Write the MIDI file.
        midi_folder = os.path.join("midi", authorization_token, timestamp)
        if not os.path.exists(midi_folder):
            os.makedirs(midi_folder)
        midi_path = os.path.join(midi_folder, "song.mid")

        # Save the midi file.
        save_token_sequence_to_midi(token_sequence, midi_path, bpm)
        logger.info(f"Saved token sequence to {midi_path}")

        # Send the file as a response.
        return send_file(midi_path, as_attachment=True, mimetype="audio/midi")

           

    else:
        raise Exception(f"Unknown command: {command_name}")

    return True

def write_exception(exception, authorization_token, command_name, command_parameters):
    exception_folder = "exceptions"
    if not os.path.exists(exception_folder):
        os.mkdir(exception_folder)

    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    exception_file_name = f"{exception_folder}/{timestamp}.json"

    with open(exception_file_name, "w") as f:
        exception_data = {
            "timestamp": timestamp,
            "authorization_token": authorization_token,
            "command_name": command_name,
            "command_parameters": command_parameters,
            "exception": str(exception),
        }
        f.write(json.dumps(exception_data, indent=4))

# App route for song images.
@app.route("/images/<image_name>")
def images(image_name):
    return send_file(f"static/songimage.jpg")


@app.route('/robots.txt')
#@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


#if __name__ == '__main__':
#   app.run(host="0.0.0.0", port=5666)


if __name__ == "__main__":
    logger.info("Starting server...")
    serve(app, host="0.0.0.0", port=5777)