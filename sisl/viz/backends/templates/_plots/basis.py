from .grid import GridBackend

from ....plots import BasisPlot

class BasisBackend(GridBackend):
    
    def draw(self, backend_info):
        for grid_backend_info in backend_info:
            super().draw(grid_backend_info)
    

BasisPlot.backends.register_template(BasisBackend)