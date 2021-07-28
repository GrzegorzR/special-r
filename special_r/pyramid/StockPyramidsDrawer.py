

class StockPyramidsDrawer:
    def __init__(self, pyramids):
        self.pyramids = pyramids
        self.max_l = max([len(p.rects) for p in self.pyramids])

    def update(self, ts):
        for p in self.pyramids:
            p.update(ts)

    def draw(self, surface):
        for i in range(self.max_l):
            for p in self.pyramids:
                if i < len(p.rects):
                    p.rects[i].draw(surface)


