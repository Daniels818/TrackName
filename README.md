# TrackName

![Python](https://img.shields.io/badge/python-3.8%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/flask-3.0%2B-lightgrey?logo=flask&logoColor=white)
![API](https://img.shields.io/badge/API-Genius%20%7C%20lyrics.ovh-yellow)

TrackName is a powerful, dual-interface music discovery and management tool. Search for songs by **title**, **artist name**, or even **a fragment of the lyrics**. View rich song details, read lyrics previews, and manage your search history and favorite tracks locally. 

You can run TrackName as a **Command-Line Interface (CLI)** or launch the modern, dark-themed **Web Application (GUI)**.

---

## Features

### 🔍 Search & Discovery
- **Search by Title & Artist:** Fast search powered by the Genius API.
- **Search by Lyrics:** Can't remember the name of a song? Type a snippet of the lyrics to find it, powered by the lyrics.ovh API.
- **Rich Song Details:** Fetch release year, view count, annotations, featured artists, song description, and a preview of the lyrics.

### 💾 Local Management & Personalization
- **Favorites:** Save your favorite songs locally to keep track of your top discoveries.
- **Search History:** Automatically track your search history so you can review recent queries or clear them at any time.

### 🌐 Dual Interface Support
- **Interactive CLI:** A terminal interface featuring clean console layouts, quick shortcuts, and robust text-based menus.
- **Modern Web GUI:** A beautiful, responsive dark-mode web dashboard built with vanilla CSS glassmorphism, smooth animations, and clean navigation.

---

## Requirements

- Python 3.8 or higher
- Flask 3.0+
- Beautiful Soup 4
- Requests

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Daniels818/TrackName.git
   cd TrackName
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

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

   **Windows — CMD:**
   ```cmd
   setx GENIUS_ACCESS_TOKEN "your_token_here"
   ```
   *Note: Open a new terminal window after setting environment variables with `setx` for changes to take effect.*

---

## Usage

### 🖥️ Web UI (Flask Web Application)
Launch the web interface locally by running:
```bash
python app.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

#### Web Features:
- Glassmorphic, modern dark-themed user interface.
- Complete search by text or lyrics.
- Smooth transitions and interactive cards.
- Favorites management dashboard.
- Live search history view with one-click cleanup.

### 📟 CLI (Command-Line Interface)
Start the interactive command-line app by running:
```bash
python main.py
```

#### CLI Special Commands:
- `:lyrics` — Search for a song using a snippet of its lyrics.
- `:history` — Show your last 10 searches.
- `:favorites` — List all your saved favorite songs.
- `:clear` — Clear your search history.
- `q`, `quit`, `exit` — Exit the application.

---

## Testing

To run the automated test suite:
```bash
python -m unittest discover
```

---

## Project Structure

```text
TrackName/
├── app.py                  # Entrypoint for the web application
├── main.py                 # Entrypoint for the CLI application
├── requirements.txt        # Third-party dependencies
├── README.md               # Documentation
├── static/                 # Static assets for the web UI
│   ├── style.css           # Premium dark-theme CSS stylesheet
│   └── main.js             # Client-side interactions
├── templates/              # Jinja2 HTML templates for the web UI
│   ├── base.html           # Main base layout
│   ├── index.html          # Homepage / Search selection
│   ├── results.html        # Track / artist search results page
│   ├── lyrics.html         # Lyrics fragment search results page
│   ├── detail.html         # Detailed song info & lyrics preview page
│   ├── favorites.html      # Saved favorite songs management page
│   └── history.html        # Search history page
├── tests/                  # Unit tests for CLI/API modules
└── trackname/              # Core application package
    ├── __init__.py
    ├── api.py              # Genius API integration & response parser
    ├── cli.py              # CLI interactive flow logic
    ├── details.py          # Web scraping for lyrics previews & details
    ├── display.py          # CLI text formatting & colorization
    ├── lyrics_search.py    # lyrics.ovh API integration for lyrics search
    ├── storage.py          # Local JSON storage for history & favorites
    └── text.py             # Query cleanup helpers
```
