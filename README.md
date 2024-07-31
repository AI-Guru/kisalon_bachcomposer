# kisalon_bachcomposer
## Copyright 2022 Dr. Tristan Behrens

![](static/songimage.jpg)

Here is a video:
https://www.youtube.com/watch?v=z1p4dhLLMYg

## Installation

The best way to get everything up and running is Docker.

Build the docker container: 

```
docker build -t kisalon_bachcomposer .
```

Now let us run the app. Do not forget to fill in the blanks:

```
docker run --rm -it -p 5001:5001 kisalon_bachcomposer
```
