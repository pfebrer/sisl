from ....plots import BondLengthMap
from .geometry import MatplotlibGeometryBackend
from ...templates import BondLengthMapBackend

class MatplotlibBondLengthMapBackend(MatplotlibGeometryBackend, BondLengthMapBackend):

    def draw_2D(self, backend_info, **kwargs):
        self._colorscale = None
        if "bonds_coloraxis" in backend_info:
            self._colorscale = backend_info["bonds_coloraxis"]["colorscale"]

        super().draw_2D(backend_info, **kwargs)

    def _draw_bonds_2D_multi_color_size(self, *args, **kwargs):
        kwargs["colorscale"] = self._colorscale
        super()._draw_bonds_2D_multi_color_size(*args, **kwargs)

BondLengthMap._backends.register("matplotlib", MatplotlibBondLengthMapBackend)