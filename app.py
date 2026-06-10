import os
import sys
from datetime import datetime
from flask import Flask

def datetimeformat(value):
    try:
        dt = datetime.fromisoformat(value)
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        return f"{dt.day} {months[dt.month - 1]} {dt.year} · {dt.strftime('%H:%M')}"
    except (ValueError, TypeError):
        return value

def create_app():
    token = os.environ.get("GENIUS_ACCESS_TOKEN")
    if not token:
        print("ERROR: The GENIUS_ACCESS_TOKEN environment variable is not set.")
        sys.exit(1)

    app = Flask(__name__)
    app.config["GENIUS_TOKEN"] = token
    app.template_filter('datetimeformat')(datetimeformat)

    from trackname.web.routes import web_bp
    app.register_blueprint(web_bp)

    return app

app = create_app()

if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG") == "1"
    app.run(debug=debug_mode)
