function compose_button_clicked() {

    set_busy(true);

    // Get the values.
    var temperature = get_select_button_value("temperature");
    var instrument = get_select_button_value("instrument");
    var bpm = get_select_button_value("tempo");
    var density = get_select_button_value("density");

    // Put everything into a JSON object.
    var json_object = {
        "instrument": instrument,
        "bpm": bpm,
        "temperature": temperature,
        "density": density
    };

    // Post the command.
    post_command("compose", json_object, completion_callback=(response) => {
        set_busy(false);
    } );
}


function redo_button_clicked(redo_instrument_index) {

    // Get the values.
    var temperature = get_select_button_value("temperature");
    var instrument = get_select_button_value("instrument");
    var bpm = get_select_button_value("tempo");
    var density = get_select_button_value("density");

    // Get token sequence.
    var token_sequence = document.getElementById("tokens_placeholder").innerHTML;

    // Do not do anything if token sequence is empty.
    if (token_sequence == "") {
        return;
    }

    // Create the command.
    var command_name = "redo";
    var command_parameters = {
        "redo_instrument_index": redo_instrument_index,
        "token_sequence": token_sequence,
        "instrument": instrument,
        "bpm": bpm,
        "temperature": temperature,
        "density": density
    };

    // Post the command.
    post_command(command_name, command_parameters);

}


function get_auth_token() {

    // Get the auth token from the session.
    var auth_token = sessionStorage.getItem("auth_token");
    return auth_token;

}


function play_token_sequence() {

    // Get the token sequence.
    var token_sequence = document.getElementById("tokens_placeholder").innerHTML;
    if (token_sequence == "") {
        return;
    }

    set_busy(true);

    // Get the values.
    var temperature = get_select_button_value("temperature");
    var instrument = get_select_button_value("instrument");
    var bpm = get_select_button_value("tempo");
    var density = get_select_button_value("density");


    // Put everything into a JSON object.
    var json_object = {
        "token_sequence": token_sequence,
        "instrument": instrument,
        "bpm": bpm,
        "temperature": temperature,
        "density": density
    };

    post_command("play", json_object, completion_callback=(response) => {
        set_busy(false);
    } );

}

function post_command(command_name, command_parameters, completion_callback=null) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/command", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader('Authorization', "Bearer " + get_auth_token());
    xhr.send(JSON.stringify({command_name: command_name, command_parameters: command_parameters}));

    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.status == "OK") {

                // check if response has the property svg
                if (response.svg) {
                    document.getElementById("svg_placeholder").innerHTML = response.svg;
                }

                if (response.token_sequence) {
                    document.getElementById("tokens_placeholder").innerHTML = response.token_sequence;
                }

                if (response.audio_data) {
                    var audio_data = response.audio_data;
                    var audio_element = document.getElementById("audio");
                    audio_element.src = "data:audio/wav;base64," + audio_data;
                    audio_element.play();
                }
                
            }
            else {
                alert("Error: " + response.error);
            }
            
        }
        else if (xhr.readyState == 4 && xhr.status == 401) {
            alert("Error: Unauthorized");

            // Redirect to the login page.
            window.location.href = "/";
        }

        if (completion_callback) {
            completion_callback();
        }
    }
}

function set_busy(busy) {
    if (busy) {
        document.body.style.pointerEvents = "none";
        document.body.style.userSelect = "none";
        document.getElementById("overlay").style.display = "block";
    }
    else {
        document.body.style.pointerEvents = "auto";
        document.body.style.userSelect = "auto";
        document.getElementById("overlay").style.display = "none";
    }

}

function select_button_clicked(the_button, recompose=false) {

    // Get the group attribute.
    var group = the_button.getAttribute("group");

    // Find all the button tags with class select-button.
    var select_buttons = document.getElementsByClassName("select-button");

    // Get all those that have the same group.
    var select_buttons_in_group = [];
    for (var i = 0; i < select_buttons.length; i++) {
        var select_button = select_buttons[i];
        if (select_button.getAttribute("group") == group) {
            select_buttons_in_group.push(select_button);
        }
    }

    // For each of the buttons remove the class button-active and add the class button-inactive.
    for (var i = 0; i < select_buttons_in_group.length; i++) {
        var select_button = select_buttons_in_group[i];
        select_button.classList.remove("button-active");
        select_button.classList.add("button-inactive");
    }

    // Add the class button-active to the clicked button.
    the_button.classList.remove("button-inactive");
    the_button.classList.add("button-active");

    if (recompose) {
        compose_button_clicked();
    }
    else {
        play_token_sequence();
    }

}

function get_select_button_value(group) {
    
    // Find all the button tags with class instrument-button and class button-active.
    var instrument_buttons = document.getElementsByClassName("select-button button-active");

    // Get all those that have the same group.
    var instrument_buttons_in_group = [];
    for (var i = 0; i < instrument_buttons.length; i++) {
        var instrument_button = instrument_buttons[i];
        if (instrument_button.getAttribute("group") == group) {
            instrument_buttons_in_group.push(instrument_button);
        }
    }

    // If there is one, return the instrument token.
    if (instrument_buttons_in_group.length == 1) {
        return instrument_buttons_in_group[0].getAttribute("value");
    }

    alert("Error: No instrument selected.");
}
