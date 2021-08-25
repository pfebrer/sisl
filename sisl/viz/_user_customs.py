# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import sys
import importlib.util

from sisl._environ import get_environ_variable

__all__ = ["import_user_extensions"]

USER_CUSTOM_FOLDER = get_environ_variable("SISL_CONFIGDIR") / "viz"

def import_user_extensions():
    """Imports the custom code of users."""
    # We could just run the __init__.py file, but then relative imports won't work in the
    # user's code.
    try:
        spec = importlib.util.spec_from_file_location("sislviz_customs", USER_CUSTOM_FOLDER / "__init__.py")
        foo = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = foo
        spec.loader.exec_module(foo)
    except FileNotFoundError:
        pass
