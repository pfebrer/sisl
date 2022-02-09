from .grid import GridBackend

from ....plots import BasisPlot

class BasisBackend(GridBackend):
    
    def draw(self, backend_info):
        for grid_backend_info in backend_info['grids']:
            super().draw(grid_backend_info)

        if backend_info["geom_plot"] is not None:
            self.draw_other_plot(backend_info["geom_plot"])
    

BasisPlot.backends.register_template(BasisBackend)