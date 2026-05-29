# Smart Lyrics

![Python](https://img.shields.io/badge/python-3.8%2B-blue?logo=python&logoColor=white)
![API](https://img.shields.io/badge/API-Genius-yellow)

Search for songs by **title**, **artist name**, or both — powered by the Genius API. Get the top 5 matching results instantly with direct links to the full lyrics on Genius.

> **Why title/artist instead of lyrics?**  
> The Genius API `/search` endpoint indexes song titles and artist metadata,
> not the actual lyric text. Searching by lyric fragment returns unreliable
> results, so this tool embraces what the API actually does well.

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

```bash
python main.py
```

An interactive prompt will appear. You can search by:

| Input style | Example |
|---|---|
| Song title only | `Bohemian Rhapsody` |
| Artist name only | `Queen` |
| Title + artist | `Queen Bohemian Rhapsody` |

```
=======================================================
  SMART LYRICS — Song search by title or artist
=======================================================

  Tips:
    • Search by song title     →  Bohemian Rhapsody
    • Search by artist name    →  Queen
    • Combine both             →  Queen Bohemian Rhapsody

  Search (title / artist / both) — or 'q' to quit: The Weeknd Blinding Lights

  1. Blinding Lights — The Weeknd (November 29, 2019)
     https://genius.com/The-weeknd-blinding-lights-lyrics

  2. Blinding Lights (Remix) — The Weeknd (April 24, 2020)
     https://genius.com/The-weeknd-blinding-lights-remix-lyrics

  Press Enter to continue...
```

Type `q` to quit.

## Project Structure

```
smart-lyrics-en/
├── main.py            # All the logic lives here
├── requirements.txt   # Third-party dependencies
├── .gitignore         # Files Git should not track
└── README.md          # You are here
```
