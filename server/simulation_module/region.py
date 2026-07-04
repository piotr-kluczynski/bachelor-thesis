class Region:
    def __init__(self, tiles, commandCentre, owner=None, regionUpkeep=2):
        self.tiles = tiles
        self.commandCentre = commandCentre
        self.owner = owner
        self.regionUpkeep = regionUpkeep