"""
This is the initial setup for the Euclid namespace package
"""
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)  # @ReservedAssignment

__author__  = 'Hubert Degaudenzi'

import sys

# hooks and other customizations are not used ith iPython
_is_ipython = hasattr(__builtins__, '__IPYTHON__') or 'IPython' in sys.modules

# Add some infrastructure if we are being imported via a Jupyter Kernel ------
if _is_ipython:
    from IPython import get_ipython
    ip = get_ipython()
    if hasattr(ip,"kernel"):
        from .Login import LoginScript
        # option_list = ["--debug"]
        option_list = []
        _login_script = LoginScript()
        _login_script.parseOpts(option_list)
        _ev = _login_script.setEnv()
        _al = _login_script.setAliases()
        _ex = _login_script.setExtra()

# cleanup 
import atexit
def cleanup():

    if _is_ipython:
        ip = get_ipython()
        if hasattr(ip,"kernel"):
            del _ex
            del _al
            del _ev
            del _login_script

    # destroy ROOT module
    del sys.modules[ 'Euclid' ]

atexit.register( cleanup )
del cleanup, atexit
