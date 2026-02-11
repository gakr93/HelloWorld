from __future__ import annotations

import json
from datetime import datetime
from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from random import choice
from urllib.error import URLError
from urllib.request import urlopen

HOST = "0.0.0.0"
PORT = 8000
WEATHER_URL = "https://wttr.in/Celina,TX?format=j1"
QUOTES = [
    "Success is the sum of small efforts, repeated day in and day out.",
    "Dream big. Start small. Act now.",
    "Discipline is choosing between what you want now and what you want most.",
    "Your future is created by what you do today, not tomorrow.",
    "Keep going. Everything you need will come to you at the perfect time.",
]


def get_weather() -> dict[str, str]:
    """Fetch current weather in Celina, TX from wttr.in."""
    try:
        with urlopen(WEATHER_URL, timeout=6) as response:
            payload = json.loads(response.read().decode("utf-8"))
        current = payload["current_condition"][0]
        forecast = payload["weather"][0]
        return {
            "temp_c": current.get("temp_C", "N/A"),
            "description": current.get("weatherDesc", [{"value": "N/A"}])[0]["value"],
            "feels_like": current.get("FeelsLikeC", "N/A"),
            "high": forecast.get("maxtempC", "N/A"),
            "low": forecast.get("mintempC", "N/A"),
        }
    except (URLError, KeyError, IndexError, ValueError, TimeoutError):
        return {
            "temp_c": "N/A",
            "description": "Weather data unavailable",
            "feels_like": "N/A",
            "high": "N/A",
            "low": "N/A",
        }


def render_html() -> str:
    date_text = datetime.now().strftime("%A, %B %d, %Y")
    weather = get_weather()
    quote = choice(QUOTES)

    return f"""<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>Akshay's Daily Dashboard</title>
    <style>
      body {{
        margin: 0;
        font-family: Inter, Arial, sans-serif;
        min-height: 100vh;
        display: grid;
        place-items: center;
        background: linear-gradient(140deg, #0f2027, #203a43, #2c5364);
        color: #f8fafc;
      }}
      .card {{
        width: min(720px, 92vw);
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.25);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 16px 40px rgba(2, 6, 23, 0.45);
        position: relative;
        overflow: hidden;
      }}
      .watermark {{
        position: absolute;
        right: 16px;
        bottom: 10px;
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: 0.2rem;
        color: rgba(248, 250, 252, 0.08);
        user-select: none;
      }}
      h1 {{
        margin: 0;
        font-size: clamp(1.6rem, 3vw, 2.2rem);
      }}
      .section {{
        margin-top: 1.3rem;
        padding-top: 1.1rem;
        border-top: 1px solid rgba(148, 163, 184, 0.25);
      }}
      .label {{
        text-transform: uppercase;
        letter-spacing: 0.08rem;
        font-size: 0.78rem;
        color: #93c5fd;
      }}
      .value {{
        margin-top: 0.3rem;
        font-size: 1.2rem;
      }}
      .quote {{
        font-style: italic;
        line-height: 1.55;
      }}
    </style>
  </head>
  <body>
    <main class=\"card\">
      <h1>Hello Akshay 👋</h1>
      <section class=\"section\">
        <div class=\"label\">Today's Date</div>
        <div class=\"value\">{escape(date_text)}</div>
      </section>
      <section class=\"section\">
        <div class=\"label\">Weather in Celina, TX</div>
        <div class=\"value\">{escape(weather['temp_c'])}°C · {escape(weather['description'])}</div>
        <div>Feels like {escape(weather['feels_like'])}°C · H: {escape(weather['high'])}°C / L: {escape(weather['low'])}°C</div>
      </section>
      <section class=\"section\">
        <div class=\"label\">Motivation</div>
        <p class=\"quote\">“{escape(quote)}”</p>
      </section>
      <div class=\"watermark\">AKSHAY</div>
    </main>
  </body>
</html>"""


class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        if self.path not in ("/", ""):
            self.send_error(404)
            return

        body = render_html().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), DashboardHandler)
    print(f"Serving on http://{HOST}:{PORT}")
    server.serve_forever()
