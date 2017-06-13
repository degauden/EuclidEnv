#!/usr/bin/env python
# Commit Id: $Format:%H$
# Author:    $Format:%an$
# Date  :    $Format:%ad$


from distutils.core import setup, Command
from distutils.command.install import install as _install
from distutils.command.sdist import sdist as _sdist
from distutils.command.bdist_rpm import bdist_rpm as _bdist_rpm
from distutils.command.build import build as _build


import os
import sys
from subprocess import call, check_output
from glob import glob


from string import Template

__version__ = "3.1"
__project__ = "EuclidEnv"


def get_data_files(input_dir, output_dir):
    result = []
    for root, dirs, files in os.walk(input_dir):
        da_files = []
        for f in files:
            da_files.append(os.path.join(root, f))
#             splf = os.path.splitext(f)
#             if splf[1] == ".py":
#                 pass
#                 da_files.append(os.path.join(root, splf[0] + ".pyo"))
#                 da_files.append(os.path.join(root, splf[0] + ".pyc"))
        result.append(
            (os.sep.join([output_dir] + root.split(os.sep)[1:]), da_files))
    return result

these_files = get_data_files("data/cmake", __project__)
these_files += get_data_files("data/texmf", __project__)


# Please note the that the local install is
# also needed for --prefix. Take as example the
# /usr/local prefix.
use_local_install = False
for a in sys.argv:
    for b in ["--user", "--prefix", "--home"]:
        if a.startswith(b):
            use_local_install = True


etc_install_root = None
install_root = None
for a in sys.argv:
    if a.startswith("--etc-root"):
        # TODO implement the extratction of the value from
        # the option
        e_base = a.split("=")[1:]
        if len(e_base) == 1:
            etc_install_root = e_base[0]
        sys.argv.remove(a)
    if a.startswith("--root"):
        # TODO implement the extraction of the value from
        # the option
        r_base = a.split("=")[1:]
        if len(r_base) == 1:
            install_root = r_base[0]


if not etc_install_root:
    if use_local_install:
        etc_install_prefix = "../etc"
    else:
        etc_install_prefix = "../../etc"
else:
    etc_install_prefix = os.path.join(etc_install_root, "etc")


etc_files = [(os.path.join(etc_install_prefix, "profile.d"), [os.path.join("data", "profile", "euclid.sh"),
                                       os.path.join("data", "profile", "euclid.csh")]),
             (os.path.join(etc_install_prefix, "sysconfig"),
                  [os.path.join("data", "sys", "config", "euclid")])
            ]


use_custom_install_root = False
for a in sys.argv:
    if a.startswith("--root"):
        # use custom install root. Possibly creating a
        # RPM. This will prevent the post install treatment.
        use_custom_install_root = True


skip_install_fix = False


# disable the postinstall script if needed. This is especially needed for the RPM
# creation. In that case the postinstall is done by the RPM spec file.
# This option is obsolete: rather use --skip-custom-postinstall
for a in sys.argv:
    if a.startswith("--skip-install-fix"):
        skip_install_fix = True
        sys.argv.remove(a)

skip_custom_postinstall = skip_install_fix
for a in sys.argv:
    if a.startswith("--skip-custom-postinstall"):
        skip_custom_postinstall = True
        sys.argv.remove(a)

this_euclid_base = "/opt/euclid"
for a in sys.argv:
    if a.startswith("--euclid-base"):
        # TODO implement the extratction of the value from
        # the option
        e_base = a.split("=")[1:]
        if len(e_base) == 1:
            this_euclid_base = e_base[0]
        sys.argv.remove(a)


def getRMD160Digest(filepath):
    return check_output(["openssl", "dgst", "-rmd160", filepath]).split()[-1]


def getSHA256Digest(filepath):
    return check_output(["openssl", "dgst", "-sha256", filepath]).split()[-1]


class my_build(_build):
    def run(self):
        _build.run(self)


class my_sdist(_sdist):

    @staticmethod
    def _get_template_target(filename):
        fname, fext = os.path.splitext(os.path.basename(filename))
        if fext == ".in":
            return os.path.join("dist", fname)
        else:
            print("Error: the %s file has not the '.in' extension" % filename)
            sys.exit(1)

    @staticmethod
    def _get_sdist_filepath():
        return os.path.join("dist", "%s-%s.tar.gz" % (__project__, __version__))

    @staticmethod
    def _get_changelog_filepath():
        return "ChangeLog"

    def expand_template_file(self, filename):
        out_fname = self._get_template_target(filename)
        print("Generating %s from the %s template" % (out_fname, filename))
        rmd160_digest = getRMD160Digest(self._get_sdist_filepath())
        sha256_digest = getSHA256Digest(self._get_sdist_filepath())
        changelog_content = open(self._get_changelog_filepath()).read()
        with open(filename) as in_f:
            src = Template(in_f.read()).substitute(
                version=__version__, project=__project__,
                rmd160=rmd160_digest, sha256=sha256_digest,
                changelog=changelog_content)
        with open(out_fname, "w") as out_f:
            out_f.write(src)

    def expand_templates(self):
        flist = []
        flist.append(os.path.join("data", "RPM", "%s.spec.in" % __project__))
        flist.append(os.path.join("data", "Ports", "Portfile.in"))
        for f in flist:
            if os.path.exists(f):
                self.expand_template_file(f)

    def run(self):
        _sdist.run(self)
        self.expand_templates()


class my_bdist_rpm(_bdist_rpm):

    @staticmethod
    def run():
        print("Cannot run directly the bdist_rpm target. Please rather use the generated " \
               "spec file (together with the sdist target) in the dist sub-directory")
        sys.exit(1)


class my_install(_install):

    def initialize_options(self):

        _install.initialize_options(self)

        parent_dir = os.path.dirname(__file__)

        dist_dir = os.path.join(parent_dir, "dist")

        if not os.path.exists(dist_dir):
            os.mkdir(dist_dir)

        self.record = os.path.join(dist_dir, "installed_files.txt")

    def get_login_scripts(self):
        p_list = []
        for c in ["ELogin", "Euclid_group_login", "Euclid_group_setup"]:
            for s in ["sh", "csh"]:
                file2fix = os.path.join(self.install_scripts, "%s.%s" % (c, s))
                if os.path.exists(file2fix):
                    p_list.append(file2fix)
        return p_list

    def get_profile_scripts(self):
        p_list = []
        this_install = self.get_etc_install_root()
        for s in ["sh", "csh"]:
            file2fix = os.path.join(
                this_install, "etc", "profile.d", "%s.%s" % ("euclid", s))
            if os.path.exists(file2fix):
                p_list.append(file2fix)
        return p_list

    def get_etc_install_root(self):
        if etc_install_root:
            this_install = etc_install_root
        else:
            if use_local_install:
                this_install = os.path.dirname(self.install_scripts)
            else:
                this_install = os.path.dirname(os.path.dirname(self.install_scripts))

        return this_install


    def fix_etc_install_path(self):
        fixscript = os.path.join(self.install_scripts, "FixInstallPath")
        proc_list = self.get_config_scripts()
        this_install = os.path.join(self.get_etc_install_root(), "etc")
        for p in proc_list:
            print("Fixing %s with the %s prefix path" % (p, this_install))
            call(["python", fixscript, "-n", "this_etc_install_prefix", this_install, p])


    def fix_install_path(self):
        fixscript = os.path.join(self.install_scripts, "FixInstallPath")
        proc_list = self.get_login_scripts() + self.get_config_scripts()
        file2fix = os.path.join(self.install_lib, "Euclid", "Login.py")
        if os.path.exists(file2fix):
            proc_list.append(file2fix)
        proc_list += self.get_profile_scripts()
        for p in proc_list:
            print("Fixing %s with the %s prefix path" % (p, os.path.dirname(self.install_scripts)))
            call(["python", fixscript, os.path.dirname(self.install_scripts), p])
        self.fix_etc_install_path()

    def fix_version(self):
        fixscript = os.path.join(self.install_scripts, "FixInstallPath")
        file2fix = os.path.join(self.install_lib, "Euclid", "Login.py")
        if os.path.exists(file2fix):
            print("Fixing %s with the %s version" % (file2fix, __version__))
            call(
                ["python", fixscript, "-n", "this_install_version", __version__, file2fix])

    def get_sysconfig_files(self):
        p_list = []

        this_install = self.get_etc_install_root()

        file2fix = os.path.join(this_install, "etc", "sysconfig", "euclid")
        if os.path.exists(file2fix):
            p_list.append(file2fix)
        return p_list

    def get_config_scripts(self):
        p_list = []
        for s in ["sh", "csh"]:
            file2fix = os.path.join(
                self.install_scripts, "%s.%s" % ("Euclid_config", s))
            if os.path.exists(file2fix):
                p_list.append(file2fix)
        return p_list

    def fix_euclid_base(self):
        fixscript = os.path.join(self.install_scripts, "FixInstallPath")
        proc_list = self.get_sysconfig_files()
        proc_list += self.get_config_scripts()
        file2fix = os.path.join(self.install_lib, "Euclid", "Login.py")
        if os.path.exists(file2fix):
            proc_list.append(file2fix)
        for p in proc_list:
            print("Fixing %s with the %s euclid base" % (p, this_euclid_base))
            call(
                ["python", fixscript, "-n", "this_euclid_base", this_euclid_base, p])

    def create_extended_init(self):
        init_file = os.path.join(self.install_lib, "Euclid", "__init__.py")

        if not os.path.exists(init_file):
            print("Creating the %s file" % init_file)
            init_content = """# This is the initial setup for the Euclid namespace package
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)  # @ReservedAssignment

"""
            open(init_file, "w").write(init_content)

    def custom_post_install(self):
        self.fix_install_path()
        self.fix_version()
        self.fix_euclid_base()
        self.create_extended_init()

    def run(self):
        _install.run(self)
        # postinstall
        if not skip_custom_postinstall:
#             print "This is the prefix %s" % self.prefix
#             print "This is the install base %s" % self.install_base
#             print "This is the install platbase %s" % self.install_platbase
#             print "This is the install root %s" % self.root
#             print "This is the install purelib %s" % self.install_purelib
#             print "This is the install platlib %s" % self.install_platlib
#             print "This is the install lib %s" % self.install_lib
#             print "This is the install headers %s" % self.install_headers
#             print "This is the install scripts %s" % self.install_scripts
#             print "This is the install data %s" % self.install_data
            self.custom_post_install()

class PyTest(Command):
    user_options = []
    runtests_filename = "runtests.py"

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    @staticmethod
    def _get_python_path():
        parent_dir = os.path.dirname(__file__)
        return os.path.join(parent_dir, "python")

    @staticmethod
    def _get_tests_files():
        parent_dir = os.path.dirname(__file__)
        return glob(os.path.join(parent_dir, "tests", "*Test.py"))

    def _generate_runtests_file(self):
        import subprocess
        errno = subprocess.call(["py.test", "--genscript=%s" % self.runtests_filename])
        print("%s generated. Please consider to add it to your sources" % self.runtests_filename)
        if errno != 0:
            raise SystemExit(errno)


    def run(self):
        import subprocess
        import sys
        if not os.path.exists(os.path.join(os.getcwd(), self.runtests_filename)) :
            self._generate_runtests_file()

        sys.path.insert(0, self._get_python_path())
        os.environ["PYTHONPATH"] = os.pathsep.join(sys.path)
        errno = subprocess.call([sys.executable, 'runtests.py'] + self._get_tests_files())
        raise SystemExit(errno)

class Purge(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    @staticmethod
    def run():

        import shutil

        parent_dir = os.path.dirname(__file__)

        for d in ["build", "dist"]:
            full_d = os.path.join(parent_dir, d)
            if os.path.exists(full_d):
                print("Removing the %s directory" % full_d)
                shutil.rmtree(full_d)


class Uninstall(Command):

    description = 'Uninstallation of recorded files'
    user_options = [
            ('root=', None, 'path to the root install location'),
        ]

    def initialize_options(self):
        self.root = None

    def finalize_options(self):
        if self.root:
            assert os.path.exists(self.root), "The %s root installation directory doesn't exist" % self.root

    def run(self):

        import shutil
        parent_dir = os.path.dirname(__file__)
        record = os.path.join(parent_dir, "dist", "installed_files.txt")
        with open(record) as rf:
            for l in rf:
                f = l.strip()
                if self.root:
                    if f.startswith("/"):
                        f = f[1:]
                    f = os.path.join(self.root, f)
                if os.path.exists(f):
                    if os.path.isdir(f):
                        print("Removing the %s directory" % f)
                        shutil.rmtree(f)
                    else:
                        print("Removing the %s file" % f)
                        os.remove(f)


setup(name=__project__,
      version=__version__,
      description="Euclid Environment Scripts",
      author="Hubert Degaudenzi",
      author_email="Hubert.Degaudenzi@unige.ch",
      url="http://www.isdc.unige.ch/redmine/projects/euclidenv",
      package_dir={"": "python"},
      packages=["Euclid", "Euclid.Run"],
      scripts=[os.path.join("scripts", "ELogin.sh"),
               os.path.join("scripts", "ELogin.csh"),
               os.path.join("scripts", "Euclid_config.sh"),
               os.path.join("scripts", "Euclid_config.csh"),
               os.path.join("scripts", "Euclid_group_login.sh"),
               os.path.join("scripts", "Euclid_group_login.csh"),
               os.path.join("scripts", "Euclid_group_setup.sh"),
               os.path.join("scripts", "Euclid_group_setup.csh"),
               os.path.join("scripts", "runpy"),
               os.path.join("scripts", "StripPath.csh"),
               os.path.join("scripts", "StripPath.sh"),
               os.path.join("scripts", "WhereAmI"),
               os.path.join("scripts", "E-Run"),
               os.path.join("scripts", "eclipse_pythonpath_fix"),
               os.path.join("scripts", "FixInstallPath"),
               os.path.join("scripts", "ERun_autocompletion.sh"),
               ],
      data_files=etc_files + these_files,
      cmdclass={"install": my_install,
                "build": my_build,
                "sdist": my_sdist,
                "bdist_rpm": my_bdist_rpm,
                "test": PyTest,
                "purge": Purge,
                "uninstall": Uninstall,
                },
      )
