import math, heapq, random
from dataclasses import dataclass

@dataclass
class City:
    id: str
    name: str
    lat: float = None
    lon: float = None

@dataclass
class Road:
    u: str
    v: str
    distance: float
    time: float = None
    cost: float = 0.0
    one_way: bool = False

class CityGraph:
    def __init__(self, directed=False):
        self.graph = {}
        self.cities = {}
        self.directed = directed

    def add_city(self, city: City):
        if city.id in self.cities:
            raise ValueError('city exists')
        self.cities[city.id] = city
        self.graph[city.id] = []

    def add_road(self, road: Road):
        if road.u not in self.cities or road.v not in self.cities:
            raise ValueError('both cities must exist')
        attrs = {'distance': float(road.distance), 'time': float(road.time) if road.time is not None else float(road.distance)/50.0, 'cost': float(road.cost), 'one_way': bool(road.one_way)}
        self.graph[road.u].append((road.v, attrs))
        if not road.one_way and not self.directed:
            self.graph[road.v].append((road.u, attrs))

    def neighbors(self, u):
        return self.graph.get(u, [])

    def nodes(self):
        return list(self.graph.keys())

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2*R*math.asin(math.sqrt(a))

def dijkstra(city_graph: CityGraph, source, target=None, weight_attr='distance'):
    graph = city_graph.graph
    dist = {u: float('inf') for u in graph}
    prev = {}
    if source not in graph:
        raise ValueError('Source not in graph')
    dist[source] = 0.0
    pq = [(0.0, source)]
    while pq:
        d,u = heapq.heappop(pq)
        if d>dist[u]:
            continue
        if u == target:
            break
        for v, attrs in graph[u]:
            w = float(attrs.get(weight_attr, 1.0))
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, prev

def reconstruct_path(prev, source, target):
    if source == target:
        return [source]
    if target not in prev:
        cur = target
        path = []
        while cur in prev:
            path.append(cur)
            cur = prev[cur]
            if cur == source:
                path.append(source)
                return path[::-1]
        return None
    path = []
    cur = target
    while cur != source:
        path.append(cur)
        cur = prev[cur]
    path.append(source)
    return path[::-1]

def a_star(city_graph: CityGraph, source, target, weight_attr='distance'):
    if source not in city_graph.graph or target not in city_graph.graph:
        raise ValueError('source/target not in graph')
    cities = city_graph.cities
    open_set = []
    g = {u: float('inf') for u in city_graph.graph}
    f = {u: float('inf') for u in city_graph.graph}
    g[source] = 0.0
    def heuristic(u, v):
        cu, cv = cities[u], cities[v]
        if cu.lat is None or cv.lat is None:
            return 0.0
        return haversine(cu.lat, cu.lon, cv.lat, cv.lon)
    f[source] = heuristic(source, target)
    heapq.heappush(open_set, (f[source], source))
    came_from = {}
    closed = set()
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == target:
            break
        if current in closed:
            continue
        closed.add(current)
        for neighbor, attrs in city_graph.graph[current]:
            tentative_g = g[current] + float(attrs.get(weight_attr, 1.0))
            if tentative_g < g[neighbor]:
                came_from[neighbor] = current
                g[neighbor] = tentative_g
                f[neighbor] = tentative_g + heuristic(neighbor, target)
                heapq.heappush(open_set, (f[neighbor], neighbor))
    return g, came_from

def build_sample_graph():
    cg = CityGraph(directed=False)
    base_coords = [
        (\"A\",\"Alpha\",28.61,77.20),
        (\"B\",\"Beta\",28.70,77.10),
        (\"C\",\"Gamma\",28.50,77.18),
        (\"D\",\"Delta\",28.60,77.35),
        (\"E\",\"Epsilon\",28.55,77.03),
        (\"F\",\"Phi\",28.65,77.28),
        (\"G\",\"Gamma2\",28.68,77.05),
        (\"H\",\"Theta\",28.52,77.30),
        (\"I\",\"Iota\",28.58,77.08),
        (\"J\",\"Kappa\",28.72,77.25)
    ]
    for cid, name, lat, lon in base_coords:
        cg.add_city(City(id=cid, name=name, lat=lat, lon=lon))
    def add_road(u,v):
        cu = cg.cities[u]
        cv = cg.cities[v]
        dist = haversine(cu.lat, cu.lon, cv.lat, cv.lon)
        road = Road(u=u, v=v, distance=dist * (1.2 + 0.1*random.random()))
        cg.add_road(road)
    edges = [
        (\"A\",\"B\"), (\"A\",\"C\"), (\"A\",\"D\"), (\"B\",\"F\"), (\"C\",\"E\"),
        (\"D\",\"F\"), (\"E\",\"I\"), (\"F\",\"J\"), (\"G\",\"B\"), (\"G\",\"E\"),
        (\"H\",\"C\"), (\"H\",\"D\"), (\"I\",\"E\"), (\"J\",\"A\")
    ]
    for u,v in edges:
        add_road(u,v)
    return cg
