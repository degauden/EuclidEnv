# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name:           EuclidEnv
Version:        1.14.1
Release:        1%{?dist}
Summary:        Euclid Environment Login and Utilities

License:        Public Domain
Source:         %{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
Prefix:         /usr
Prefix:         /etc
Prefix:         /opt/euclid

%description
This package include the scripts to for setting up the run-time and
development environment. This involves the main ELogin script.


%prep
%setup -q


%build
# Remove CFLAGS=... for noarch packages (unneeded)
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --skip-install-fix --root $RPM_BUILD_ROOT


%files
%doc
# For noarch packages: sitelib
%{python_sitelib}/*
%{_bindir}/*
%{_sysconfdir}/profile.d/euclid.csh
%{_sysconfdir}/profile.d/euclid.sh
%{_sysconfdir}/sysconfig/euclid
%{_datadir}/EuclidEnv/cmake/*
%{_datadir}/EuclidEnv/texmf/*


%post
python_loc=$(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(prefix='$RPM_INSTALL_PREFIX0'))")
${RPM_INSTALL_PREFIX0}/bin/FixInstallPath $RPM_INSTALL_PREFIX0 $RPM_INSTALL_PREFIX0/bin/ELogin.{,c}sh
${RPM_INSTALL_PREFIX0}/bin/FixInstallPath $RPM_INSTALL_PREFIX0 $RPM_INSTALL_PREFIX0/bin/Euclid_group_{login,setup}.{,c}sh
${RPM_INSTALL_PREFIX0}/bin/FixInstallPath $RPM_INSTALL_PREFIX0 $RPM_INSTALL_PREFIX0/bin/Euclid_config.{,c}sh
${RPM_INSTALL_PREFIX0}/bin/FixInstallPath $RPM_INSTALL_PREFIX0 $RPM_INSTALL_PREFIX1/profile.d/euclid.{,c}sh
${RPM_INSTALL_PREFIX0}/bin/FixInstallPath $RPM_INSTALL_PREFIX0 $python_loc/Euclid/Login.py
${RPM_INSTALL_PREFIX0}/bin/FixInstallPath -n this_install_version %{version} $python_loc/Euclid/Login.py
${RPM_INSTALL_PREFIX0}/bin/FixInstallPath -n this_euclid_base $RPM_INSTALL_PREFIX2 $RPM_INSTALL_PREFIX1/sysconfig/euclid
${RPM_INSTALL_PREFIX0}/bin/FixInstallPath -n this_euclid_base $RPM_INSTALL_PREFIX2 $RPM_INSTALL_PREFIX0/bin/Euclid_config.{,c}sh
${RPM_INSTALL_PREFIX0}/bin/FixInstallPath -n this_euclid_base $RPM_INSTALL_PREFIX2 $python_loc/Euclid/Login.py
if [[ ! -f "${python_loc}/Euclid/__init__.py" ]]; then
cat << EOF > ${python_loc}/Euclid/__init__.py
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)  # @ReservedAssignment
EOF
fi


%changelog
* Fri Dec 4 2015 Hubert Degaudenzi <Hubert.Degaudenzi@unige.ch> 1.14.1-1
- Emergency fir for the usage of EUCLID_BASE env variable in ELogin
- add a generic lx type in the BINARY_TAG. This corresponds
  to an unkown linux box.

* Fri Nov 27 2015 Hubert Degaudenzi <Hubert.Degaudenzi@unige.ch> 1.14-1
- update to the cmake library of Elements 3.9
- fix the cleaning of the ELogin banner
- fix the setup of the environment for bash. Now it is not repeated for 
  every subshell.
- add the new "python setup.py test" command. It is based on a generated
  py.test script.

* Tue Oct 13 2015 Hubert Degaudenzi <Hubert.Degaudenzi@unige.ch> 1.13.1-1
- Bugfix. The E-Run command was not checking the existence of the
  directory of a project before trying to list its version subdirectories.

* Wed Oct 7 2015 Hubert Degaudenzi <Hubert.Degaudenzi@unige.ch> 1.13-1
- update to the cmake library of Elements 3.8 
- introduction of the draft generation of the python SWIG bindings

* Tue Sep 22 2015 Hubert Degaudenzi <Hubert.Degaudenzi@unige.ch> 1.12.3-1
- update to the cmake library of the Elements 3.7.3 version
- critical bug fix to locate Elements in the release area (/opt/euclid)

* Tue Aug 18 2015 Hubert Degaudenzi <Hubert.Degaudenzi@unige.ch> 1.12.2-1
- update to the cmake library of the Elements 3.7.2 version
- fix a bug in the toolchain crawling of projects

* Wed Aug 5 2015 Hubert Degaudenzi <Hubert.Degaudenzi@unige.ch> 1.12.1-1
- update to the cmake library of the Elements 3.7.1 version
- fix of the conversion of the CMAKE_PROJECT_PATH environment variable 
  into a cmake list

* Mon Aug 3 2015 Hubert Degaudenzi <Hubert.Degaudenzi@unige.ch> 1.12-1
- update the cmake library to the Elements 3.7 version
- fix the E-Run command to work with the User_area without version
  directory.

* Mon Jun 15 2015 Hubert Degaudenzi <Hubert.Degaudenzi@unige.ch> 1.11-1
- update the cmake library to the Elements 3.6 version.
- contains the CMake Bootstrap Toolchain.

* Thu Feb 26 2015 Hubert Degaudenzi <Hubert.Degaudenzi@unige.ch> 1.10-1
- update the cmake library to the Elements 3.5 version.
- fixes for the MacPort warnings.

* Mon Feb 2 2015 Hubert Degaudenzi <Hubert.Degaudenzi@unige.ch> 1.9-1
- update the cmake library to the Elements 3.4 version.
- various fixes for the Darwin platform.
- new version of the latex class with the new Euclid logo.

* Fri Nov 7 2014 Hubert Degaudenzi <Hubert.Degaudenzi@unige.ch> 1.8-1
- updated the cmake library to the Elements 3.3 version.

* Mon Oct 13 2014 Hubert Degaudenzi <Hubert.Degaudenzi@unige.ch> 1.7-1
- updated to the Elements 3.2 cmake library.
- fixed the version extraction from the SVN tags.

* Mon Oct 6 2014 Hubert Degaudenzi <Hubert.Degaudenzi@unige.ch> 1.6-1
- imported the cmake library from Elements 3.1
- fixed the User_area location default from ~/Work to ~/Work/Projects.

* Thu Aug 28 2014 Hubert Degaudenzi <Hubert.Degaudenzi@unige.ch> 1.5-1
- Release of version 1.5
- adapted from Elements 3.0
- mostly a removal of the win32 part

* Mon Jul 14 2014 Hubert Degaudenzi <Hubert.Degaudenzi@unige.ch> 1.4-1
- Release of version 1.4
- Fix the default BINARY_TAG and set it to the RelWithDebugInfo type.
- Cure the logic for the full setup of the ELogin wrapper. It is done if
  the shell is either a login one or non-interactive.
- Add the "--implicit-latest" option to E-Run.
