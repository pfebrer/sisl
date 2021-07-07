# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import importlib
import pytest

import os.path as osp

@pytest.fixture(scope="session")
def importables():
    # Find out which packages are impo
    importables_info = {True: [], False: []}
    for modname in ("plotly", "skimage", "pandas", "xarray"):
        try:
            importlib.import_module(modname)
            importables_info[True].append(modname)
        except ImportError:
            importables_info[False].append(modname)

    return importables_info

@pytest.fixture(scope="session")
def siesta_test_files(sisl_files):

    def _siesta_test_files(path):
        return sisl_files(osp.join('sisl', 'io', 'siesta', path))
    
    return _siesta_test_files

class _TestPlot:

    @pytest.fixture(scope="class")
    def plot(self, init_func_and_attrs, importables):
        """Initializes the plot using the initializin function.

        If the plot can't be initialized it skips all tests for that plot.
        """

        init_func = init_func_and_attrs[0]

        msg = ""
        if importables[False]:
            msg = ", ".join(importables[False]) + " is/are not importable"
        if importables[True]:
            msg = f'{", ".join(importables[True]) + " is/are importable"}; {msg}'

        try:
            return init_func(_debug=True)
        except Exception as e:
            pytest.skip(f"Plot was not initialized. Error: {e}. \n\n{msg}")

    @pytest.fixture(scope="class")
    def test_attrs(self, init_func_and_attrs):
        """Checks that all the attributes required for testing have been passed.

        Otherwise, tests are skipped.
        """
        attrs = init_func_and_attrs[1]

        missing_attrs = set(getattr(self, "_required_attrs", [])) - set(attrs)
        if len(missing_attrs) > 0:
            pytest.skip(f"Tests could not be ran because some testing attributes are missing: {missing_attrs}")
        
        return attrs
