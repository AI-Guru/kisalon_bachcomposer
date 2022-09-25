# If there are not exactly 2 arguments to the script, then give user help.
if [ $# -ne 2 ]
then
    echo "Usage: $0 command target"
exit
fi

if [ $1 == "hordak" ]; then
    USERNAME=hordak
    HOST=192.168.2.111
    PORT=22
    TARGETPATH=Development/chordcomposer
    SERVERURL=welt.de
elif [ $1 == "bruno" ]; then
    USERNAME=tristan
    HOST=6uay30l3zpqwv5eg.myfritz.net
    PORT=3322
    TARGETPATH=Development/chordcomposer
    SERVERURL=http://6uay30l3zpqwv5eg.myfritz.net:3313
elif [ $1 == "studio" ]; then
    USERNAME=tristan
    HOST=6uay30l3zpqwv5eg.myfritz.net
    PORT=3323
    TARGETPATH=Development/chordcomposer
    SERVERURL=http://6uay30l3zpqwv5eg.myfritz.net:3308

elif [ $1 == "local" ]; then
    USERNAME=tristan

else
    echo "Error: Unknown target."
    exit

fi

# If argument is "model", then copy model.
if [ $2 = "importbin" ]; then
    rm -rf bin
    mkdir -p bin/
    SOUNDFONTPATH="/Users/tristanbehrens/Datasets/soundfonts/arachno-soundfont-10-sf2/Arachno SoundFont - Version 1.0.sf2"
    cp "$SOUNDFONTPATH" bin/soundfont.sf2
fi

# If argument is "uploadapp", then upload app.
if [ $2 = "uploadapp" ]; then
    ssh -p $PORT $USERNAME@$HOST "mkdir -p $TARGETPATH"
    ssh -p $PORT $USERNAME@$HOST "mkdir -p $TARGETPATH/source"
    ssh -p $PORT $USERNAME@$HOST "mkdir -p $TARGETPATH/templates"
    ssh -p $PORT $USERNAME@$HOST "mkdir -p $TARGETPATH/static"
    scp -P $PORT app.py $USERNAME@$HOST:$TARGETPATH
    scp -P $PORT instruments_synth.json $USERNAME@$HOST:$TARGETPATH
    scp -P $PORT chord_progressions.json $USERNAME@$HOST:$TARGETPATH
    scp -P $PORT source/*.py $USERNAME@$HOST:$TARGETPATH/source
    scp -P $PORT templates/*.html $USERNAME@$HOST:$TARGETPATH/templates
    scp -P $PORT static/*.css $USERNAME@$HOST:$TARGETPATH/static
    scp -P $PORT static/*.js $USERNAME@$HOST:$TARGETPATH/static
fi

# If argument is "uploadcredentials", then upload credentials.
if [ $2 = "uploadcredentials" ]; then
    scp -P $PORT active_tokens.txt $USERNAME@$HOST:$TARGETPATH
fi

# If argument is "uploadbin", then upload model.
if [ $2 = "uploadbin" ]; then
    echo "Uploading bin..."
    ssh -p $PORT $USERNAME@$HOST "mkdir -p $TARGETPATH/bin"
    scp -P $PORT -r bin $USERNAME@$HOST:$TARGETPATH
fi

# Just ssh login.
if [ $2 = "login" ]; then
    ssh -p $PORT $USERNAME@$HOST
fi

# Cat server log.
if [ $2 = "log" ]; then
    ssh -p $PORT $USERNAME@$HOST "cat $TARGETPATH/server.log"
fi

# Create an active token.
if [ $2 = "createtoken" ]; then
    python create_auth_token.py
    scp -P $PORT active_tokens.txt $USERNAME@$HOST:$TARGETPATH
fi

# Cat active tokens.
if [ $2 = "activetokens" ]; then
    ssh -p $PORT $USERNAME@$HOST "cat $TARGETPATH/active_tokens.txt"
fi

# Open in browser.
if [ $2 = "browser" ]; then
    open $SERVERURL
fi

# Download midis and exceptions.
if [ $2 = "download" ]; then
    REMOTEPATH=./remote/$1
    mkdir -p $REMOTEPATH
    scp -P $PORT -r $USERNAME@$HOST:$TARGETPATH/midi $REMOTEPATH/
    scp -P $PORT -r $USERNAME@$HOST:$TARGETPATH/exceptions $REMOTEPATH/
fi

# If argument is "uploadapp", then upload app.
if [ $2 = "downloadchords" ]; then
    scp -P $PORT $USERNAME@$HOST:$TARGETPATH/chord_progressions.json .
fi

# If argument is "restart" then restart server.
if [ $2 = "restart" ]; then
    ssh -p $PORT $USERNAME@$HOST "sudo -S service retrofuturesynthcomposer restart"
fi