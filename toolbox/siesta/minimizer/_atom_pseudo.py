# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import sys
from pathlib import Path
from functools import partial

import numpy as np
import sisl as si

from ..atom import AtomInput
from ._variable import UpdateVariable, read_variable_yaml


__all__ = ["AtomPseudo"]


class AtomPseudo(AtomInput):

    def get_variables(self, dict_or_yaml):
        """ Convert a dictionary or yaml file input to variables usable by the minimizer """
        return self._get_variables_dict(read_variable_yaml(dict_or_yaml, self.atom.tag))

    def _get_variables_dict(self, dic):
        """ Parse a dictionary adding potential variables to the minimize model """
        symbol = self.atom.tag
        V = []
        if len(dic) == 0:
            return V

        # Now loop and find coincidences in the dictionary
        # with respect to the basis
        def update_orb(old, new, orb):
            """ Update an orbital's radii """
            orb._R = new

        # Define other options
        def update(old, new, d, key, idx=None):
            """ An updater for a dictionary with optional keys """
            if idx is None:
                d[key] = new
            else:
                d[key][idx] = new

        # Now parse dictionary for nl
        # Loop keys to figure out what is there
        for key, value in dic.items():
            # we don't need to parse POLARIZATION
            # since that is implicitly handled
            l = 'spdf'.find(key)
            if 0 <= l:
                # Extract values
                v0 = value["initial"]
                bounds = value["bounds"]
                delta = value["delta"]

                found = False
                for orb in self.atom:
                    if orb.l == l:
                        found = True
                        # Ensure it is defined
                        var = UpdateVariable(f"{symbol}.{key}", v0, bounds,
                                             partial(update_orb, orb=orb),
                                             delta=delta)
                        V.append(var)
                if not found:
                    raise ValueError(f"Could not find l={l} shell in the orbitals?")

            elif key in ("core_correction", "core", "rcore"):
                # Extract values
                v0 = value["initial"]
                bounds = value["bounds"]
                delta = value["delta"]
                # Ensure it is enabled
                self.opts.cc = True
                var = UpdateVariable(f"{symbol}.core", v0, bounds,
                                     partial(update, d=self.opts, key="rcore"),
                                     delta=delta)
                V.append(var)

            elif key in ("log_radii", "logr"):
                # Extract values
                v0 = value["initial"]
                bounds = value["bounds"]
                delta = value["delta"]
                var = UpdateVariable(f"{symbol}.logr", v0, bounds,
                                     partial(update, d=self.opts, key="logr"),
                                     delta=delta)
                V.append(var)

            else:
                raise ValueError(f"Could not find something useful to do with: {key} = {value}, a typo perhaps?")

        return V
