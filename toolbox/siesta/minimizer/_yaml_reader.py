# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import yaml
from sisl.unit.siesta import units


def read_yaml(file, nodes=()):
    """ Reads a yaml-file and returns the dictionary for the yaml-file

    Parameters
    ----------
    file : Path
       the yaml-file to parse
    nodes : iterable, optional
       extract the node in a consecutive manner
    """
    dic = yaml.load(open(file, 'r'), Loader=yaml.CLoader)
    if isinstance(nodes, str):
        nodes = [nodes]
    for node in nodes:
        dic = dic[node]
    return dic


def parse_value(value, unit=None, value_unit=None):
    """ Converts a float/str to proper value """
    value_unit = unit
    if isinstance(value, str):
        value, value_unit = value.split()
        if len(value_unit) == 0:
            value_unit = None
    value = float(value)
    # Now parse unit
    if unit == value_unit:
        return value
    return value * units(value_unit, unit)


def parse_variable(value, default=None, unit=None, name='', update_func=None):
    """ Parse a value to either a `Parameter` or `Variable` with defaults and units

    Parameters
    ----------
    value : str, float or dict
       parseable value, if a dictionary it must contain the entries:
       initial, bounds, delta
    default : float, optional
       default value
    unit : str, optional
       the default unit of the variable
    name : str, optional
       name of the parameter/variable
    update_func : callable, optional
       the update function to be called if required
    """
    from ._variable import Parameter, Variable, UpdateVariable
    attrs = {}
    if unit is not None:
        attrs = {'unit': unit}

    if isinstance(value, dict):
        value_unit = value.get("unit")
        val = parse_value(value["initial"], unit, value_unit)
        bounds = value["bounds"]
        bounds = [parse_value(bound, unit, value_unit) for bound in bounds]
        delta = parse_value(value["delta"], unit, value_unit)
        if update_func is None:
            return Variable(name, val, bounds, delta=delta, **attrs)
        return UpdateVariable(name, val, bounds, func=update_func, delta=delta, **attrs)

    if value is None:
        return Parameter(name, default, **attrs)
    return Parameter(name, parse_value(value, unit), **attrs)
