"""
This is the initial setup for the Euclid namespace package
"""
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)  # @ReservedAssignment

__author__  = 'Hubert Degaudenzi'

import sys

# hooks and other customizations are not used ith iPython
_is_ipython = hasattr(__builtins__, '__IPYTHON__') or 'IPython' in sys.modules

### Add some infrastructure if we are being imported via a Jupyter Kernel ------
if _is_ipython:
    from IPython import get_ipython
    ip = get_ipython()
    if hasattr(ip,"kernel"):
        from .Login import LoginScript
        _ls = LoginScript()
        _env = _ls.setEnv()
        _al  = _ls.setAliases()
        _ex  = _ls.setExtra()

### b/c of circular references, the facade needs explicit cleanup ---------------
import atexit
def cleanup():

    if _is_ipython:
        ip = get_ipython()
        if hasattr(ip,"kernel"):
            del _ex
            del _al
            del _env
            del _ls

    # destroy ROOT module
    del sys.modules[ 'Euclid' ]

atexit.register( cleanup )
del cleanup, atexit
