#!/usr/bin/python
""" Main script to setup the basic Euclid environment """

import sys
import os

#============================================================================
# setting up the core environment for Python only. This has to be done before
# the import of the local modules.
# In principle, only the PYTHONPATH (internal) setup is needed. The PATH and
# other are delayed to the created setup script

# first try to use the installed prefix path
my_own_prefix = "%(this_install_prefix)s"
has_prefix = False

if os.path.exists(my_own_prefix):
    has_prefix = True

my_own_version = "%(this_install_version)s"
has_version = False

if not my_own_version.startswith("%"):
    has_version = True


if has_prefix:
    from distutils.sysconfig import get_python_lib
    if my_own_prefix != "/usr":
        # funky location yeah
        python_loc = get_python_lib(prefix=my_own_prefix)
    else:
        # if the location is standard, don't try to be funny
        python_loc = None
else:
    # use the local properties if the intall_path is no available
    try:
        _this_file = __file__
    except NameError:
        # special procedure to handle the situation when __file__ is not defined.
        # It happens typically when trying to use pdb.
        from imp import find_module, load_module
        _ff, _filename, _desc = find_module("Euclid")
        try:
            lbconf_package = load_module('Euclid', _ff, _filename, _desc)
            _ff, _filename, _desc = find_module(
                'Login', lbconf_package.__path__)
            _this_file = _filename
        finally:
            _ff.close()
    # Bootstrapping the python location
    _pyeuc_dir = os.path.dirname(_this_file)
    _py_dir = os.path.dirname(_pyeuc_dir)
    if os.path.basename(_pyeuc_dir) == "Euclid":
        _base_dir = os.path.dirname(_py_dir)
        python_loc = _py_dir

if python_loc:
    sys.path.insert(0, python_loc)
#============================================================================

from Euclid.Platform import getBinaryOfType, build_types, default_build_type
from Euclid.Platform import getBinaryTypeName
from Euclid.Platform import getCompiler, getPlatformType, getArchitecture
from Euclid.Platform import isBinaryType, NativeMachine
from Euclid.Script import SourceScript
from Euclid.Path import pathPrepend, getClosestPath
import logging
import shutil

__version__ = ""

if has_version:
    __version__ = my_own_version

#-------------------------------------------------------------------------
# Helper functions


def getLoginEnv(optionlist=None):
    if not optionlist:
        optionlist = []
    s = LoginScript()
    s.parseOpts(optionlist)
    return s.setEnv()


def getLoginAliases(optionlist=None):
    if not optionlist:
        optionlist = []
    s = LoginScript()
    s.parseOpts(optionlist)
    return s.setAliases()


def getLoginExtra(optionlist=None):
    if not optionlist:
        optionlist = []
    s = LoginScript()
    s.parseOpts(optionlist)
    return s.setExtra()

#-------------------------------------------------------------------------


class LoginScript(SourceScript):
    _version = __version__
    _description = __doc__
    _description += """

The type is to be chosen among the following list:
%s and the default is %s.
""" % (", ".join(build_types.keys()), default_build_type)

    def __init__(self, usage=None, version=None):
        self._nativemachine = NativeMachine()
        SourceScript.__init__(self, usage, version)
        self.platform = ""
        self.binary = ""
        self.compdef = ""
        self._target_binary_type = None
        self._triedlocalsetup = False
        self._triedAFSsetup = False

#-------------------------------------------------------------------------
# Option definition

    def defineOpts(self):
        """ define commandline options """
        parser = self.parser
        parser.set_defaults(binary_tag=None)
        parser.add_option("-b", "--binary-tag",
                          dest="binary_tag",
                          help="set BINARY_TAG.",
                          fallback_env="BINARY_TAG")
        parser.set_defaults(userarea=None)
        parser.add_option("-u", "--userarea",
                          dest="userarea",
                          help="set User_area.",
                          fallback_env="User_area")
        parser.set_defaults(remove_userarea=False)
        parser.add_option("--no-userarea",
                          dest="remove_userarea",
                          action="store_true",
                          help="prevent the addition of a user area [default: %default]")
        parser.set_defaults(sharedarea=None)
        parser.add_option("-s", "--shared",
                          dest="sharedarea",
                          help="set the shared area",
                          fallback_env="EUCLID_BASE")
        parser.set_defaults(strip_path=True)
        parser.add_option("--no-strip-path",
                          dest="strip_path",
                          action="store_false",
                          help="prevent the cleanup of invalid entries in pathes")
        parser.add_option("--strip-path",
                          dest="strip_path",
                          action="store_true",
                          help="activate the cleanup of invalid entries in pathes [default: %default]")
# specific native platform options
        if self._nativemachine.OSType() == "Darwin":
            parser.add_option("--macport-location",
                              dest="macport_location",
                              help="Set the MacOSX port install base",
                              fallback_env="MACPORT_LOCATION")
            parser.set_defaults(use_macport=True)
            parser.add_option("--no-macport",
                              dest="use_macport",
                              action="store_false",
                              help="prevent the setup of the Mac Port location")

#-------------------------------------------------------------------------

    def _check_env_var(self, envvar):

        ev = self.Environment()
        log = logging.getLogger()

        if envvar in ev:
            log.debug("%s is set to %s" % (envvar, ev[envvar]))
            if not ev[envvar].endswith(os.pathsep):
                log.warn(
                    "The %s variable doesn't end with a \"%s\"" % (envvar, os.pathsep))

#-------------------------------------------------------------------------
    def setOwnPath(self):
        ev = self.Environment()
        opts = self.options
        log = logging.getLogger()

        if python_loc:
            if "PYTHONPATH" in ev:
                ev["PYTHONPATH"] = pathPrepend(ev["PYTHONPATH"],
                                               python_loc,
                                               exist_check=opts.strip_path,
                                               unique=opts.strip_path)
            else:
                if opts.strip_path:
                    if os.path.exists(python_loc):
                        ev["PYTHONPATH"] = python_loc
                else:
                    ev["PYTHONPATH"] = python_loc

        if "PYTHONPATH" in ev:
            log.debug("%s is set to %s" % ("PYTHONPATH", ev["PYTHONPATH"]))

        bin_loc = None

        if python_loc:
            bin_loc = getClosestPath(
                python_loc, os.sep.join(["bin", "ELogin.sh"]), alloccurences=False)
            if not bin_loc:
                bin_loc = getClosestPath(
                    python_loc, os.sep.join(["scripts", "ELogin.sh"]), alloccurences=False)

        if bin_loc:
            the_loc = os.path.dirname(bin_loc[0])
            ev["PATH"] = pathPrepend(ev["PATH"],
                                     the_loc,
                                     exist_check=opts.strip_path,
                                     unique=opts.strip_path)

        log.debug("%s is set to %s" % ("PATH", ev["PATH"]))

        # try the installed directory in $prefix/share/EuclidEnv/cmake/...

        if python_loc:
            python_prefix = python_loc
        else:
            python_prefix = "/usr"

        cmake_loc = getClosestPath(python_prefix,
                                   os.sep.join(
                                       ["share", "EuclidEnv", "cmake", "ElementsProjectConfig.cmake"]),
                                   alloccurences=False)
        if not cmake_loc:
            # use the local source directory
            cmake_loc = getClosestPath(python_prefix,
                                       os.sep.join(
                                           ["data", "cmake", "ElementsProjectConfig.cmake"]),
                                       alloccurences=False)

        if cmake_loc:
            the_loc = os.path.dirname(cmake_loc[0])
            if "CMAKE_PREFIX_PATH" in ev:
                ev["CMAKE_PREFIX_PATH"] = pathPrepend(ev["CMAKE_PREFIX_PATH"],
                                                      the_loc,
                                                      exist_check=opts.strip_path,
                                                      unique=opts.strip_path)
            elif os.path.exists(the_loc):
                ev["CMAKE_PREFIX_PATH"] = the_loc

        if "CMAKE_PREFIX_PATH" in ev:
            log.debug("%s is set to %s" %
                      ("CMAKE_PREFIX_PATH", ev["CMAKE_PREFIX_PATH"]))

        texmf_loc = getClosestPath(python_prefix,
                                   os.sep.join(
                                       ["share", "EuclidEnv", "texmf", "esgsdoc.cls"]),
                                   alloccurences=False)
        if not texmf_loc:
            # use the local source directory
            texmf_loc = getClosestPath(python_prefix,
                                       os.sep.join(
                                           ["data", "texmf", "esgsdoc.cls"]),
                                       alloccurences=False)

        if texmf_loc:
            the_loc = os.path.dirname(texmf_loc[0])
            if "TEXINPUTS" in ev:
                ev["TEXINPUTS"] = pathPrepend(ev["TEXINPUTS"],
                                              the_loc,
                                              exist_check=opts.strip_path,
                                              unique=opts.strip_path)
            elif os.path.exists(the_loc):
                ev["TEXINPUTS"] = the_loc

#-------------------------------------------------------------------------

    def fixPath(self):

        ev = self.Environment()
        log = logging.getLogger()

        var_list = ["MANPATH", "TEXINPUTS"]

        for v in var_list:
            if v in ev:
                if not ev[v].endswith(os.pathsep):
                    log.debug("Adding \"%s\" to the %s variable" %
                              (os.pathsep, v))
                    ev[v] += os.pathsep

        for v in var_list:
            self._check_env_var(v)

#-------------------------------------------------------------------------

    def setPath(self):
        ev = self.Environment()
        opts = self.options
        log = logging.getLogger()
        if not opts.strip_path:
            log.debug("Disabling the path stripping")
            ev["E_NO_STRIP_PATH"] = "1"
        else:
            if ev.has_key("E_NO_STRIP_PATH"):
                log.debug("Reenabling the path stripping")
                del ev["E_NO_STRIP_PATH"]

        self.setOwnPath()

        if (self._nativemachine.OSType() == "Darwin"):
            if ("MACPORT_LOCATION" not in ev) and os.path.exists("/opt/local"):
                ev["MACPORT_LOCATION"] = "/opt/local"

            if "MACPORT_LOCATION" in ev:
                log.debug("%s is set to %s" %
                          ("MACPORT_LOCATION", ev["MACPORT_LOCATION"]))
                mac_bin = os.path.join(ev["MACPORT_LOCATION"], "bin")

                if "PATH" in ev:
                    ev["PATH"] = pathPrepend(ev["PATH"],
                                             mac_bin,
                                             exist_check=opts.strip_path,
                                             unique=opts.strip_path)
                elif os.path.exists(mac_bin):
                    ev["PATH"] = mac_bin

                mac_man = os.path.join(ev["MACPORT_LOCATION"], "man")
                if "MANPATH" in ev:
                    ev["MANPATH"] = pathPrepend(ev["MANPATH"],
                                                mac_man,
                                                exist_check=opts.strip_path,
                                                unique=opts.strip_path)
                elif os.path.exists(mac_man):
                    ev["MANPATH"] = mac_man

        self.fixPath()

#-------------------------------------------------------------------------

    def setHomeDir(self):
        ev = self.Environment()
        log = logging.getLogger()
        if sys.platform == "win32" and not ev.has_key("HOME"):
            ev["HOME"] = os.path.join(ev["HOMEDRIVE"], ev["HOMEPATH"])
            log.debug("Setting HOME to %s" % ev["HOME"])
        if sys.platform != "win32":
            username = ev["USER"]
        else:
            username = ev["USERNAME"]
        log.debug("User name is %s" % username)

        if sys.platform != "win32" and self.targetShell() == "sh" and ev.has_key("HOME"):
            hprof = os.path.join(ev["HOME"], ".bash_profile")
            sprof = os.path.join("/etc", "skel", ".bash_profile")
            hlist = []
            hlist.append(hprof)
            hlist.append(os.path.join(ev["HOME"], ".bash_login"))
            hlist.append(os.path.join(ev["HOME"], ".profile"))
            if not [x for x in hlist if os.path.exists(x)]:
                if os.path.exists(sprof):
                    try:
                        shutil.copy(sprof, hprof)
                        log.warning("Copying %s to %s" % (sprof, hprof))
                    except IOError:
                        log.warning("Failed to copy %s to %s" % (sprof, hprof))
            hbrc = os.path.join(ev["HOME"], ".bashrc")
            sbrc = os.path.join("/etc", "skel", ".bashrc")
            if not os.path.exists(hbrc):
                if os.path.exists(sbrc):
                    try:
                        shutil.copy(sbrc, hbrc)
                        log.warning("Copying %s to %s" % (sbrc, hbrc))
                    except IOError:
                        log.warning("Failed to copy %s to %s" % (sbrc, hbrc))
        if not ev.has_key("LD_LIBRARY_PATH"):
            ev["LD_LIBRARY_PATH"] = ""
            log.debug("Setting a default LD_LIBRARY_PATH")

        if not ev.has_key("ROOTSYS"):
            ev["ROOTSYS"] = ""
            log.debug("Setting a default ROOTSYS")

        self.setUserArea()

    def setUserArea(self):
        log = logging.getLogger()
        opts = self.options
        ev = self.Environment()
        if not opts.remove_userarea:
            newdir = False
            if not opts.userarea:
                # @todo: use something different for window
                opts.userarea = os.path.join(ev["HOME"], "Work", "Projects")
            ev["User_area"] = opts.userarea
            log.debug("User_area is set to %s" % ev["User_area"])

            rename_cmakeuser = False
            # is a file, a directory or a valid link
            if os.path.exists(opts.userarea):
                # is a file or a link pointing to a file
                if os.path.isfile(opts.userarea):
                    log.warning("%s is a file" % opts.userarea)
                    rename_cmakeuser = True
                    newdir = True
                # is a directory or a link pointing to a directory. Nothing to
                # do
                else:
                    log.debug("%s is a directory" % opts.userarea)
            else:  # doesn't exist or is an invalid link
                if os.path.islink(opts.userarea):  # broken link
                    log.warning("%s is a broken link" % opts.userarea)
                    rename_cmakeuser = True
                newdir = True
            if rename_cmakeuser:
                bak_userarea = opts.userarea + "_bak"
                if not os.path.exists(bak_userarea):
                    if os.path.islink(bak_userarea):
                        try:
                            os.remove(bak_userarea)  # remove broken link
                        except IOError:
                            log.warning("Can't remove %s" % bak_userarea)
                    try:
                        os.rename(opts.userarea, opts.userarea + "_bak")
                        log.warning("Renamed %s into %s" %
                                    (opts.userarea, opts.userarea + "_bak"))
                    except IOError:
                        log.warning("Can't rename %s into %s" %
                                    (opts.userarea, opts.userarea + "_bak"))
                else:
                    log.warning(
                        "Can't backup %s because %s is in the way" % (opts.userarea, bak_userarea))
                    log.warning("No %s directory created" % opts.userarea)
                    newdir = False
            if newdir:
                try:
                    os.makedirs(opts.userarea)
                    self.addEcho(
                        " --- a new User_area directory has been created in your HOME directory")
                except IOError:
                    log.warning("Can't create %s" % opts.userarea)
        elif ev.has_key("User_area"):
            del ev["User_area"]
            log.debug("Removed User_area from the environment")

    def getSupportedBinaryTag(self):
        """
        returns the best matched BINARY_TAG for the wilcard string
        """
        theconf = None
        log = logging.getLogger()

        if self._target_binary_type:
            log.debug("Guessing BINARY_TAG for the %s type" %
                      self._target_binary_type)
            supported_configs = self._nativemachine.supportedBinaryTag(
                all_types=True)
            supported_configs = [
                s for s in supported_configs if isBinaryType(s, self._target_binary_type)]
        else:
            log.debug("Guessing BINARY_TAG")
            supported_configs = self._nativemachine.supportedBinaryTag()

        if supported_configs:
            theconf = supported_configs[0]

        return theconf

    def setBinaryTag(self):
        ev = self.Environment()
        opts = self.options
        log = logging.getLogger()
        self.binary = None
        self.platform = None
        self.compdef = None

        if self._target_binary_type:
            # the type has been explicitly set on the command line as argument
            if opts.binary_tag:
                log.debug("Ignoring the provided BINARY_TAG %s" %
                          opts.binary_tag)
            theconf = self.getSupportedBinaryTag()
        else:
            if opts.binary_tag:
                # the binary has either beeen passed with the -b option or
                # with the BINARY_TAG env variable
                log.debug("Using the provided BINARY_TAG %s" % opts.binary_tag)
                theconf = opts.binary_tag
            else:
                # the type is completely guessed
                theconf = self.getSupportedBinaryTag()
                if not theconf:
                    log.debug("Falling back on the native BINARY_TAG")
                    theconf = self._nativemachine.nativeBinaryTag()
            if theconf:
                self._target_binary_type = getBinaryTypeName(theconf)

        if theconf:
            self.binary = getArchitecture(theconf)
            self.platform = getPlatformType(theconf)
            self.compdef = getCompiler(theconf)
            opts.binary_tag = theconf
        else:
            log.error("Cannot set the BINARY_TAG environment variable")

        supported_binarytags = self._nativemachine.supportedBinaryTag(
            all_types=True)
        if opts.binary_tag not in supported_binarytags:
            log.warning(
                "%s is not in the list of distributed configurations" % opts.binary_tag)
            if supported_binarytags:
                log.warning(
                    "Please switch to a supported one with 'ELogin -b <binary_tag>' before building")
                log.warning("Supported binary tags: %s" %
                            ", ".join(supported_binarytags))

        if sys.platform == "win32":
            ev["BINARY_TAG"] = getBinaryOfType(theconf, "Debug")
        else:
            ev["BINARY_TAG"] = opts.binary_tag

        log.debug("BINARY_TAG is set to %s" % ev["BINARY_TAG"])

    def setSGShostos(self):
        '''
        Set the environment variable SGS_hostos, used by the 'sgs-' compiler wrappers.
        '''
        ev = self.Environment()
        nm = self._nativemachine
        # we take only the first two elements of the native BINARY_TAG, e.g.
        #  x86_64-slc5-gcc46-opt -> x86_64-slc5
        ev['SGS_hostos'] = '-'.join(nm.nativeBinaryTag().split('-')[:2])

    def setCMakePath(self):
        ev = self.Environment()
        opts = self.options
        log = logging.getLogger()

        self.setHomeDir()

        prefix_path = []

        if not opts.remove_userarea and ev.has_key("User_area"):
            prefix_path.append(ev["User_area"])

        if opts.sharedarea:
            ev["EUCLIDPROJECTPATH"] = opts.sharedarea

        if "EUCLIDPROJECTPATH" not in ev:
            if os.path.exists("/opt/euclid"):
                ev["EUCLIDPROJECTPATH"] = "/opt/euclid"

        if "EUCLIDPROJECTPATH" in ev:
            prefix_path.append(ev["EUCLIDPROJECTPATH"])

        if not opts.remove_userarea and ev.has_key("User_area"):
            prefix_path.append(ev["User_area"])

        if "CMAKE_PROJECT_PATH" not in ev:
            ev["CMAKE_PROJECT_PATH"] = ""

        for p in prefix_path:
            ev["CMAKE_PROJECT_PATH"] = pathPrepend(ev["CMAKE_PROJECT_PATH"],
                                                   p,
                                                   exist_check=opts.strip_path,
                                                   unique=opts.strip_path)

        log.debug("CMAKE_PROJECT_PATH is set to %s" % ev["CMAKE_PROJECT_PATH"])

        if "MACPORT_LOCATION" in ev:
            if "CMAKEFLAGS" in ev:
                ev["CMAKEFLAGS"] += " -DCMAKE_FIND_FRAMEWORK=LAST"
                ev["CMAKEFLAGS"] += " -DCMAKE_FIND_ROOT_PATH=%s" % ev["MACPORT_LOCATION"]
            else:
                ev["CMAKEFLAGS"] = "-DCMAKE_FIND_FRAMEWORK=LAST"
                ev["CMAKEFLAGS"] += " -DCMAKE_FIND_ROOT_PATH=%s" % ev["MACPORT_LOCATION"]

    def copyEnv(self):
        ev = self.Environment()
        retenv = dict(ev.env)
        al = self.Aliases()
        retaliases = dict(al.env)
        retextra = self.extra()
        return retenv, retaliases, retextra

    def setEnv(self):
        log = logging.getLogger()
        log.debug("Entering the environment setup")
        self.setPath()

        self.setBinaryTag()
        self.setCMakePath()

        # this is use internally by the 'sgs-' compiler wrapper.
        self.setSGShostos()

        # return a copy otherwise the environment gets restored
        # at the destruction of the instance

        return self.copyEnv()[0]

    def setAliases(self):
        al = self.Aliases()
        if self.targetShell() == "sh":
            al["ELogin"] = ". \\`/usr/bin/which  ELogin.%s\\`" % self.targetShell()
        else:
            al["ELogin"] = "source \\`/usr/bin/which ELogin.%s\\`" % self.targetShell()

        al["ERun"] = "E-Run"
        al["EuclidRun"] = "E-Run"

        return self.copyEnv()[1]

    def setExtra(self):
        #        ex = self.extra()
        return self.copyEnv()[2]

    def manifest(self, binary_type=default_build_type):
        ev = self.Environment()
        opts = self.options
        if opts.log_level != "CRITICAL":
            self.addEcho("*" * 80)
            vers = __version__
            if vers:
                self.addEcho(
                    "*" + ("---- Euclid Login %s ----" % vers).center(78) + "*")
            else:
                self.addEcho(
                    "*" + "---- Euclid Login ----".center(78) + "*")
            if self.binary:
                self.addEcho("*" + ("Building with %s on %s %s system (%s)" % (
                    self.compdef, self.platform, self.binary, ev["BINARY_TAG"])).center(78) + "*")
            else:  # for windows
                self.addEcho("*" + ("Building with %s on %s system (%s)" %
                                    (self.compdef, self.platform, ev["BINARY_TAG"])).center(78) + "*")
            self.addEcho("*" * 80)
            if ev.has_key("User_area"):
                self.addEcho(" --- User_area is set to %s" % ev["User_area"])
            if ev.has_key("EUCLIDPROJECTPATH"):
                self.addEcho(" --- EUCLIDPROJECTPATH is set to:")
                for p in ev["EUCLIDPROJECTPATH"].split(os.pathsep):
                    if p:
                        self.addEcho("    %s" % p)
            if self._nativemachine.OSType() == "Darwin" and opts.use_macport:
                if ev.has_key("MACPORT_LOCATION"):
                    self.addEcho(" --- Using MacPort location from %s" %
                                 ev["MACPORT_LOCATION"])
            self.addEcho("-" * 80)

    def parseOpts(self, args):
        SourceScript.parseOpts(self, args)
        for a in self.args:
            for b in build_types:
                if a.lower() == b.lower():
                    self._target_binary_type = b
                elif a.lower() == build_types[b].lower():
                    self._target_binary_type = b

    def main(self):
        opts = self.options

        log = logging.getLogger()

        if has_prefix:
            log.debug("The installation prefix is: %s" % my_own_prefix)

        # first part: the environment variables
        if not opts.shell_only:
            self.setEnv()

        # second part the aliases
        self.setAliases()

        if not opts.shell_only:
            # the shell-only part has to be completely silent
            self.manifest()

        self.flush()

        return 0


if __name__ == '__main__':
    sys.exit(LoginScript(usage="%prog [options] [type]").run())
