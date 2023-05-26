# Serenity

[Desired domain name](https://uk.godaddy.com/domainsearch/find?checkAvail=1&domainToCheck=meetserenity.co.uk)

We need to install FFMPEG to run the audio stuff, which can be found [here](https://stackoverflow.com/questions/56370173/how-to-export-ffmpeg-into-my-python-program)

## Installation

This project requires Python 3.10 to be installed, which can be found [here](https://www.python.org/downloads/), as well as FFMPEG, which can be found at [This direct link](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z). You should also run:
`python -m pip install -r requirements.txt` so all the packages are downloaded properly.
You'll also need to create a bunch of key files, `aws_access_keys.txt` (aws_access_key_id and aws_secret_access_key), `deep_gram.txt`, (just the raw key)
`openai_key.txt` (just the raw key), `eleven_labs_dev_key.txt` (just the raw key), and `eleven_labs_keys.txt`, (list of keys, one per line)

The CodeTour VSCode plugin should also be installed, which will guide you around the code base.

## Linting, CI/CD

Black is used to format the code, using the command: `black . --line-length 140`, and mypy with `mypy . --strict`. Pygount also can be run with `pygount --format=summary --verbose --folders-to-skip="[...],*__pycache__,.vscode,.mypy_cache,.git,__pycache__,build" .` to get a summary of the codebase.
