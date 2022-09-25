# Copyright 2021 Tristan Behrens.
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

midi_table = [("?", "?") for _ in range(128)]
midi_table[0] = ("acoustic_grand_piano", "piano")
midi_table[1] = ("bright_acoustic_piano", "piano")
midi_table[2] = ("electric_grand_piano", "piano")
midi_table[3] = ("honky-tonk_piano", "piano")
midi_table[4] = ("electric_piano_1", "piano")
midi_table[5] = ("electric_piano_2", "piano")
midi_table[6] = ("harpsichord", "piano")
midi_table[7] = ("clavinet", "piano")
midi_table[8] = ("celesta", "chromatic percussion")
midi_table[9] = ("glockenspiel", "chromatic percussion")
midi_table[10] = ("music_box", "chromatic percussion")
midi_table[11] = ("vibraphone", "chromatic percussion")
midi_table[12] = ("marimba", "chromatic percussion")
midi_table[13] = ("xylophone", "chromatic percussion")
midi_table[14] = ("tubular_bells", "chromatic percussion")
midi_table[15] = ("dulcimer", "chromatic percussion")
midi_table[16] = ("drawbar_organ", "organ")
midi_table[17] = ("percussive_organ", "organ")
midi_table[18] = ("rock_organ", "organ")
midi_table[19] = ("church_organ", "organ")
midi_table[20] = ("reed_organ", "organ")
midi_table[21] = ("accordion", "organ")
midi_table[22] = ("harmonica", "organ")
midi_table[23] = ("tango_accordion", "organ")
midi_table[24] = ("acoustic_guitar_nylon", "guitar")
midi_table[25] = ("acoustic_guitar_steel", "guitar")
midi_table[26] = ("electric_guitar_jazz", "guitar")
midi_table[27] = ("electric_guitar_clean", "guitar")
midi_table[28] = ("electric_guitar_muted", "guitar")
midi_table[29] = ("overdriven_guitar", "guitar")
midi_table[30] = ("distortion_guitar", "guitar")
midi_table[31] = ("guitar_harmonics", "guitar")
midi_table[32] = ("acoustic_bass", "bass")
midi_table[33] = ("electric_bass_finger", "bass")
midi_table[34] = ("electric_bass_pick", "bass")
midi_table[35] = ("fretless_bass", "bass")
midi_table[36] = ("slap_bass_1", "bass")
midi_table[37] = ("slap_bass_2", "bass")
midi_table[38] = ("synth_bass_1", "bass")
midi_table[39] = ("synth_bass_2", "bass")
midi_table[40] = ("violin", "strings")
midi_table[41] = ("viola", "strings")
midi_table[42] = ("cello", "strings")
midi_table[43] = ("contrabass", "strings")
midi_table[44] = ("tremolo_strings", "strings")
midi_table[45] = ("pizzicato_strings", "strings")
midi_table[46] = ("orchestral_harp", "strings")
midi_table[47] = ("timpani", "strings")
midi_table[48] = ("string_ensemble_1", "strings")
midi_table[49] = ("string_ensemble_2", "strings")
midi_table[50] = ("synth_strings_1", "strings")
midi_table[51] = ("synth_strings_2", "strings")
midi_table[52] = ("choir_aahs", "strings")
midi_table[53] = ("voice_oohs", "strings")
midi_table[54] = ("synth_voice", "strings")
midi_table[55] = ("orchestra_hit", "strings")
midi_table[56] = ("trumpet", "brass")
midi_table[57] = ("trombone", "brass")
midi_table[58] = ("tuba", "brass")
midi_table[59] = ("muted_trumpet", "brass")
midi_table[60] = ("french_horn", "brass")
midi_table[61] = ("brass_section", "brass")
midi_table[62] = ("synth_brass_1", "brass")
midi_table[63] = ("synth_brass_2", "brass")
midi_table[64] = ("soprano_sax", "reed")
midi_table[65] = ("alto_sax", "reed")
midi_table[66] = ("tenor_sax", "reed")
midi_table[67] = ("baritone_sax", "reed")
midi_table[68] = ("oboe", "reed")
midi_table[69] = ("english_horn", "reed")
midi_table[70] = ("bassoon", "reed")
midi_table[71] = ("clarinet", "reed")
midi_table[72] = ("piccolo", "pipe")
midi_table[73] = ("flute", "pipe")
midi_table[74] = ("recorder", "pipe")
midi_table[75] = ("pan_flute", "pipe")
midi_table[76] = ("blown_bottle", "pipe")
midi_table[77] = ("shakuhachi", "pipe")
midi_table[78] = ("whistle", "pipe")
midi_table[79] = ("ocarina", "pipe")
midi_table[80] = ("lead_1_square", "synth lead")
midi_table[81] = ("lead_2_sawtooth", "synth lead")
midi_table[82] = ("lead_3_calliope", "synth lead")
midi_table[83] = ("lead_4_chiff", "synth lead")
midi_table[84] = ("lead_5_charang", "synth lead")
midi_table[85] = ("lead_6_voice", "synth lead")
midi_table[86] = ("lead_7_fifths", "synth lead")
midi_table[87] = ("lead_8_bass_+_lead", "synth lead")
midi_table[88] = ("pad_1_new_age", "synth pad")
midi_table[89] = ("pad_2_warm", "synth pad")
midi_table[90] = ("pad_3_polysynth", "synth pad")
midi_table[91] = ("pad_4_choir", "synth pad")
midi_table[92] = ("pad_5_bowed", "synth pad")
midi_table[93] = ("pad_6_metallic", "synth pad")
midi_table[94] = ("pad_7_halo", "synth pad")
midi_table[95] = ("pad_8_sweep", "synth pad")
midi_table[96] = ("fx_1_rain", "synth effects")
midi_table[97] = ("fx_2_soundtrack", "synth effects")
midi_table[98] = ("fx_3_crystal", "synth effects")
midi_table[99] = ("fx_4_atmosphere", "synth effects")
midi_table[100] = ("fx_5_brightness", "synth effects")
midi_table[101] = ("fx_6_goblins", "synth effects")
midi_table[102] = ("fx_7_echoes", "synth effects")
midi_table[103] = ("fx_8_sci-fi", "synth effects")
midi_table[104] = ("sitar", "ethnic")
midi_table[105] = ("banjo", "ethnic")
midi_table[106] = ("shamisen", "ethnic")
midi_table[107] = ("koto", "ethnic")
midi_table[108] = ("kalimba", "ethnic")
midi_table[109] = ("bag_pipe", "ethnic")
midi_table[110] = ("fiddle", "ethnic")
midi_table[111] = ("shanai", "ethnic")
midi_table[112] = ("tinkle_bell", "percussive")
midi_table[113] = ("agogo", "percussive")
midi_table[114] = ("steel_drums", "percussive")
midi_table[115] = ("woodblock", "percussive")
midi_table[116] = ("taiko_drum", "percussive")
midi_table[117] = ("melodic_tom", "percussive")
midi_table[118] = ("synth_drum", "percussive")
midi_table[119] = ("reverse_cymbal", "sound effects")
midi_table[120] = ("guitar_fret_noise", "sound effects")
midi_table[121] = ("breath_noise", "sound effects")
midi_table[122] = ("seashore", "sound effects")
midi_table[123] = ("bird_tweet", "sound effects")
midi_table[124] = ("telephone_ring", "sound effects")
midi_table[125] = ("helicopter", "sound effects")
midi_table[126] = ("applause", "sound effects")
midi_table[127] = ("gunshot", "sound effects")

notes_list = ["C-1", "C#-1", "D-1", "D#-1", "E-1", "F-1", "F#-1", "G-1", "G#-1", "A-1", "A#-1", "B-1", "C0", "C#0", "D0", "D#0", "E0", "F0", "F#0", "G0", "G#0", "A0", "A#0", "B0", "C1", "C#1", "D1", "D#1", "E1", "F1", "F#1", "G1", "G#1", "A1", "A#1", "B1", "C2", "C#2", "D2", "D#2", "E2", "F2", "F#2", "G2", "G#2", "A2", "A#2", "B2", "C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", "A3", "A#3", "B3", "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4", "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5", "B5", "C6", "C#6", "D6", "D#6", "E6", "F6", "F#6", "G6", "G#6", "A6", "A#6", "B6", "C7", "C#7", "D7", "D#7", "E7", "F7", "F#7", "G7", "G#7", "A7", "A#7", "B7", "C8", "C#8", "D8", "D#8", "E8", "F8", "F#8", "G8", "G#8", "A8", "A#8", "B8", "C9", "C#9", "D9", "D#9", "E9", "F9", "F#9", "G9"]


def midi_family_to_instruments(family):
    instruments = []
    for index in range(128):
        if midi_table[index][1] == family:
            instruments.append(index)
    return tuple(instruments)


def get_midi_instrument_by_name(name):
    for index in range(128):
        if midi_table[index][0] == name:
            return index
    return None


def program_to_name(program):
    return midi_table[program][0]


def program_to_family(program):
    return midi_table[program][1]