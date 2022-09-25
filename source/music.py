import note_seq
from note_seq.midi_synth import fluidsynth
import tempfile
import scipy
import os
import numpy as np
import wave
import base64
import io
import svgwrite

#NOTE_LENGTH_16TH_120BPM = 0.25 * 60 / 120
#BAR_LENGTH_120BPM = 4.0 * 60 / 120
SAMPLE_RATE=44100


def play_note_sequence(note_sequence, soundfont_path=None):
    synth=fluidsynth
    sample_rate = 44100
    data = synth(note_sequence, sample_rate=sample_rate)
    
    # Play wav from a temporary directory.
    with tempfile.TemporaryDirectory() as tmpdirname:
        wav_path = os.path.join(tmpdirname, "song.wav")
        scipy.io.wavfile.write(wav_path, sample_rate, data)
        os.system(f"afplay {wav_path}")


def save_token_sequence_to_midi(token_sequence, midi_path, bpm):
    note_sequence = token_sequence_to_note_sequence(token_sequence, bpm)
    note_seq.midi_io.note_sequence_to_midi_file(note_sequence, midi_path)


def note_sequence_to_audio(note_sequence):
    synth = note_seq.midi_synth.fluidsynth
    array_of_floats = synth(note_sequence, sample_rate=SAMPLE_RATE)
    note_plot = note_seq.plot_sequence(note_sequence, False)
    array_of_floats /= 1.414
    array_of_floats *= 32767
    int16_data = array_of_floats.astype(np.int16)
    return int16_data, SAMPLE_RATE


def encode_audio_base64(audio_data, sample_rate):
    # Encode the audio-data as wave file in memory. Use the wave module.
    audio_data_bytes = io.BytesIO()
    wave_file = wave.open(audio_data_bytes, "wb")
    wave_file.setframerate(sample_rate)
    wave_file.setnchannels(1)
    wave_file.setsampwidth(2)
    wave_file.writeframes(audio_data)
    wave_file.close()

    # Return the audio-data as a base64-encoded string.
    audio_data_bytes.seek(0)
    audio_data_base64 = base64.b64encode(audio_data_bytes.read()).decode("utf-8")
    audio_data_bytes.close()

    return audio_data_base64


def token_sequence_to_note_sequence(token_sequence, bpm, use_program=True, use_drums=True, instrument_mapper=None, only_piano=False):

    if isinstance(token_sequence, str):
        token_sequence = token_sequence.split()

    note_sequence = empty_note_sequence(qpm=bpm)

    print("ACHTUNG bpm", bpm)

    note_length_bpm = 0.25 * 60 / bpm
    bar_length_bpm = 4.0 * 60 / bpm

    # Render all notes.
    current_program = 1
    current_is_drum = False
    current_instrument = 0
    track_count = 0
    for token_index, token in enumerate(token_sequence):

        if token == "PIECE_START":
            pass
        elif token == "PIECE_END":
            break
        elif token == "TRACK_START":
            current_bar_index = 0
            track_count += 1
            pass
        elif token == "TRACK_END":
            pass
        elif token == "KEYS_START":
            pass
        elif token == "KEYS_END":
            pass
        elif token.startswith("KEY="):
            pass
        elif token.startswith("INST"):
            instrument = token.split("=")[-1]
            if instrument != "DRUMS" and use_program:
                if instrument_mapper is not None:
                    if instrument in instrument_mapper:
                        instrument = instrument_mapper[instrument]
                current_program = int(instrument)
                current_instrument = track_count
                current_is_drum = False
            if instrument == "DRUMS" and use_drums:
                current_instrument = 0
                current_program = 0
                current_is_drum = True
        elif token == "BAR_START":
            current_time = current_bar_index * bar_length_bpm
            current_notes = {}
        elif token == "BAR_END":
            current_bar_index += 1
            pass
        elif token.startswith("NOTE_ON"):
            pitch = int(token.split("=")[-1])
            note = note_sequence.notes.add()
            note.start_time = current_time
            note.end_time = current_time + 4 * note_length_bpm
            note.pitch = pitch
            note.instrument = current_instrument
            note.program = current_program
            note.velocity = 80
            note.is_drum = current_is_drum
            current_notes[pitch] = note
        elif token.startswith("NOTE_OFF"):
            pitch = int(token.split("=")[-1])
            if pitch in current_notes:
                note = current_notes[pitch]
                note.end_time = current_time
        elif token.startswith("TIME_DELTA"):
            delta = float(token.split("=")[-1]) * note_length_bpm
            current_time += delta
        elif token.startswith("DENSITY="):
            pass
        elif token == "[PAD]":
            pass
        else:
            pass

    # Make the instruments right.
    instruments_drums = []
    for note in note_sequence.notes:
        pair = [note.program, note.is_drum, note.instrument]
        if pair not in instruments_drums:
            instruments_drums += [pair]
        note.instrument = instruments_drums.index(pair)

    if only_piano:
        for note in note_sequence.notes:
            if not note.is_drum:
                note.instrument = 0
                note.program = 0

    for note in note_sequence.notes:
        if note.end_time > note_sequence.total_time:
            note_sequence.total_time = note.end_time

    return note_sequence


def empty_note_sequence(qpm=120.0, total_time=0.0):
    note_sequence = note_seq.protobuf.music_pb2.NoteSequence()
    note_sequence.tempos.add().qpm = qpm
    note_sequence.ticks_per_quarter = note_seq.constants.STANDARD_PPQ
    note_sequence.total_time = total_time
    return note_sequence


def note_sequence_to_svg(note_sequence, bpm):

    # Make sure that the end_time is correct.
    for note in note_sequence.notes:
        if note.end_time > note_sequence.total_time:
            note_sequence.total_time = note.end_time


    note_length_bpm = 0.25 * 60 / bpm
    bar_length_bpm = 4.0 * 60 / bpm

    # Create a list of lists of notes.
    # Each list of notes is a bar.

    # Create an empty SVG.
    scale_x = 1000.0
    scale_y = 500.0

    colors = ["orchid", "magenta", "violet", "hotpink"]
    colors = ["#f5da4b", "#b63655", "#892169", "#e45b2e"]

    svg_document = svgwrite.Drawing(
        filename = None,
        size = (scale_x, scale_y)
    )

    # Do a bars grid. No fill. Just white lines.
    #for bar_index in range(int(note_sequence.total_time / bar_length_bpm) + 1):
    #    svg_document.add(
    #        svg_document.line(
    #            start = (bar_index * bar_length_bpm * scale_x / note_sequence.total_time, 0),
    #            end = (bar_index * bar_length_bpm * scale_x / note_sequence.total_time, scale_y),
    #            # make the stroke a dark purple
    #            stroke = "purple",
    #            stroke_width = 1
    #        )
    #    )

    for note in note_sequence.notes:
        pitch = note.pitch
        start_time = note.start_time
        end_time = note.end_time
        if note.is_drum:
            pitch -= 36
            end_time = start_time + 0.05
        svg_document.add(
            # Make the rect glow.
            svgwrite.shapes.Rect(
                insert = (scale_x * start_time / note_sequence.total_time, scale_y * (128 - pitch) / 128),
                size = (scale_x *   (end_time - start_time) / note_sequence.total_time, 2 * scale_y / 128),
                fill = colors[note.instrument],
                rx = 2.0,
            )
        )

    # Turn the SVG into a string.
    svg_string = svg_document.tostring()
    return svg_string
    #svg_document.save()