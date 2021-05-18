# discord-go-gif-bot

A interactive discord bot for playing out sgf games & variations as gifs

credit goes to
- https://github.com/rooklift/sgf_to_gif 
golang library for converting sgf files to gif.

I copied his source code and placed it in `sgf_to_gif.go` here. All credit goes to rooklift.

To compile it, install golang then run `go build sgf_to_gif.go` to get the compiled executable `sgf_to_gif`, and then place it in this same directory (project root).
The `sgf_to_gif` executable needs to be placed in project root before running `python3 main.py` (the discord bot), since the bot relies on that (and expects it in project root).

- https://github.com/mattheww/sgfmill
python lib for parsing and manipulating sgf files

this project is mostly glue code around those libraries, so thanks to the lib authors.

note that the discord bot token needs to be set as `DISCORD_BOT_TOKEN` in a `.env` file in project root (our bot will read from this file).

## Docker support
After setting `DISCORD_BOT_TOKEN` in the `.env` in project root, and making sure that we `cd` into project root,
run `docker build . -t discord-go-gif-bot` (might take a minute or two)
then run `docker run -it discord-go-gif-bot`.



License: MIT

![alt text](./screenshot.png "Logo Title Text 1")

