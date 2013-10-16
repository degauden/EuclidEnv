from distutils.core import setup
from distutils.command.install import install as _install

import os


setup (name="euclidenv",
       version="0.1",
       description="Euclid Environment Scripts",
       author="Hubert Degaudenzi",
       author_email="Hubert.Degaudenzi@unige.ch",
       url="http://www.isdc.unige.ch/redmine/projects/euclidenv",
       py_modules = [ "Euclid.Env"],
       package_dir={"": "python"},
       ext_package= "Euclid",
       scripts  = [ os.path.join("scripts","ELogin.sh"),
                    os.path.join("scripts","ELogin.csh")],
       data_files = [("/etc/profile.d", [os.path.join("data", "profile", "euclid.sh")]),
                     ("/etc/profile.d", [os.path.join("data", "profile", "euclid.csh")]),
                     ("/etc/sysconfig", [os.path.join("data", "sys", "config", "euclid")]),
                     ("/opt/Euclid/env", [os.path.join("data", "env", "group_login.sh")]),
                     ("/opt/Euclid/env", [os.path.join("data", "env", "group_login.csh")]),
                     ("/opt/Euclid/env", [os.path.join("data", "env", "group_login.bat")]),
                     ("/opt/Euclid/env", [os.path.join("data", "env", "group_setup.sh")]),
                     ("/opt/Euclid/env", [os.path.join("data", "env", "group_setup.csh")]),
                     ("/opt/Euclid/env", [os.path.join("data", "env", "group_setup.bat")])

                     ],

#       options = {'bdist_rpm':{'post_install' : 'post_install',
#                               'pre_uninstall' : 'pre_uninstall'}},
       )
