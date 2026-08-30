import logging

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, current_app
from trackname.text import clean_query
from trackname.api import search_genius
from trackname import storage, details, lyrics_search
from trackname.lyrics_search import LyricsSearchError
import requests

from trackname.web.limiter import limiter

web_bp = Blueprint('web', __name__)
logger = logging.getLogger(__name__)

@web_bp.route('/')
def index():
    return render_template('index.html')

@web_bp.route('/search')
@limiter.limit("20 per minute")
def search():
    query = request.args.get('q', '').strip()
    if not query:
        return render_template('results.html', error="Query cannot be empty", query=query, hits=[])
    
    clean_q = clean_query(query)
    token = current_app.config.get("GENIUS_TOKEN")
    
    try:
        hits = search_genius(clean_q, token)
        if hits:
            storage.add_history_entry(query, hits)
        return render_template('results.html', hits=hits, query=query)
    except Exception:
        logger.exception("Search failed for query=%r", query)
        return render_template(
            'results.html',
            error="Something went wrong while searching. Please try again.",
            query=query,
            hits=[],
        )

@web_bp.route('/song/<song_id>')
def song_detail(song_id):
    token = current_app.config.get("GENIUS_TOKEN")
    artist = request.args.get('artist', '')
    title = request.args.get('title', '')
    try:
        song_details = details.fetch_song_details(song_id, token)
        lyrics = details.fetch_lyrics(artist, title) if artist and title else ""
        return render_template('detail.html', details=song_details, lyrics=lyrics, song_id=song_id)
    except Exception:
        logger.exception("Failed to fetch song details for song_id=%r", song_id)
        return render_template(
            'detail.html',
            error="Couldn't load this song's details right now. Please try again.",
            song_id=song_id,
        )

@web_bp.route('/favorites/add', methods=['POST'])
def add_favorite():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid data"})
    
    added = storage.add_favorite_entry(data)
    if added:
        return jsonify({"success": True, "message": "Added to favorites"})
    else:
        return jsonify({"success": False, "message": "Already in favorites"})

@web_bp.route('/favorites/remove', methods=['POST'])
def remove_favorite():
    data = request.get_json()
    url = data.get('url') if data else None
    if not url:
        return jsonify({"success": False})
    
    favorites = storage.load_favorites()
    new_favorites = [f for f in favorites if isinstance(f, dict) and f.get('url') != url]
    storage.save_favorites(new_favorites)
    return jsonify({"success": True})

@web_bp.route('/favorites')
def favorites():
    favs = storage.load_favorites()
    return render_template('favorites.html', favorites=favs)

@web_bp.route('/history')
def history():
    entries = storage.load_history()
    entries = entries[-50:]
    return render_template('history.html', entries=entries)

@web_bp.route('/history/clear', methods=['POST'])
def clear_history():
    storage.clear_history()
    return redirect(url_for('web.history'))

@web_bp.route('/lyrics')
def lyrics():
    return render_template('lyrics.html')

@web_bp.route('/lyrics/search')
@limiter.limit("20 per minute")
def search_lyrics():
    fragment = request.args.get('q', '').strip()
    if not fragment:
        return render_template('lyrics.html', error="No songs found")
        
    try:
        candidates = lyrics_search.search_by_lyrics(fragment)
        if not candidates:
            return render_template('lyrics.html', error="No songs found")
        if len(candidates) == 1:
            chosen = candidates[0]
            q = f"{chosen['artist']} {chosen['title']}"
            return redirect(url_for('web.search', q=q))
        return render_template('lyrics.html', candidates=candidates)
    except Exception:
        logger.exception("Lyrics search failed for fragment=%r", fragment)
        return render_template(
            'lyrics.html',
            error="Something went wrong while searching lyrics. Please try again.",
        )
