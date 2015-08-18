from distutils.core import setup
from distutils.command.install import install as _install

import os
import sys
from subprocess import call

__version__ = "1.12.2"


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

these_files = get_data_files("data/cmake", "EuclidEnv")
these_files += get_data_files("data/texmf", "EuclidEnv")


use_local_install = False
for a in sys.argv:
    for b in ["--user", "--prefix", "--home"]:
        if a.startswith(b):
            use_local_install = True

if use_local_install:
    etc_files = [("../etc/profile.d", [os.path.join("data", "profile", "euclid.sh"),
                                       os.path.join("data", "profile", "euclid.csh")]),
                 ("../etc/sysconfig",
                  [os.path.join("data", "sys", "config", "euclid")])
                 ]
else:
    etc_files = [("../../etc/profile.d", [os.path.join("data", "profile", "euclid.sh"),
                                          os.path.join("data", "profile", "euclid.csh")]),
                 ("../../etc/sysconfig",
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


class my_install(_install):

    def get_login_scripts(self):
        p_list = []
        for c in ["ELogin", "Euclid_group_login", "Euclid_group_setup", "Euclid_config"]:
            for s in ["sh", "csh"]:
                file2fix = os.path.join(self.install_scripts, "%s.%s" % (c, s))
                if os.path.exists(file2fix):
                    p_list.append(file2fix)
        return p_list

    def get_profile_scripts(self):
        p_list = []
        for s in ["sh", "csh"]:
            file2fix = os.path.join(
                self.install_base, "etc", "profile.d",  "%s.%s" % ("euclid", s))
            if os.path.exists(file2fix):
                p_list.append(file2fix)
        return p_list

    def fix_install_path(self):
        fixscript = os.path.join(self.install_scripts, "FixInstallPath")
        proc_list = self.get_login_scripts()
        file2fix = os.path.join(self.install_lib, "Euclid", "Login.py")
        if os.path.exists(file2fix):
            proc_list.append(file2fix)
        if use_local_install:
            proc_list += self.get_profile_scripts()

        for p in proc_list:
            print "Fixing %s with the %s prefix path" % (p, self.install_base)
            call(["python", fixscript, self.install_base, p])

        if os.path.exists(file2fix):
            print "Fixing %s with the %s version" % (file2fix, __version__)
            call(
                ["python", fixscript, "-n", "this_install_version", __version__, file2fix])

    def create_extended_init(self):
        init_file = os.path.join(self.install_lib, "Euclid", "__init__.py")

        if not os.path.exists(init_file):
            print "Creating the %s file" % init_file
            init_content = """# This is the initial setup for the Euclid namespace package
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)  # @ReservedAssignment

"""
            open(init_file, "w").write(init_content)

    def custom_post_install(self):
        self.fix_install_path()
        self.create_extended_init()

    def run(self):
        _install.run(self)
        # postinstall
        if not skip_custom_postinstall:
            # print "This is the install base %s" % self.install_base
            # print "This is the install platbase %s" % self.install_platbase
            # print "This is the install root %s" % self.root
            # print "This is the install purelib %s" % self.install_purelib
            # print "This is the install platlib %s" % self.install_platlib
            # print "This is the install lib %s" % self.install_lib
            # print "This is the install headers %s" % self.install_headers
            # print "This is the install scripts %s" % self.install_scripts
            # print "This is the install data %s" % self.install_data
            self.custom_post_install()

setup(name="EuclidEnv",
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
               ],
      data_files=etc_files + these_files,
      cmdclass={"install": my_install},
      )
