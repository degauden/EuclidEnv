# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name:           EuclidEnv
Version:        1.2.1
Release:        1%{?dist}
Summary:        Euclid Environment Login and Utilities

License:        Public Domain
Source:         %{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
Prefix:         /usr
Prefix:         /etc

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
${RPM_INSTALL_PREFIX0}/bin/FixInstallPath $RPM_INSTALL_PREFIX0 $RPM_INSTALL_PREFIX1/profile.d/euclid.{,c}sh  
${RPM_INSTALL_PREFIX0}/bin/FixInstallPath $RPM_INSTALL_PREFIX0 $python_loc/Euclid/Login.py  


%changelog
