# Smart Lyrics

![Python](https://img.shields.io/badge/python-3.8%2B-blue?logo=python&logoColor=white)
![API](https://img.shields.io/badge/API-Genius-yellow)

Search for songs by lyric fragment using the Genius API. Type a piece of a song you remember and get the top 5 matching results instantly — no account needed to run it, just a free API token.

## Requirements

- Python 3.8 or higher
- pip

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

You need a free Genius API token (takes about 2 minutes to set up).

1. Sign up at https://genius.com/api-clients
2. Create an app and copy the **Client Access Token**
3. Set the environment variable:

   **Linux / macOS:**
   ```bash
   export GENIUS_ACCESS_TOKEN='your_token_here'
   ```
   Add that line to `~/.bashrc` or `~/.zshrc` to make it permanent across sessions.

   **Windows — PowerShell:**
   ```powershell
   $env:GENIUS_ACCESS_TOKEN = "your_token_here"
   ```
   To make it permanent, use `setx` in CMD:
   ```cmd
   setx GENIUS_ACCESS_TOKEN "your_token_here"
   ```
   Then open a new terminal window for the change to take effect.

## Usage

```bash
python main.py
```

An interactive prompt will appear. Type any lyric fragment and press Enter — the script will show up to 5 matching songs with links to the full lyrics on Genius. Type `q` to quit.

```
=======================================================
  SMART LYRICS — Song lyrics search engine
=======================================================

  Enter a lyric fragment (or 'q' to quit): blinded by the lights

  1. Blinded by the Lights — The Streets (May 17, 2004)
     https://genius.com/The-streets-blinded-by-the-lights-lyrics

  2. Blinded By The Lights — Dan Caplen (November 22, 2016)
     https://genius.com/Dan-caplen-blinded-by-the-lights-lyrics

  Press Enter to continue...
```

## Project Structure

```
smart-lyrics-en/
├── main.py            # All the logic lives here
├── requirements.txt   # Third-party dependencies
├── .gitignore         # Files Git should not track
├── LICENSE            # MIT License
└── README.md          # You are here
```

## License

Distributed under the [MIT License](LICENSE).
