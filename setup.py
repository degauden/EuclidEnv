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
                    os.path.join("scripts","ELogin.csh"),
                    os.path.join("scripts", "Euclid_group_login.sh"),
                    os.path.join("scripts", "Euclid_group_login.csh"),
                    os.path.join("scripts", "Euclid_group_login.bat"),
                    os.path.join("scripts", "Euclid_group_setup.sh"),
                    os.path.join("scripts", "Euclid_group_setup.csh"),
                    os.path.join("scripts", "Euclid_group_setup.bat")
                  ],
       data_files = [("/etc/profile.d", [os.path.join("data", "profile", "euclid.sh")]),
                     ("/etc/profile.d", [os.path.join("data", "profile", "euclid.csh")]),
                     ("/etc/sysconfig", [os.path.join("data", "sys", "config", "euclid")])
                     ],

#       options = {'bdist_rpm':{'post_install' : 'post_install',
#                               'pre_uninstall' : 'pre_uninstall'}},
       )
