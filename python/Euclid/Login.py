#!/usr/bin/python
""" Main script to setup the basic Euclid environment """

import sys
import os

#============================================================================
# bootstrapping the location of the file
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

_pyconf_dir = os.path.dirname(_this_file)
_py_dir = os.path.dirname(_pyconf_dir)
_base_dir = os.path.dirname(_py_dir)
_ia_dir = _base_dir
_iapy_dir = os.path.join(_ia_dir, "python")

# added the installarea if I am called from the local package
if os.path.basename(_base_dir) != "InstallArea" :
    _ia_dir = os.path.join(os.path.dirname(_base_dir), "InstallArea")
    _iapy_dir = os.path.join(_ia_dir, "python")
    if os.path.isdir(_iapy_dir) :
        sys.path.insert(0, _iapy_dir)

_lbs_home_dir = os.path.dirname(_ia_dir)

# updating the sys.path for the bare minimum of the available scripts
sys.path.insert(0, _pyconf_dir)
sys.path.insert(0, _py_dir)


# needed for the cache use
_scripts_dir = os.path.join(_base_dir, "scripts")
#============================================================================


from SetupProject import SetupProject

from Euclid.Platform import getBinaryDbg, getBinaryOpt
from Euclid.Platform import getCompiler, getPlatformType, getArchitecture
from Euclid.Platform import isBinaryDbg, NativeMachine
from LbConfiguration.External import CMT_version, CMake_version
from Euclid.Version import sortStrings, ParseSvnVersion
from Euclid.Script import SourceScript
from Euclid.Path import multiPathGet, multiPathGetFirst, multiPathJoin
from Euclid.Path import envPathPrepend, pathAdd
import logging
import shutil

__version__ = ParseSvnVersion("$Id: LbLogin.py 147640 2012-11-05 16:51:30Z marcocle $", "$URL: svn+ssh://svn.cern.ch/reps/lhcb/LbScripts/trunk/LbConfiguration/python/LbConfiguration/LbLogin.py $")
#-----------------------------------------------------------------------------------
# Helper functions


def getLbLoginEnv(optionlist=None):
    if not optionlist :
        optionlist = []
    s = LbLoginScript()
    s.parseOpts(optionlist)
    return s.setEnv()[0]

#-----------------------------------------------------------------------------------
# Option callbacks

def _setCMTVersionCb(_option, _opt_str, value, parser):
    if parser.values.cmtvers != value :
        parser.values.cmtvers = value

def _setCMakeVersionCb(_option, _opt_str, value, parser):
    if parser.values.cmakevers != value :
        parser.values.cmakevers = value

def _noPythonCb(_option, _opt_str, _value, parser):
    parser.values.get_python = False

def _userAreaScriptsCb(_option, _opt_str, _value, parser):
    parser.values.user_area_scripts = True

def _useDevCb(_option, _opt_str, _value, parser):
    parser.values.usedevarea = True

def _pythonVerCb(_option, _opt_str, value, parser):
    parser.values.pythonvers = value
    parser.values.get_python = True

#-----------------------------------------------------------------------------------

class LbLoginScript(SourceScript):
    _version = __version__
    _description = __doc__
    def __init__(self, usage=None, version=None):
        SourceScript.__init__(self, usage, version)
        self.platform = ""
        self.binary = ""
        self.compdef = ""
        self._nativemachine = None
        self._currentcmtroot = os.environ.get("CMTROOT", None)
        self._triedlocalsetup = False
        self._triedAFSsetup = False

#-----------------------------------------------------------------------------------
# Option definition

    def defineOpts(self):
        """ define commandline options """
        parser = self.parser
        parser.set_defaults(mysiteroot=None)
        parser.add_option("-m", "--mysiteroot",
                          dest="mysiteroot",
                          help="set MYSITEROOT.")
        parser.set_defaults(cmtsite=None)
        parser.add_option("--cmtsite",
                          dest="cmtsite",
                          help="set the CMTSITE.",
                          fallback_env="CMTSITE")
        parser.set_defaults(cmtconfig=None)
        parser.add_option("-c", "--cmtconfig",
                          dest="cmtconfig",
                          help="set CMTCONFIG.",
                          fallback_env="CMTCONFIG")
        parser.set_defaults(wcmtconfig=None)
        parser.add_option("-w", "--wildcard-cmtconfig",
                          dest="wcmtconfig",
                          help="choose the first CMTCONFIG that match the string in the list of supported ones")
        parser.set_defaults(userarea=None)
        parser.add_option("-u", "--userarea",
                          dest="userarea",
                          help="set User_release_area.",
                          fallback_env="User_release_area")
        parser.set_defaults(nightlies_dir=None)
        parser.add_option("-n", "--nightlies-dir",
                          dest="nightlies_dir",
                          help="set nightlies directory.",
                          fallback_env="LHCBNIGHTLIES")
        parser.set_defaults(remove_userarea=False)
        parser.add_option("--no-userarea",
                          dest="remove_userarea",
                          action="store_true",
                          help="prevent the addition of a user area [default: %default]")
        parser.set_defaults(cmtvers=CMT_version)
        parser.add_option("--cmtvers",
                          action="callback",
                          callback=_setCMTVersionCb,
                          type="string",
                          help="set CMT version")
        parser.set_defaults(cmakevers=CMake_version)
        parser.add_option("--cmakevers",
                          action="callback",
                          callback=_setCMakeVersionCb,
                          type="string",
                          help="set CMake version")
        parser.set_defaults(scriptsvers=None)
        parser.add_option("--scripts-version",
                          dest="scriptsvers",
                          help="version of LbScripts to be setup [default: %default]")
        parser.set_defaults(usedevarea=False)
        parser.add_option("--dev",
                          dest="usedevarea",
                          action="callback",
                          callback=_useDevCb,
                          help="add the LHCBDEV area for the LbScripts setup [default: %default]")
        parser.set_defaults(pythonvers=None)
        parser.add_option("--python-version",
                          dest="pythonvers",
                          action="callback",
                          callback=_pythonVerCb,
                          help="version of python to be setup [default: %default]")
        parser.set_defaults(get_python=True)
        parser.add_option("--no-python",
                          action="callback",
                          callback=_noPythonCb,
                          help="prevents the python setup")
        parser.set_defaults(sharedarea=None)
        parser.add_option("-s", "--shared",
                          dest="sharedarea",
                          help="set the shared area",
                          fallback_env="VO_LHCB_SW_DIR")
        parser.set_defaults(no_compat=False)
        parser.add_option("--no-compat",
                          dest="no_compat",
                          action="store_true",
                          help="prevent the usage of the Compat project in SetupProject[default: %default]")
        parser.add_option("--use-compat",
                          dest="no_compat",
                          action="store_false",
                          help="add the usage of the Compat project in SetupProject")
        parser.set_defaults(compat_prepend=None)
        parser.add_option("--compat-prepend",
                          dest="compat_prepend",
                          action="store_true",
                          help="(internal) Prepend the Compat env to the script env[default: %default]")
        parser.add_option("--no-compat-prepend",
                          dest="compat_prepend",
                          action="store_false",
                          help="(internal) prevent the usage of the Compat env in the script")
        parser.set_defaults(compat_version="v*")
        parser.add_option("--compat-version",
                          dest="compat_version",
                          help="Set the vesion of the Compat project to use [default %default")
        parser.set_defaults(strip_path=True)
        parser.add_option("--no-strip-path",
                          dest="strip_path",
                          action="store_false",
                          help="prevent the cleanup of invalid entries in pathes")
        parser.add_option("--strip-path",
                          dest="strip_path",
                          action="store_true",
                          help="activate the cleanup of invalid entries in pathes [default: %default]")
        parser.set_defaults(user_area_scripts=False)
        parser.add_option("--user-area-scripts",
                          action="callback",
                          callback=_userAreaScriptsCb,
                          help="Enable the usage of the user release area for the setup of the scripts. Use with care. [default: %default]")
        parser.set_defaults(use_cmtextratags=False)
        parser.add_option("--dont-use-cmtextratags",
                          dest="use_cmtextratags",
                          action="store_false",
                          help="prevent the usage of CMTEXTRATAGS during the LbScripts setup [default]")
        parser.add_option("--use-cmtextratags",
                          dest="use_cmtextratags",
                          action="store_true",
                          help="use CMTEXTRATAGS during the LbScripts setup")

#-----------------------------------------------------------------------------------

    def setPath(self):
        ev = self.Environment()
        opts = self.options
        log = logging.getLogger()
        log.debug("%s is set to %s" % ("PATH", ev["PATH"]) )
        if not opts.strip_path :
            log.debug("Disabling the path stripping")
            ev["E_NO_STRIP_PATH"] = "1"
        else :
            if ev.has_key("E_NO_STRIP_PATH") :
                log.debug("Reenabling the path stripping")
                del ev["E_NO_STRIP_PATH"]




#-----------------------------------------------------------------------------------
# Core CMT business

    def setCMTBin(self):
        log = logging.getLogger()
        ev = self.Environment()
        if not self._nativemachine :
            self._nativemachine = NativeMachine()
        ev["CMTBIN"] = self._nativemachine.CMTSystem()
        log.debug("CMTBIN is set to %s" % ev["CMTBIN"])

    def hasCommand(self, cmd):
        hascmd = False
        f = os.popen("which %s >& /dev/null" % cmd)
        f.read()
        if f.close() is None :
            hascmd = True
        return hascmd

    def setCMTSystem(self):
        log = logging.getLogger()
        ev = self.Environment()
        if sys.platform != "win32" :
            system = ev["CMTBIN"]
        else :
            if ev.has_key("CMTCONFIG") :
                system = ev["CMTCONFIG"]
            else :
                system = ev["CMTBIN"]
        log.debug("CMT system is set to %s" % system)
        return system



#-----------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------

    def setHomeDir(self):
        ev = self.Environment()
        opts = self.options
        log = logging.getLogger()
        if sys.platform == "win32" and not ev.has_key("HOME") :
            ev["HOME"] = os.path.join(ev["HOMEDRIVE"], ev["HOMEPATH"])
            log.debug("Setting HOME to %s" % ev["HOME"])
        homedir = ev["HOME"]
        rhostfile = os.path.join(homedir, ".rhosts")
        if sys.platform != "win32" :
            username = ev["USER"]
        else :
            username = ev["USERNAME"]
        log.debug("User name is %s" % username)
        if not os.path.exists(rhostfile) and sys.platform != "win32" :
            self.addEcho("Creating a %s file to use CMT" % rhostfile)
            self.addEcho("Joel.Closier@cern.ch")
            try :
                f = open(rhostfile, "w")
                f.write("+ %s\n" % username)
                f.close()
            except IOError:
                log.warning("Can't create the file %s" % rhostfile)
        # remove any .cmtrc file stored in the $HOME directory
        cmtrcfile = os.path.join(homedir, ".cmtrc")
        if os.path.exists(cmtrcfile) :
            os.remove(cmtrcfile)
            log.debug("Removing %s" % cmtrcfile)
        # to work with rootd the .rootauthrc file is required
        rootrcfile = os.path.join(homedir, ".rootauthrc")
        if not os.path.exists(rootrcfile) and opts.cmtsite != "standalone" :
            srcrootrcfile = os.path.join(_lbs_home_dir, "LbConfiguration", "data", ".rootauthrc")
            if os.path.exists(srcrootrcfile) :
                try :
                    shutil.copy(srcrootrcfile, rootrcfile)
                    log.debug("Copying %s to %s" % (srcrootrcfile, rootrcfile))
                except IOError :
                    log.warning("Failed to copy %s to %s" % (srcrootrcfile, rootrcfile) )

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
        al = self.Aliases()
        if not opts.remove_userarea :
            newdir = False
            if not opts.userarea :
                opts.userarea = os.path.join(ev["HOME"], "cmtuser") # @todo: use something different for window
            ev["User_release_area"] = opts.userarea
            log.debug("User_release_area is set to %s" % ev["User_release_area"])

            rename_cmtuser = False
            if os.path.exists(opts.userarea) : # is a file, a directory or a valid link
                if os.path.isfile(opts.userarea) : # is a file or a link pointing to a file
                    log.warning("%s is a file"  % opts.userarea)
                    rename_cmtuser = True
                    newdir = True
                else : # is a directory or a link pointing to a directory. Nothing to do
                    log.debug("%s is a directory" % opts.userarea)
            else : # doesn't exist or is an invalid link
                if os.path.islink(opts.userarea) : # broken link
                    log.warning("%s is a broken link"  % opts.userarea)
                    rename_cmtuser = True
                newdir = True
            if rename_cmtuser :
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
                    self.addEcho(" --- a new cmtuser directory has been created in your HOME directory")
                except IOError:
                    log.warning("Can't create %s" % opts.userarea)
            if opts.cmtsite == "CERN" and sys.platform != "win32" and self.hasCommand("fs"):
                if newdir :
                    try :
                        os.system("fs setacl %s system:anyuser l" % opts.userarea)
                        os.system("fs setacl %s cern:z5 rl" % opts.userarea)
                    except IOError:
                        log.warning("Can't change ACL of %s" % opts.userarea)
                    self.addEcho(" --- with LHCb public access (readonly)")
                    self.addEcho(" --- use mkprivate to remove public access to the current directory")
                    self.addEcho(" --- use mkpublic to give public access to the current directory")
                al["mkprivate"] = "find . -type d -print -exec fs setacl {} system:anyuser l \\; ; find . -type d -print -exec fs setacl {} cern:z5 l \\;"
                al["mkpublic"] = "find . -type d -print -exec fs setacl {} system:anyuser l \\; ; find . -type d -print -exec fs setacl {} cern:z5 rl \\;"
        elif ev.has_key("User_release_area") :
            del ev["User_release_area"]
            log.debug("Removed User_release_area from the environment")

    def setSharedArea(self):
        opts = self.options
        if opts.sharedarea :
            if opts.cmtsite == "LOCAL" :
                opts.mysiteroot = os.pathsep.join(opts.sharedarea.split(os.pathsep))

    def getLocalCompilers(self, platform, binary):
        compilers = []
        ev = self.Environment()
        log = logging.getLogger()
        if sys.platform != "win32" :
            if platform == "amd64" :
                platform = "x86_64"
            if platform == "ia32" :
                platform = "i686"
            log.debug("Getting gcc main location")
            for d in multiPathGet(ev["LCG_external_area"], "gcc", alloccurences=True) :
                for v in os.listdir(d) :
                    gccversloc = os.path.join(d, v)
                    for p in os.listdir(gccversloc) :
                        if p.find(os.sep + "%s-%s" % (binary, platform) + os.sep) != -1 :
                            compilers.append(os.path.join(gccversloc, p))
                            log.debug("Found compiler: %s" % os.path.join(gccversloc, p))
        return compilers

    def selectCompiler(self, platform, binary):
        log = logging.getLogger()
        local_compilers = self.getLocalCompilers(platform, binary)
        selected_compilers = []
        for c in local_compilers :
            if platform == "slc5" :
                if c.find(os.sep + "4.3") :
                    selected_compilers.append(c)
        if selected_compilers :
            selected_compilers.sort()
            selected_compilers.reverse()
        if selected_compilers and platform == "slc5" :
            log.debug("Selected gcc 4.3 @ %s" % selected_compilers[0])
        return selected_compilers


    def getWildCardCMTConfig(self, wildcard=None, debug=False):
        """
        returns the best matched CMTCONFIG for the wilcard string
        @param wildcard: text to be look for in the CMTCONFIG
        @type wildcard: string
        @param debug: if the searched list includes also the dbg CMTCONFIG
        @type debug: boolean
        """
        opts = self.options
        log = logging.getLogger()
        theconf = None
        supported_configs = self._nativemachine.CMTSupportedConfig(debug=debug)
        if opts.cmtsite == "CERN" :
            # every platform with a descent python at CERN
            supconf = self._nativemachine.CMTCompatibleConfig(debug=debug)
        else :
            # restriction on supported CONFIG for LOCAL use
            supconf = supported_configs

        if wildcard :
            log.debug("Looking for %s in the list of selected CMTCONFIGs." % wildcard)
            supconf = [ c for c in supconf if wildcard in c ]

        if supconf :
            theconf = supconf[0]
            if theconf not in supported_configs :
                log.warning("%s is not in the list of distributed configurations" % theconf)
                if supported_configs :
                    log.warning("Please switch to a supported one with 'LbLogin -c' before building")
                    log.warning("Supported configs: %s" % ", ".join(supported_configs))

        return theconf

    def setCMTConfig(self, debug=False):
        ev = self.Environment()
        opts = self.options
        log = logging.getLogger()
        self.binary = None
        self.platform = None
        self.compdef = None
        if not opts.wcmtconfig :
            if opts.cmtconfig :
                log.debug("Using provided CMTCONFIG %s" % opts.cmtconfig)
                theconf = opts.cmtconfig
            else :
                log.debug("Guessing CMTCONFIG")
                theconf = self.getWildCardCMTConfig(debug=debug)
                if not theconf :
                    log.debug("Falling back on the native CMTCONFIG")
                    theconf = self._nativemachine.CMTNativeConfig(debug=debug)
        else :
            theconf = self.getWildCardCMTConfig(wildcard=opts.wcmtconfig, debug=True)
            if not theconf :
                if opts.cmtconfig :
                    log.debug("Falling back on the previous CMTCONFIG")
                    theconf = opts.cmtconfig
                else :
                    log.debug("Falling back on the native CMTCONFIG")
                    theconf = self._nativemachine.CMTNativeConfig(debug=debug)

        if theconf :
            if isBinaryDbg(theconf) :
                debug = True
            self.binary = getArchitecture(theconf)
            self.platform = getPlatformType(theconf)
            self.compdef = getCompiler(theconf)
            opts.cmtconfig = theconf


        ev["PYTHON_BINOFFSET"] = os.sep + "bin"

        if self.platform == "win32" :
            ev["PYTHON_BINOFFSET"] = ""

        ev["CMTOPT"] = getBinaryOpt(theconf)
        log.debug("CMTOPT is set to %s" % ev["CMTOPT"])

        ev["CMTDEB"] = getBinaryDbg(theconf)
        log.debug("CMTDEB is set to %s" % ev["CMTDEB"])


        if debug or sys.platform == "win32" :
            ev["CMTCONFIG"] = ev["CMTDEB"]
            log.debug("CMTDEB is set to %s" % ev["CMTDEB"])
        else :
            ev["CMTCONFIG"] = ev["CMTOPT"]
        log.debug("CMTCONFIG is set to %s" % ev["CMTCONFIG"])

    def setLCGhostos(self):
        '''
        Set the environment variable LCG_hostos, used by the 'lcg-' compiler wrappers.
        '''
        ev = self.Environment()
        nm = self._nativemachine
        # we take only the first two elements of the native CMTCONFIG, e.g.
        #  x86_64-slc5-gcc46-opt -> x86_64-slc5
        ev['LCG_hostos'] = '-'.join(nm.CMTNativeConfig().split('-')[:2])

    def setCMTPath(self):
        ev = self.Environment()
        opts = self.options
        log = logging.getLogger()

        self.setHomeDir()

        use_project_path = False

        if ev.has_key("CMTPROJECTPATH") :
            use_project_path = True
        elif opts.cmtvers.find("v1r20") != -1 :
            use_project_path = True

        if opts.cmtsite != "standalone" :
            if use_project_path :
                if ev.has_key("CMTPATH") :
                    del ev["CMTPATH"]
                if not opts.remove_userarea and ev.has_key("User_release_area") :
                    ev["CMTPROJECTPATH"] = os.pathsep.join([ev["User_release_area"], ev["LHCBPROJECTPATH"]])
                else :
                    ev["CMTPROJECTPATH"] = ev["LHCBPROJECTPATH"]
                log.debug("CMTPROJECTPATH is set to %s" % ev["CMTPROJECTPATH"])
            else :
                if ev.has_key("CMTPROJECTPATH") :
                    del ev["CMTPROJECTPATH"]
                if not opts.remove_userarea and ev.has_key("User_release_area"):
                    ev["CMTPATH"] = ev["User_release_area"]
                    log.debug("CMTPATH is set to %s" % ev["CMTPATH"])

    def setExtraTags(self):
        """
        setup the canonical CMTEXTRATAGS environment variable that has to be used
        by "SetupProject LbScripts". By default and unless specified on the command line
        only "NO_PYTHON_LIBPATH" is passed.
        """
        opts = self.options
        log  = logging.getLogger()
        if opts.use_cmtextratags :
            if "CMTEXTRATAGS" in os.environ.keys() :
                extra_args_list = os.environ["CMTEXTRATAGS"].replace(",", " ").split()
                extra_args_list.append("NO_PYTHON_LIBPATH")
                # according to the documentation tags are space separated.
                # but "," do work as well.
                os.environ["CMTEXTRATAGS"] = " ".join(extra_args_list)
            else :
                os.environ["CMTEXTRATAGS"] = "NO_PYTHON_LIBPATH"
        else :
            os.environ["CMTEXTRATAGS"] = "NO_PYTHON_LIBPATH"

        log.debug("CMTEXTRATAGS is set to %s" % os.environ.get("CMTEXTRATAGS", None))

    def setupCompat(self):
        """ preset the compat entries before the call to SetupProject """
        log = logging.getLogger()
        ev = self.Environment()
        opts = self.options
        log.debug("Trying to prepend the Compat project")

        if ev.has_key("LHCBRELEASES") :

            compat_dir = multiPathGetFirst(ev["LHCBRELEASES"], "COMPAT")

            if compat_dir :
                lastver = None
                if (not opts.compat_version) or opts.compat_version == "v*" :
                    compat_lst = [ x for x in os.listdir(compat_dir) if x.startswith("COMPAT_") ]
                    if compat_lst :
                        lastver = sortStrings(compat_lst, safe=True)[-1]
                else :
                    lastver = "COMPAT_%s" % opts.compat_version
                if lastver :
                    compat_rel = os.path.join(compat_dir, lastver)
                    compat_lib = os.path.join(compat_rel, "CompatSys", ev["CMTOPT"], "lib")
                    if sys.platform != "win32" :
                        compat_bin = os.path.join(compat_rel, "CompatSys", ev["CMTOPT"], "bin")
                        envPathPrepend("PATH", compat_bin)
                        envPathPrepend("LD_LIBRARY_PATH", compat_lib)
                        log.debug("Internal %s is set to %s" % ("LD_LIBRARY_PATH", os.environ["LD_LIBRARY_PATH"]))
                    else :
                        envPathPrepend("PATH", compat_lib)
                    log.debug("Internal %s is set to %s" % ("PATH", os.environ["PATH"]))


    def setupLbScripts(self):
        """ Call to SetupProject with LbScripts and python """
        log = logging.getLogger()
        opts = self.options
        ev = self.Environment()
        log.debug("Setting up LbScripts and appending to the output")
        for var in ev.keys() :
            os.environ[var] = ev[var]

        log.debug("%s is set to %s" % ("PATH", ev.get("PATH", "")))
        if sys.platform != "win32" :
            log.debug("%s is set to %s" % ("LD_LIBRARY_PATH", ev.get("LD_LIBRARY_PATH", "")))


        setupprojargs = []
        # needed for the deployment: otherwise the cache is not generated
        setupprojargs.append("--ignore-not-ready")
        if opts.log_level == "DEBUG" :
            setupprojargs.append("--debug")
        if opts.log_level == "CRITICAL" :
            setupprojargs.append("--silent")
        if not opts.user_area_scripts :
            setupprojargs.append("--no-user-area")
        if opts.usedevarea :
            setupprojargs.append("--dev")
        setupprojargs.append("--disable-CASTOR")
        setupprojargs.append("--no-touch-logfile")
        if self.output_name :
            setupprojargs.append("--append=%s" % self.output_name)
        setupprojargs.append("--shell=%s" % self.targetShell())
        setupprojargs.append("LbScripts")
        if opts.scriptsvers :
            setupprojargs.append(opts.scriptsvers)
        if opts.get_python :
            setupprojargs.append("--runtime-project")
            setupprojargs.append("LCGCMT")
            if ev["CMTCONFIG"].startswith("win32_vc71") :
                setupprojargs.append("5[0-8]*")
            setupprojargs.append("Python")
            if opts.pythonvers :
                setupprojargs.append("-v")
                setupprojargs.append(opts.pythonvers)
        if not opts.no_compat :
            setupprojargs.append("--runtime-project")
            setupprojargs.append("COMPAT")
            setupprojargs.append("--use")
            setupprojargs.append("CompatSys %s" % opts.compat_version)


        log.debug("Arguments to SetupProject: %s" % " ".join(setupprojargs))
#            self.setExtraTags()


        if opts.compat_prepend is None :
            try :
                SetupProject().main(setupprojargs)
            except ImportError:
                log.debug("SetupProject failed. Retrying with Compat prepended")
                self.setupCompat()
                SetupProject().main(setupprojargs)
        else :
            if opts.compat_prepend :
                self.setupCompat()
            SetupProject().main(setupprojargs)

        log.debug("%s is set to %s" % ("PATH", ev.get("PATH", "")))
        if sys.platform != "win32" :
            log.debug("%s is set to %s" % ("LD_LIBRARY_PATH", ev.get("LD_LIBRARY_PATH", "")))

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

        self.setSharedArea()

        self.setCMTConfig(debug)
        self.setCMTPath()
        self.setupCompat()

        # this is use internally by the 'lcg-' compiler wrapper.
        self.setLCGhostos()

        # return a copy otherwise the environment gets restored
        # at the destruction of the instance
        return self.copyEnv()

    def manifest(self, debug=False):
        ev = self.Environment()
        opts = self.options
        if opts.log_level != "CRITICAL" :
            self.addEcho("*" * 80)
            if opts.scriptsvers :
                self.addEcho("*" + ("---- LHCb Login %s ----" % opts.scriptsvers).center(78) + "*")
            else :
                self.addEcho("*" + "---- LHCb Login ----".center(78) + "*")
            if self.binary :
                self.addEcho("*" + ("Building with %s on %s %s system (%s)" % (self.compdef, self.platform, self.binary, ev["CMTCONFIG"])).center(78) + "*")
            else : # for windows
                self.addEcho("*" + ("Building with %s on %s system (%s)" % (self.compdef, self.platform, ev["CMTCONFIG"])).center(78) + "*")
            self.addEcho("*" * 80)
            if ev.has_key("CMTPATH") :
                self.addEcho(" --- CMTPATH is set to %s" % ev["CMTPATH"])
            else :
                if ev.has_key("User_release_area") :
                    self.addEcho(" --- User_release_area is set to %s" % ev["User_release_area"])
                if ev.has_key("LHCBPROJECTPATH") :
                    self.addEcho(" --- LHCBPROJECTPATH is set to:")
                    for p in ev["LHCBPROJECTPATH"].split(os.pathsep) :
                        if p :
                            self.addEcho("    %s" % p)


            self.addEcho("-" * 80)


    def main(self):
        debug = False
        for a in self.args :
            if a == "debug" :
                debug = True

        self.setEnv(debug)
        self.manifest(debug)

        self.flush()

        self.setupLbScripts()

        return 0


if __name__ == '__main__':
    sys.exit(LbLoginScript(usage="%prog [options] [debug]").run())

