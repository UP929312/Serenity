# Serenity

[Desired domain name](https://uk.godaddy.com/domainsearch/find?checkAvail=1&domainToCheck=meetserenity.co.uk)

We need to install FFMPEG to run the audio stuff, which can be found [here](https://stackoverflow.com/questions/56370173/how-to-export-ffmpeg-into-my-python-program)

Control Shift V to view markdown.

## Installation

This project requires Python 3.10 to be installed, which can be found [here](https://www.python.org/downloads/), as well as FFMPEG, which can be found at [This direct link](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z). You should also run:
`python -m pip install -r requirements.txt` so all the packages are downloaded properly.
You'll also need to create a bunch of key files, `aws_access_keys.txt` (aws_access_key_id and aws_secret_access_key), `deep_gram.txt`, (just the raw key)
`openai_key.txt` (just the raw key), `eleven_labs_dev_key.txt` (just the raw key), and `eleven_labs_keys.txt`, (list of keys, one per line)

The CodeTour VSCode plugin should also be installed, which will guide you around the code base.

## Linting, CI/CD

Black is used to format the code, using the command: `black . --line-length 140`, and mypy with `mypy . --strict`. Pygount also can be run with `pygount --format=summary --verbose --folders-to-skip="[...],*__pycache__,.vscode,.mypy_cache,.git,__pycache__,build" .` to get a summary of the codebase.

## Todo list

### Ben

- Integrate the real time audio transcription and the recording polling
  - Fully implemented, run using a different engine in non-real time.
- Write a lot of tests and probably some CI stuff too
  - Most tests done, CI not yet (e.g. building to .exe)
- Benchmark processing requirements, and estimate pricing costs for 1 minute of using the app
  - More progress required with prototype
- Implement secondary audio translation in the background, and update the history to include that instead.
  - Need to implement async/threaded audio playing first.
- Documentation
  - Documentation mostly written, writeups done too, forever task.
- Convert the Agent's speech audio into a list of phonemes, using [this](https://github.com/xinjli/allosaurus), which can be pipelined into Vito's animated agent model, with timestamps
  - Done, outputs a list of dicts, with timestamp, duration and phoneme, Vito's avatar needs to implement all the sounds it can output
- Work on compilation to a single exe which the user can seamlessly run
  - This is really hard, will keep progressing.
- Get a github.io page for our sales pages
  - Will do later.
- Deepgram params not working
  - Fixed on their side by my PR: [here](https://github.com/deepgram/deepgram-python-sdk/pull/90)

### Vito

- Prompt engineering - Initial prompt, update prompts, system prompt (for setting who the AI is) (also not to use emojis, and try to keep it only saying A-Z for TTS)
- LLM interfacing - Figure out how to combine all our metrics into the request, similar to above
- Vector Database research - Look into one that we should use
- Training - Giving the Agent the knowledge of someone who's done a degree, requires Francesco's assistance in finding good literature.

 __Low priority:__

- Animated Character prototype - Take a string emotion such as "happy", "confused", or "listening", and return a video of an animated character
  - Also needs to be able to pipe in a list of timestamps and phonemes and the face will speak them outloud

### Francesco

- Assist with finding literature for the LLM
- Create contact train with friend with Law background to assist with legalese.
- Write a list of "key words". These words will be prioritised by Speech-to-text. My best guess for a few of these words will be: `["serenity", "sad", "depressed", "feelings", "thoughts"]` etc
