# City Navigation Web App

A simple Flask web application implementing a City Navigation System using graph algorithms (Dijkstra and A*).

## How to run (locally)

1. Create a python virtual environment and install requirements:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Run the Flask app:
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
```

3. Open http://localhost:5000 in your browser.

## Features
- Select source and destination cities from dropdown.
- Choose algorithm: Dijkstra or A* (A* uses straight-line Haversine heuristic).
- Interactive map using Leaflet shows city markers and the computed route polyline.

## Files
- `app.py` - Flask application
- `graph.py` - Graph data structure and algorithms
- `templates/` - HTML templates (index.html, result.html)
- `static/css/style.css` - Basic styling
