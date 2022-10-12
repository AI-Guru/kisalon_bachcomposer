import json

def fancy_indexing(list, indices):
    return [list[index] for index in indices]

DEFAULT_DENSITY = 6

class Composer:

    def __init__(self, tokenizer, model, device):
        self.tokenizer = tokenizer
        self.model = model
        self.device = device
        self.number_of_bars = 4

    def compose_song(self, command_parameters):

        print(command_parameters["temperature"])

        instrument_tokens = ["INST=0", "INST=24", "INST=32", "INST=48"]

        # Get the tokens. 
        # Do not use all. Only use the instruments that are not EMPTY.
        song_data = {}
        song_data["instrument_tokens"] = instrument_tokens
        song_data["tracks"] = []

        # Get the temperature.
        temperature = float(command_parameters["temperature"])

        # Get the density.
        #density = int(command_parameters["density"])
        density = DEFAULT_DENSITY

        # Go through all instruments.
        for instrument_index in range(len(song_data["instrument_tokens"])):

            # Go through all bars.
            for bar_index in range(self.number_of_bars):

                # Compose that one.
                self.__compose(instrument_index, bar_index, song_data, temperature, density)

        # Generate token sequence from song data.
        token_sequence = self.__song_data_to_token_sequence(song_data)
        return token_sequence

    def redo_track(self, command_parameters):

        # Check if everything is there.
        assert "redo_instrument_index" in command_parameters
        assert "token_sequence" in command_parameters
        assert "temperature" in command_parameters

        # Get the density.
        density = DEFAULT_DENSITY

        # Map the token sequence to song data.
        song_data = self.__token_sequence_to_song_data(command_parameters["token_sequence"])

        # Get the instrument index.
        redo_instrument_index = command_parameters["redo_instrument_index"]
        assert isinstance(redo_instrument_index, int)

        # Get the instrument token.
        redo_instrument_token = song_data["instrument_tokens"][redo_instrument_index]

        # Remove instrument token from song data at redo instrument index. After that insert the redo one.
        del song_data["instrument_tokens"][redo_instrument_index]
        song_data["instrument_tokens"].append(redo_instrument_token)

        # Remove the track data from song data at redo instrument index.
        del song_data["tracks"][redo_instrument_index]

        # Get the temperature.
        temperature = float(command_parameters["temperature"])

        # Get the density.
        #density = int(command_parameters["density"])
        density = DEFAULT_DENSITY

        # Now comes the actual recomposition.
        # Go through all bars.
        for bar_index in range(self.number_of_bars):

            # Compose that one.
            self.__compose(3, bar_index, song_data, temperature, density)

        # Check if everything is okay.
        assert len(song_data["instrument_tokens"]) == 4
        assert len(song_data["tracks"]) == 4

        # See if intrument tokens and tracks instruments tokens match.
        for track_index in range(len(song_data["tracks"])):
            assert song_data["tracks"][track_index]["instrument_token"] == song_data["instrument_tokens"][track_index]

        # Reinstert at specific index, shift everything else to the right.
        def reinsert(index, list):
            element = list[-1]
            del list[-1]
            list.insert(index, element)
            return list

        # Apply the permutation to instrument tokens, density tokens and tracks.
        song_data["instrument_tokens"] = reinsert(redo_instrument_index, song_data["instrument_tokens"])
        song_data["tracks"] = reinsert(redo_instrument_index, song_data["tracks"])

        # Generate token sequence from song data.
        token_sequence = self.__song_data_to_token_sequence(song_data)
        return token_sequence

    def __compose(self, track_index, bar_index, song_data, temperature, density):

        #assert len(song_data["tracks"]) == len(song_data["instrument_tokens"])

        if len(song_data["tracks"]) <= track_index:
            track_data = {}
            track_data["instrument_token"] = song_data["instrument_tokens"][track_index]
            assert isinstance(track_data["instrument_token"], str)
            track_data["bars"] = []
            song_data["tracks"].append(track_data)
        track_data = song_data["tracks"][track_index]

        # Create the token sequence for composition.
        token_sequence = []
        token_sequence += ["PIECE_START STYLE=JSFAKES GENRE=JSFAKES"]

        # Add tokens for the previous tracks.
        for other_track_index in range(0, track_index):
            token_sequence += self.__get_other_track_tokens_for_generation(bar_index, other_track_index, song_data, density)

        # Add the tokens to start the track.
        token_sequence += ["TRACK_START"]
        token_sequence += [track_data["instrument_token"]]
        token_sequence += [f"DENSITY={density}"]

        # Add tokens for the previous bars.
        token_sequence += self.__get_bar_tokens_for_generation(bar_index, track_data)

        # Add a new bar token.
        token_sequence += ["BAR_START"]

        # Generate the next bar.
        token_sequence = " ".join(token_sequence)

        generated_token_sequence = self.__generate(token_sequence, "BAR_END", temperature=temperature).split(" ")

        track_data["bars"].append(["BAR_START"] + generated_token_sequence)

    def __get_other_track_tokens_for_generation(self, bar_index, other_track_index, song_data, density):
        if bar_index < 4:
            start_index = 0
        else:
            start_index = bar_index - 3 # TODO Sure this is three?
        end_index = start_index + 4

        track_tokens = []
        track_tokens += ["TRACK_START"]
        track_tokens += [song_data["instrument_tokens"][other_track_index]]
        track_tokens += [f"DENSITY={density}"]

        for index in range(start_index, end_index):
            track_tokens += song_data["tracks"][other_track_index]["bars"][index]

        track_tokens += ["TRACK_END"]

        return track_tokens

    def __get_bar_tokens_for_generation(self, bar_index, track_data):
        start_index = bar_index - 3
        start_index = max(0, start_index)
        end_index = bar_index
        end_index = max(0, end_index)

        bar_tokens = []
        for bar_data in track_data["bars"][start_index:end_index]:
            bar_tokens += bar_data

        return bar_tokens
        

    def __generate(self, token_sequence, end_token, temperature):
        assert isinstance(token_sequence, str)

        # Encode input.
        input_ids = self.tokenizer.encode(token_sequence, return_tensors="pt").to(self.device)
        
        eos_token_id = self.tokenizer.encode(end_token)[0] if "end_token" != None else None

        # Generate.
        print(temperature)
        generated_token_sequence = self.model.generate(
            input_ids,
            max_length=2048,
            do_sample=True,
            temperature=temperature,
            eos_token_id=eos_token_id,
        )

        generated_token_sequence = self.tokenizer.decode(generated_token_sequence[0][len(input_ids[0]):])
        return generated_token_sequence

    def __song_data_to_token_sequence(self, song_data):

        token_sequence = []
        token_sequence += ["PIECE_START"]

        # Add all tracks.
        for track_data in song_data["tracks"]:
            token_sequence += ["TRACK_START"]

            # Add instrument.
            token_sequence += [track_data["instrument_token"]]

            # Add all bars.
            for bar_data in track_data["bars"]:
                token_sequence += bar_data

            # End of track.
            token_sequence += ["TRACK_END"]

        # Return a string.
        token_sequence = " ".join(token_sequence)
        return token_sequence


    def __token_sequence_to_song_data(self, token_sequence):

        # Split token sequence along TRACK_START.
        token_sequences = token_sequence.split(" TRACK_START ")
        for index in range(1, len(token_sequences)):
            token_sequences[index] = "TRACK_START " + token_sequences[index]
        
        # Ignore the first element. It is PIECE_START.
        token_sequences = token_sequences[1:]

        # Start with the song data.
        song_data = {}

        # Chord tokens. They are empty because they are not in the token sequence.
        song_data["chord_tokens"] = []

        # Get instrument tokens and density tokens.
        song_data["instrument_tokens"] = []
        for token_sequence in token_sequences:
            token_sequence_split = token_sequence.split(" ")
            
            instrument_token = token_sequence_split[1]
            assert instrument_token.startswith("INST=")
            song_data["instrument_tokens"] += [instrument_token]

        # Density tokens. They are empty because they are not in the token sequence.            
        song_data["density_tokens"] = []

        # Create the song data.
        song_data["tracks"] = []
        for token_sequence in token_sequences:

            # Split.                
            token_sequence_split = token_sequence.split(" ")

            # Get the instrument token.
            instrument_token = token_sequence_split[1]
            assert instrument_token.startswith("INST=")

            # Create the track data.
            track_data = {}
            track_data["instrument_token"] = instrument_token

            # Add the track data to the song data.
            song_data["tracks"] += [track_data]

            # Get all the indices of BAR_START and BAR_END.
            bar_start_indices = []
            bar_end_indices = []
            for index in range(len(token_sequence_split)):
                if token_sequence_split[index] == "BAR_START":
                    bar_start_indices += [index]
                if token_sequence_split[index] == "BAR_END":
                    bar_end_indices += [index]

            # Get all the bars.
            bar_tokens = []
            for index in range(len(bar_start_indices)):
                bar = token_sequence_split[bar_start_indices[index]:bar_end_indices[index] + 1]
                bar_tokens += [bar]
            track_data["bars"] = bar_tokens

        return song_data
