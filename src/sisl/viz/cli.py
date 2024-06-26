# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import functools
import inspect
from pathlib import Path

import rich_click as click
import yaml
from nodify.cli._click import decorate_click

import sisl
import sisl.typing
from sisl.viz import BandsPlot, GeometryPlot, GridPlot, PdosPlot, WavefunctionPlot
from sisl.viz.data import Data
from sisl.viz.types import Axes


def get_cls_type_kwargs(cls):

    argument_kwargs = {"parser": cls.new}

    argument_kwargs["metavar"] = f"{cls.__name__}"

    return argument_kwargs


def _get_subclasses(cls):
    return cls.__subclasses__() + [
        g for s in cls.__subclasses__() for g in _get_subclasses(s)
    ]


all_data_subclasses = _get_subclasses(Data)

custom_type_kwargs = {
    **{
        data_cls: get_cls_type_kwargs(data_cls)
        for data_cls in all_data_subclasses
        if hasattr(data_cls, "new")
    },
    sisl.Geometry: get_cls_type_kwargs(sisl.Geometry),
    sisl.Grid: get_cls_type_kwargs(sisl.Grid),
    Axes: {"parser": lambda x: x},
    sisl.typing.AtomsLike: {"parser": lambda x: x},
}

GENERATED = []


def show(result):
    plot = GENERATED[-1]

    if plot.inputs.get("backend") == "matplotlib":
        import matplotlib.pyplot as plt

        plot.get()
        plt.show(block=True)
    elif plot.inputs.get("backend") == "ascii":
        import matplotlib as mpl

        mpl.use("module://mpl_ascii")
        return plot.show()
    else:
        return plot.show()


def wrap_plot(plot_cls):

    @functools.wraps(plot_cls)
    def plot(*args, **kwargs):
        if Path("config.yaml").exists():
            with open("config.yaml") as f:
                config = yaml.safe_load(f)

            if config.get("config_type") == "multi":
                kwargs.update(config.get("plot", {}))
                import sys

                kwargs.update(config.get(sys.argv[1], {}))
            else:
                kwargs.update(config)

        p = plot_cls(*args, **kwargs)

        GENERATED.append(p)

        return p

    return plot


def add_plot_group(plot_cls, parent, *group_args, **group_kwargs):

    plot_func = decorate_click(
        wrap_plot(plot_cls), custom_type_kwargs=custom_type_kwargs
    )

    plot_group = parent.group(
        *group_args, invoke_without_command=True, chain=True, **group_kwargs
    )(plot_func)

    if plot_cls is PdosPlot:

        split_DOS = PdosPlot.split_DOS

        @functools.wraps(split_DOS)
        def f(*args, **kwargs):
            plot = GENERATED[-1]
            return plot.split_DOS(*args, **kwargs)

        # Remove the first argument, which is the plot instance
        sig = inspect.signature(split_DOS)
        f.__signature__ = sig.replace(parameters=list(sig.parameters.values())[1:-1])

        plot_group.command(name=f.__name__)(
            decorate_click(f, custom_type_kwargs=custom_type_kwargs)
        )

    return plot_group


# subapp.command("bands")(decorate_click(wrap_plot(BandsPlot), custom_type_kwargs=custom_type_kwargs))


@click.group(result_callback=show)
def _app():
    """Plotting CLI"""


add_plot_group(BandsPlot, _app, "bands")
add_plot_group(GeometryPlot, _app, "geometry")
add_plot_group(GridPlot, _app, "grid")
add_plot_group(WavefunctionPlot, _app, "wavefunction")
add_plot_group(PdosPlot, _app, "pdos")

# merged = typer.Typer(help="Merge multiple plots in the same axes")
# app.add_typer(merged, name="merged", rich_help_panel="Combined plots")
# subplots = typer.Typer(help="Create subplots from multiple plots.")
# app.add_typer(subplots, name="subplots", rich_help_panel="Combined plots")
# animation = typer.Typer(help="Create animations from multiple plots.")
# app.add_typer(animation, name="animation", rich_help_panel="Combined plots")

_app = _app


def app():
    import sys

    if "." in sys.argv[1]:
        import sisl

        sile = sisl.get_sile(sys.argv[1])
        default = sile.plot._default or list(sile.plot._dispatchs)[0]
        sys.argv.insert(1, default)

    _app()


if __name__ == "__main__":
    app()
