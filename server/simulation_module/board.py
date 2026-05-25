from collections import deque

HEX_DIRECTIONS = [
    (1, -1, 0),
    (1, 0, -1),
    (0, 1, -1),
    (-1, 1, 0),
    (-1, 0, 1),
    (0, -1, 1)
]

class Board:
    def __init__(self, tiles=None):
        if tiles is None:
            tiles = {}
        self.tiles = tiles
        self.regions = {}

    def get_tile_by_coord(self, q, r, s):
        if q + r + s != 0:
            return None

        return self.tiles.get((q, r, s))

    def get_tiles_in_range(self, center_tile, radius):
        results = []

        for dq in range(-radius, radius + 1):
            for dr in range(max(-radius, -dq - radius), min(radius, -dq + radius) + 1):
                ds = -dq - dr

                results.append(self.tiles.get((center_tile.q + dq, center_tile.r + dr, center_tile.s + ds)))
        return results

    def get_neighbours(self, tile):
        results = []

        for dq, dr, ds in HEX_DIRECTIONS:
            neighbour = self.tiles.get((
                tile.q + dq,
                tile.r + dr,
                tile.s + ds
            ))

            if neighbour is not None:
                results.append(neighbour)
        return results

    def find_shortest_path(self, start_tile, end_tile, max_distance, occupancy):
        if calc_distance(start_tile.q, start_tile.r, start_tile.s, end_tile.q, end_tile.r, end_tile.s) > max_distance:
            return None

        queue = deque([start_tile])
        visited = {start_tile}
        came_from = {}
        distance = {
            start_tile: 0,
        }

        while queue:
            current = queue.popleft()

            if current == end_tile:
                break

            for neighbour in self.get_neighbours(current):
                if occupancy.get((neighbour.q, neighbour.r, neighbour.s)) is not None:
                    continue

                if neighbour in visited:
                    continue

                new_distance = distance[current] + 1
                if new_distance > max_distance:
                    continue

                visited.add(neighbour)
                distance[neighbour] = new_distance
                came_from[neighbour] = current

                queue.append(neighbour)

        if end_tile not in came_from and end_tile != start_tile:
            return None

        path = [end_tile]
        current = end_tile
        while current != start_tile:
            current = came_from[current]
            path.append(current)

        path.reverse()
        return path