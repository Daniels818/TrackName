# TrackName

![Python](https://img.shields.io/badge/python-3.8%2B-blue?logo=python&logoColor=white)
![API](https://img.shields.io/badge/API-Genius%20%7C%20lyrics.ovh-yellow)

TrackName is a powerful command-line tool to discover and manage songs. Search for songs by **title**, **artist name**, or even **a fragment of the lyrics**. View rich song details, read lyrics previews, and manage your search history and favorite tracks locally.

## Features

- **Search by Title & Artist:** Fast search powered by the Genius API.
- **Search by Lyrics (`:lyrics`):** Can't remember the name of a song? Type a snippet of the lyrics to find it, powered by the lyrics.ovh API.
- **Rich Song Details:** View the album, release year, view count, annotations, featured artists, song description, and a preview of the lyrics right in your terminal.
- **Favorites (`:favorites`):** Save your favorite songs locally to keep track of your top discoveries.
- **Search History (`:history`):** TrackName automatically saves your search history so you can easily review your recent queries. You can also clear it anytime with `:clear`.
- **Robust Error Handling:** Safely handles network timeouts, missing fields, and API rate limits.

## Requirements

- Python 3.8 or higher
- `requests`
- `beautifulsoup4`

## Installation

```bash
git clone https://github.com/Daniels818/TrackName.git
cd TrackName
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
   Add that line to `~/.bashrc` or `~/.zshrc` to make it permanent.

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

Start the interactive CLI by running:

```bash
python main.py
```

### Standard Search
Simply type a song name, an artist, or both.
```
  Search - or type :history, :favorites, :clear, or 'q' to quit: Queen Bohemian Rhapsody
```

### Special Commands
- `:lyrics` — Search for a song using a snippet of its lyrics.
- `:history` — Show your last 10 searches.
- `:favorites` — List all your saved favorite songs.
- `:clear` — Clear your search history.
- `q`, `quit`, `exit` — Exit the application.

## Testing

To run the automated test suite (30+ robust unit tests):

```bash
python -m unittest discover
```

## Project Structure

```text
trackname/
├── main.py              # Starts the command-line app
├── trackname/
│   ├── api.py           # Genius API calls and response validation
│   ├── cli.py           # Interactive command-line flow
│   ├── details.py       # Fetching detailed song data & lyrics previews
│   ├── display.py       # Console result formatting
│   ├── lyrics_search.py # Lyrics fragment search via lyrics.ovh
│   ├── storage.py       # Local persistence for history and favorites
│   └── text.py          # Query cleanup helpers
├── tests/               # Unit tests 
├── requirements.txt     # Third-party dependencies
└── README.md            # You are here
```
