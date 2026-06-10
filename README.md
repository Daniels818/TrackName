# TrackName

![Python](https://img.shields.io/badge/python-3.8%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/flask-3.0%2B-lightgrey?logo=flask&logoColor=white)
![API](https://img.shields.io/badge/API-Genius%20%7C%20lyrics.ovh-yellow)
![Deployment](https://img.shields.io/badge/Deployed-Render-green?logo=render)

TrackName is a powerful, dual-interface music discovery and management tool. Search for songs by **title**, **artist name**, or even **a fragment of the lyrics**. View rich song details, read lyrics previews, and manage your search history and favorite tracks.

## 🚀 Live Demo
You can try the web version of TrackName immediately:
👉 **[View Live Demo on Render](https://trackname.onrender.com)** *(Replace with your actual Render URL)*

---

## ✨ Features

### 🔍 Search & Discovery
- **Search by Title & Artist:** Fast search powered by the Genius API.
- **Search by Lyrics:** Can't remember the name of a song? Type a snippet of the lyrics to find it, powered by the lyrics.ovh API.
- **Rich Song Details:** Fetch release year, view count, annotations, featured artists, song description, and a preview of the lyrics.

### 💾 Management & Personalization
- **Favorites:** Save your favorite songs to keep track of your top discoveries.
- **Search History:** Automatically track your search history so you can review recent queries or clear them at any time.

### 🌐 Dual Interface Support
- **Modern Web GUI:** A beautiful, responsive dark-mode web dashboard built with vanilla CSS glassmorphism and smooth animations.
- **Interactive CLI:** A terminal interface featuring clean console layouts, quick shortcuts, and robust text-based menus.

---

## 🛠 How to Use

### 🌐 Via the Web (Online)
Simply visit the **Live Demo** link above. No installation required! 
*Note: For the hosted version, history and favorites are stored temporarily and will reset upon server restarts.*

### 🖥️ Via the Web (Local)
If you want to run the web app on your own machine:
1. Follow the **Installation** steps below.
2. Run: `python app.py`
3. Open your browser at: `http://127.0.0.1:5000`

### 📟 Via the CLI (Local)
For the terminal-based experience:
1. Follow the **Installation** steps below.
2. Run: `python main.py`
3. Use special commands like `:lyrics`, `:history`, `:favorites`, and `:clear`.

---

## 📦 Installation (Local)

### Requirements
- Python 3.8 or higher
- Flask 3.0+
- Beautiful Soup 4
- Requests

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Daniels818/TrackName.git
   cd TrackName
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration
You need a free Genius API token:
1. Sign up at [genius.com/api-clients](https://genius.com/api-clients)
2. Create an app and copy the **Client Access Token**.
3. Set the environment variable:
   - **Windows (PowerShell):** `$env:GENIUS_ACCESS_TOKEN = "your_token_here"`
   - **Windows (CMD):** `setx GENIUS_ACCESS_TOKEN "your_token_here"`
   - **Linux / macOS:** `export GENIUS_ACCESS_TOKEN='your_token_here'`

---

## 🚢 Deployment
This project is configured for easy deployment on platforms like Render or Railway. Detailed instructions on how to host your own instance can be found in the [DEPLOYMENT.md](./DEPLOYMENT.md) file.

---

## 🧪 Testing
To run the automated test suite locally:
```bash
python -m unittest discover
```

---

## 📂 Project Structure
```text
TrackName/
├── app.py                  # Entrypoint for the web application
├── main.py                 # Entrypoint for the CLI application
├── requirements.txt        # Third-party dependencies
├── README.md               # Documentation
├── DEPLOYMENT.md           # Deployment guide
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
