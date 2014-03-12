from distutils.core import setup
from distutils.command.install import install as _install

import os


def get_data_files(input_dir, output_dir):
    result = []
    for root, dirs, files in os.walk(input_dir) :
        da_files = []
        for f in files :
            da_files.append(os.path.join(root,f))
        result.append((os.sep.join([output_dir]+root.split(os.sep)[1:]),da_files))
    return result

these_files = get_data_files("data/cmake", "EuclidEnv")
these_files += get_data_files("data/texmf", "EuclidEnv")

setup (name="euclidenv",
       version="1.0",
       description="Euclid Environment Scripts",
       author="Hubert Degaudenzi",
       author_email="Hubert.Degaudenzi@unige.ch",
       url="http://www.isdc.unige.ch/redmine/projects/euclidenv",
       py_modules = ["Euclid.ConfigFile","Euclid.Env", "Euclid.Log",
                     "Euclid.Login", "Euclid.Option", "Euclid.Path",
                     "Euclid.PathStripper", "Euclid.Platform",
                     "Euclid.Script", "Euclid.Version"],
       package_dir={"": "python"},
       ext_package= "Euclid",
       scripts  = [ os.path.join("scripts","ELogin.sh"),
                    os.path.join("scripts","ELogin.csh"),
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
                    os.path.join("scripts", "FixInstallPath"),
                  ],
       data_files = [("/etc/profile.d", [os.path.join("data", "profile", "euclid.sh"),
                                         os.path.join("data", "profile", "euclid.csh")]),
                     ("/etc/sysconfig", [os.path.join("data", "sys", "config", "euclid")])
                     ] + these_files,

#       options = {'bdist_rpm':{'post_install' : 'post_install',
#                               'pre_uninstall' : 'pre_uninstall'}},
       )
