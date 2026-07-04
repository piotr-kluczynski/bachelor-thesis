class Tile:
    def __init__(self, q, r, s, isCommandCentre = False):
        self.q = q
        self.r = r
        self.s = s
        self.isCommandCentre = isCommandCentre
        self.unit = None
        self.region = None