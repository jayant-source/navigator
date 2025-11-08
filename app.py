from flask import Flask, render_template, request, redirect, url_for, jsonify
from graph import build_sample_graph, CityGraph, dijkstra, a_star, reconstruct_path
import json

app = Flask(__name__)

# Load or build graph at startup
CG = build_sample_graph()

@app.route('/')
def index():
    # provide list of cities for the form and markers for map
    cities = [{ 'id': cid, 'name': c.name, 'lat': c.lat, 'lon': c.lon } for cid,c in CG.cities.items()]
    return render_template('index.html', cities=cities)

@app.route('/route', methods=['POST'])
def route():
    src = request.form.get('source')
    dst = request.form.get('destination')
    algo = request.form.get('algorithm', 'dijkstra')
    if not src or not dst:
        return redirect(url_for('index'))
    if src not in CG.cities or dst not in CG.cities:
        return redirect(url_for('index'))
    if algo == 'astar':
        g, came = a_star(CG, src, dst)
        path = reconstruct_path(came, src, dst)
        total = g.get(path[-1]) if path else None
    else:
        dist, prev = dijkstra(CG, src, target=dst)
        path = reconstruct_path(prev, src, dst)
        total = dist.get(path[-1]) if path else None

    # build coordinates for path to show on map
    coords = []
    if path:
        for pid in path:
            c = CG.cities[pid]
            coords.append([c.lat, c.lon])
    cities = [{ 'id': cid, 'name': c.name, 'lat': c.lat, 'lon': c.lon } for cid,c in CG.cities.items()]
    return render_template('result.html', path=path, total=total, cities=cities, coords=json.dumps(coords), source=src, destination=dst, algorithm=algo)

@app.route('/api/shortest', methods=['GET'])
def api_shortest():
    src = request.args.get('src')
    dst = request.args.get('dst')
    algo = request.args.get('algo', 'dijkstra')
    if not src or not dst:
        return jsonify({'error':'src and dst required'}), 400
    if algo == 'astar':
        g, came = a_star(CG, src, dst)
        path = reconstruct_path(came, src, dst)
        total = g.get(path[-1]) if path else None
    else:
        dist, prev = dijkstra(CG, src, target=dst)
        path = reconstruct_path(prev, src, dst)
        total = dist.get(path[-1]) if path else None
    return jsonify({'path': path or [], 'distance': total})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')