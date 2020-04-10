"""
This is the initial setup for the Euclid namespace package
"""
from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)  # @ReservedAssignment

__author__  = 'Hubert Degaudenzi'

import sys

# hooks and other customizations are not used ith iPython
_is_ipython = hasattr(__builtins__, '__IPYTHON__') or 'IPython' in sys.modules
_cleanup_list = []

# Add some infrastructure if we are being imported via a Jupyter Kernel ------
if _is_ipython:
    from IPython import get_ipython
    _ip = get_ipython()
    _cleanup_list.append(_ip)
    if hasattr(_ip,"kernel"):
        from .Login import LoginScript
        # _option_list = ["--debug"]
        _option_list = []
        _cleanup_list.append(_option_list)
        _login_script = LoginScript()
        _cleanup_list.append(_login_script)
        _login_script.parseOpts(_option_list)
        _ev = _login_script.setEnv()
        _cleanup_list.append(_ev)
        _al = _login_script.setAliases()
        _cleanup_list.append(_al)
        _ex = _login_script.setExtra()
        _cleanup_list.append(_ex)

# _cleanup 
import atexit
def _cleanup():

    for s in _cleanup_list:
        del s

    del _cleanup_list, _is_ipython
    # destroy Euclid module
    del sys.modules[ 'Euclid' ]

atexit.register( _cleanup )
del _cleanup, atexit, sys
