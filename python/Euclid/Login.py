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
my_own_prefix="%(this_install_prefix)s"
has_prefix = False

if os.path.exists(my_own_prefix) :
    has_prefix = True

if has_prefix :
    from distutils.sysconfig import get_python_lib
    python_loc=get_python_lib(prefix=my_own_prefix)
else :
    # use the local properties if the intall_path is no available
    try:
        _this_file = __file__
    except NameError :
        # special procedure to handle the situation when __file__ is not defined.
        # It happens typically when trying to use pdb.
        from imp import find_module, load_module
        _ff, _filename, _desc = find_module("Euclid")
        try :
            lbconf_package = load_module('Euclid', _ff, _filename, _desc)
            _ff, _filename, _desc = find_module('Login', lbconf_package.__path__)
            _this_file = _filename
        finally :
            _ff.close()
    # Bootstrapping the python location
    _pyeuc_dir = os.path.dirname(_this_file)
    _py_dir = os.path.dirname(_pyeuc_dir)
    if os.path.basename(_pyeuc_dir) == "Euclid" :
        _base_dir = os.path.dirname(_py_dir)
        python_loc = _py_dir
        
sys.path.insert(0, python_loc)
#============================================================================

from Euclid.Platform import getBinaryDbg, getBinaryOpt
from Euclid.Platform import getCompiler, getPlatformType, getArchitecture
from Euclid.Platform import isBinaryDbg, NativeMachine
from Euclid.Version import ParseSvnVersion
from Euclid.Script import SourceScript
from Euclid.Path import pathPrepend, getClosestPath
import logging
import shutil

__version__ = ParseSvnVersion("$Id$", "$URL$")
#-----------------------------------------------------------------------------------
# Helper functions

def getELoginEnv(optionlist=None):
    if not optionlist :
        optionlist = []
    s = ELoginScript()
    s.parseOpts(optionlist)
    return s.setEnv()[0]

def getELoginAliases(optionlist=None):
    if not optionlist :
        optionlist = []
    s = ELoginScript()
    s.parseOpts(optionlist)
    return s.setEnv()[1]

def getELoginExtra(optionlist=None):
    if not optionlist :
        optionlist = []
    s = ELoginScript()
    s.parseOpts(optionlist)
    return s.setEnv()[2]

#-----------------------------------------------------------------------------------

class ELoginScript(SourceScript):
    _version = __version__
    _description = __doc__
    def __init__(self, usage=None, version=None):
        SourceScript.__init__(self, usage, version)
        self.platform = ""
        self.binary = ""
        self.compdef = ""
        self._nativemachine = None
        self._triedlocalsetup = False
        self._triedAFSsetup = False

#-----------------------------------------------------------------------------------
# Option definition

    def defineOpts(self):
        """ define commandline options """
        parser = self.parser
        parser.set_defaults(binary_tag=None)
        parser.add_option("-b", "--binary-tag",
                          dest="binary_tag",
                          help="set BINARY_TAG.",
                          fallback_env="BINARY_TAG")
        parser.set_defaults(wbinary_tag=None)
        parser.add_option("-w", "--wildcard-binary-tag",
                          dest="wbinary_tag",
                          help="choose the first BINARY_TAG that match the string in the list of supported ones")
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
#-----------------------------------------------------------------------------------

    def setPath(self):
        ev = self.Environment()
        opts = self.options
        log = logging.getLogger()
        if not opts.strip_path :
            log.debug("Disabling the path stripping")
            ev["E_NO_STRIP_PATH"] = "1"
        else :
            if ev.has_key("E_NO_STRIP_PATH") :
                log.debug("Reenabling the path stripping")
                del ev["E_NO_STRIP_PATH"]

        ev["PYTHONPATH"] = pathPrepend(ev["PYTHONPATH"], 
                                      python_loc, 
                                      exist_check=opts.strip_path, 
                                      unique=opts.strip_path)

        log.debug("%s is set to %s" % ("PYTHONPATH", ev["PYTHONPATH"]) )
        
        bin_loc = getClosestPath(python_loc, os.sep.join(["bin", "ELogin.sh"]), alloccurences=False)
        if not bin_loc :
            bin_loc = getClosestPath(python_loc, os.sep.join(["scripts", "ELogin.sh"]), alloccurences=False)
        if bin_loc :
            the_loc = os.path.dirname(bin_loc[0])
            ev["PATH"] = pathPrepend(ev["PATH"], 
                                     the_loc, 
                                     exist_check=opts.strip_path, 
                                     unique=opts.strip_path)
            
        log.debug("%s is set to %s" % ("PATH", ev["PATH"]) )
        

        # try the installed directory in $prefix/share/EuclidEnv/cmake/...
        cmake_loc = getClosestPath(python_loc, 
                                   os.sep.join(["share", "EuclidEnv", "cmake", "ElementsProjectConfig.cmake"]), 
                                   alloccurences=False)
        if not cmake_loc:
            # use the local source directory
            cmake_loc = getClosestPath(python_loc, 
                                       os.sep.join(["data", "cmake", "ElementsProjectConfig.cmake"]), 
                                       alloccurences=False)
            
        if cmake_loc :
            the_loc = os.path.dirname(cmake_loc[0])
            if "CMAKE_PREFIX_PATH" in ev :
                ev["CMAKE_PREFIX_PATH"] = pathPrepend(ev["CMAKE_PREFIX_PATH"], 
                                                      the_loc, 
                                                      exist_check=opts.strip_path, 
                                                      unique=opts.strip_path)
            elif os.path.exists(the_loc) :
                ev["CMAKE_PREFIX_PATH"] = the_loc

        if "CMAKE_PREFIX_PATH" in ev :
            log.debug("%s is set to %s" % ("CMAKE_PREFIX_PATH", ev["CMAKE_PREFIX_PATH"]) )

#-----------------------------------------------------------------------------------

    def setHomeDir(self):
        ev = self.Environment()
        log = logging.getLogger()
        if sys.platform == "win32" and not ev.has_key("HOME") :
            ev["HOME"] = os.path.join(ev["HOMEDRIVE"], ev["HOMEPATH"])
            log.debug("Setting HOME to %s" % ev["HOME"])
        if sys.platform != "win32" :
            username = ev["USER"]
        else :
            username = ev["USERNAME"]
        log.debug("User name is %s" % username)

        if sys.platform != "win32" and self.targetShell() == "sh" and ev.has_key("HOME"):
            hprof = os.path.join(ev["HOME"], ".bash_profile")
            sprof = os.path.join("/etc", "skel", ".bash_profile")
            hlist = []
            hlist.append(hprof)
            hlist.append(os.path.join(ev["HOME"], ".bash_login"))
            hlist.append(os.path.join(ev["HOME"], ".profile"))
            if not [ x for x in hlist if os.path.exists(x) ] :
                if os.path.exists(sprof) :
                    try :
                        shutil.copy(sprof, hprof)
                        log.warning("Copying %s to %s" % (sprof, hprof))
                    except IOError :
                        log.warning("Failed to copy %s to %s" % (sprof, hprof) )
            hbrc = os.path.join(ev["HOME"], ".bashrc")
            sbrc = os.path.join("/etc", "skel", ".bashrc")
            if not os.path.exists(hbrc) :
                if os.path.exists(sbrc) :
                    try :
                        shutil.copy(sbrc, hbrc)
                        log.warning("Copying %s to %s" % (sbrc, hbrc))
                    except IOError :
                        log.warning("Failed to copy %s to %s" % (sbrc, hbrc) )
        if not ev.has_key("LD_LIBRARY_PATH") :
            ev["LD_LIBRARY_PATH"] = ""
            log.debug("Setting a default LD_LIBRARY_PATH")

        if not ev.has_key("ROOTSYS") :
            ev["ROOTSYS"] = ""
            log.debug("Setting a default ROOTSYS")

        self.setUserArea()

    def setUserArea(self):
        log = logging.getLogger()
        opts = self.options
        ev = self.Environment()
        if not opts.remove_userarea :
            newdir = False
            if not opts.userarea :
                opts.userarea = os.path.join(ev["HOME"], "Work") # @todo: use something different for window
            ev["User_area"] = opts.userarea
            log.debug("User_area is set to %s" % ev["User_area"])

            rename_cmakeuser = False
            if os.path.exists(opts.userarea) : # is a file, a directory or a valid link
                if os.path.isfile(opts.userarea) : # is a file or a link pointing to a file
                    log.warning("%s is a file"  % opts.userarea)
                    rename_cmakeuser = True
                    newdir = True
                else : # is a directory or a link pointing to a directory. Nothing to do
                    log.debug("%s is a directory" % opts.userarea)
            else : # doesn't exist or is an invalid link
                if os.path.islink(opts.userarea) : # broken link
                    log.warning("%s is a broken link"  % opts.userarea)
                    rename_cmakeuser = True
                newdir = True
            if rename_cmakeuser :
                bak_userarea = opts.userarea + "_bak"
                if not os.path.exists(bak_userarea) :
                    if os.path.islink(bak_userarea) :
                        try :
                            os.remove(bak_userarea) # remove broken link
                        except IOError:
                            log.warning("Can't remove %s" % bak_userarea)
                    try :
                        os.rename(opts.userarea, opts.userarea + "_bak")
                        log.warning("Renamed %s into %s" % (opts.userarea, opts.userarea + "_bak"))
                    except IOError:
                        log.warning("Can't rename %s into %s" % (opts.userarea, opts.userarea + "_bak"))
                else :
                    log.warning("Can't backup %s because %s is in the way" % (opts.userarea, bak_userarea))
                    log.warning("No %s directory created" % opts.userarea)
                    newdir = False
            if newdir :
                try :
                    os.makedirs(opts.userarea)
                    self.addEcho(" --- a new User_area directory has been created in your HOME directory")
                except IOError:
                    log.warning("Can't create %s" % opts.userarea)
        elif ev.has_key("User_area") :
            del ev["User_area"]
            log.debug("Removed User_area from the environment")



    def getWildCardBinaryTag(self, wildcard=None, debug=False):
        """
        returns the best matched BINARY_TAG for the wilcard string
        @param wildcard: text to be look for in the BINARY_TAG
        @type wildcard: string
        @param debug: if the searched list includes also the dbg BINARY_TAG
        @type debug: boolean
        """
        log = logging.getLogger()
        theconf = None
        supported_configs = self._nativemachine.supportedBinaryTag(debug=debug)
        
        supconf = supported_configs

        if wildcard :
            log.debug("Looking for %s in the list of selected BINARY_TAGs." % wildcard)
            supconf = [ c for c in supconf if wildcard in c ]

        if supconf :
            theconf = supconf[0]
            if theconf not in supported_configs :
                log.warning("%s is not in the list of distributed configurations" % theconf)
                if supported_configs :
                    log.warning("Please switch to a supported one with 'LbLogin -c' before building")
                    log.warning("Supported configs: %s" % ", ".join(supported_configs))

        return theconf

    def setBinaryTag(self, debug=False):
        ev = self.Environment()
        opts = self.options
        log = logging.getLogger()
        self.binary = None
        self.platform = None
        self.compdef = None
        if not opts.wbinary_tag :
            if opts.binary_tag :
                log.debug("Using provided BINARY_TAG %s" % opts.binary_tag)
                theconf = opts.binary_tag
            else :
                log.debug("Guessing BINARY_TAG")
                theconf = self.getWildCardBinaryTag(debug=debug)
                if not theconf :
                    log.debug("Falling back on the native BINARY_TAG")
                    theconf = self._nativemachine.nativeBinaryTag(debug=debug)
        else :
            theconf = self.getWildCardBinaryTag(wildcard=opts.wbinary_tag, debug=True)
            if not theconf :
                if opts.binary_tag :
                    log.debug("Falling back on the previous BINARY_TAG")
                    theconf = opts.binary_tag
                else :
                    log.debug("Falling back on the native BINARY_TAG")
                    theconf = self._nativemachine.nativeBinaryTag(debug=debug)

        if theconf :
            if isBinaryDbg(theconf) :
                debug = True
            self.binary = getArchitecture(theconf)
            self.platform = getPlatformType(theconf)
            self.compdef = getCompiler(theconf)
            opts.binary_tag = theconf


        if debug or sys.platform == "win32" :
            ev["BINARY_TAG"] = getBinaryDbg(theconf)
        else :
            ev["BINARY_TAG"] = getBinaryOpt(theconf)
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


        if not opts.remove_userarea and ev.has_key("User_area") :
            prefix_path.append(ev["User_area"])
        
        if opts.sharedarea :
            ev["EUCLIDPROJECTPATH"] = opts.sharedarea
            
        if "EUCLIDPROJECTPATH" not in ev :
            if os.path.exists("/opt/Euclid") :
                ev["EUCLIDPROJECTPATH"] = "/opt/Euclid"
                
        if "EUCLIDPROJECTPATH" in ev :
            prefix_path.append(ev["EUCLIDPROJECTPATH"])


        if not opts.remove_userarea and ev.has_key("User_area") :
            prefix_path.append(ev["User_area"])
        
        if "CMAKE_PROJECT_PATH" not in ev:
            ev["CMAKE_PROJECT_PATH"] = ""

        for p in prefix_path:
            ev["CMAKE_PROJECT_PATH"] = pathPrepend(ev["CMAKE_PROJECT_PATH"], 
                                                      p, 
                                                      exist_check=opts.strip_path, 
                                                      unique=opts.strip_path)

        log.debug("CMAKE_PROJECT_PATH is set to %s" % ev["CMAKE_PROJECT_PATH"])


    def copyEnv(self):
        ev = self.Environment()
        retenv = dict(ev.env)
        al = self.Aliases()
        retaliases = dict(al.env)
        retextra = self.extra()
        return retenv, retaliases, retextra

    def setEnv(self, debug=False):
        log = logging.getLogger()
        log.debug("Entering the environment setup")
        self.setPath()

        self._nativemachine = NativeMachine()
        self.setBinaryTag(debug)
        self.setCMakePath()

        # this is use internally by the 'sgs-' compiler wrapper.
        self.setSGShostos()

        # return a copy otherwise the environment gets restored
        # at the destruction of the instance

        return self.copyEnv()

    def setAliases(self, debug=False):
        al = self.Aliases()
        if self.targetShell() == "sh" :
            al["ELogin"] = ". \\`/usr/bin/which  ELogin.%s\\`" % self.targetShell()
        else :
            al["ELogin"] = "source \\`/usr/bin/which ELogin.%s\\`" % self.targetShell()

        return self.copyEnv()



    def manifest(self, debug=False):
        ev = self.Environment()
        opts = self.options
        if opts.log_level != "CRITICAL" :
            self.addEcho("*" * 80)
            self.addEcho("*" + "---- Euclid Login ----".center(78) + "*")
            if self.binary :
                self.addEcho("*" + ("Building with %s on %s %s system (%s)" % (self.compdef, self.platform, self.binary, ev["BINARY_TAG"])).center(78) + "*")
            else : # for windows
                self.addEcho("*" + ("Building with %s on %s system (%s)" % (self.compdef, self.platform, ev["BINARY_TAG"])).center(78) + "*")
            self.addEcho("*" * 80)
            if ev.has_key("User_area") :
                self.addEcho(" --- User_area is set to %s" % ev["User_area"])
            if ev.has_key("EUCLIDPROJECTPATH") :
                self.addEcho(" --- EUCLIDPROJECTPATH is set to:")
                for p in ev["EUCLIDPROJECTPATH"].split(os.pathsep) :
                    if p :
                        self.addEcho("    %s" % p)


            self.addEcho("-" * 80)


    def main(self):
        opts = self.options
        debug = False
        for a in self.args :
            if a == "debug" :
                debug = True
        # first part: the environment variables
        if not opts.shell_only :
            self.setEnv(debug)
            
        # second part the aliases    
        self.setAliases(debug)

        if not opts.shell_only :
            # the shell-only part has to be completely silent
            self.manifest(debug)

        self.flush()

        return 0


if __name__ == '__main__':
    sys.exit(ELoginScript(usage="%prog [options] [debug]").run())

