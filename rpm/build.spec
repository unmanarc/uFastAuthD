%define name uFastAuthD
%define version 1.3.1
%define build_timestamp %{lua: print(os.date("%Y%m%d"))}
Name:           %{name}
Version:        %{version}
Release:        %{build_timestamp}.git%{?dist}
Summary:        Unmanarc Fast Authentication Daemon
License:        GPLv3
URL:            https://github.com/unmanarc/uFastAuthD
Source0:        https://github.com/unmanarc/uFastAuthD/archive/main.tar.gz#/%{name}-%{version}-%{build_timestamp}.tar.gz
Group:          Applications/Internet
%define cmake cmake
%if 0%{?rhel} == 6
%define cmake cmake3
%endif
%if 0%{?rhel} == 7
%define cmake cmake3
%endif
%if 0%{?rhel} == 8
%define debug_package %{nil}
%endif
%if 0%{?rhel} == 9
%define debug_package %{nil}
%endif
%if 0%{?fedora} >= 33
%define debug_package %{nil}
%endif
BuildRequires: libMantids-devel >= 2.8.27
BuildRequires: %{cmake} systemd libMantids-sqlite zlib-devel boost-devel gcc-c++ jsoncpp-devel sqlite-devel
%if 0%{?rhel} == 7
BuildRequires:  openssl11-devel
%else
BuildRequires:  openssl-devel
%endif
Requires: libMantids >= 2.8.27
Requires: libMantids-sqlite zlib boost-regex jsoncpp sqlite
%if 0%{?rhel} == 7
Requires:       openssl11
%else
Requires:       openssl
%endif
%description
This package contains a server that provides a directory/authorization implementation for managing users for your libMantids applications.
%prep
%autosetup -n %{name}-main
%build
%if 0%{?rhel} == 7
%{cmake} -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_BUILD_TYPE=MinSizeRel -DSSLRHEL7=ON
%else
%{cmake} -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_BUILD_TYPE=MinSizeRel
%endif
make %{?_smp_mflags}
%clean
rm -rf $RPM_BUILD_ROOT
%install
rm -rf $RPM_BUILD_ROOT
%if 0%{?fedora} >= 33
ln -s . %{_host}
%endif
%if 0%{?rhel} >= 9
ln -s . %{_host}
ln -s . redhat-linux-build
%endif
%if 0%{?fedora} == 35
ln -s . redhat-linux-build
%endif
%if "%{_host}" == "powerpc64le-redhat-linux-gnu"
ln -s . ppc64le-redhat-linux-gnu
%endif
%if "%{_host}" == "s390x-ibm-linux-gnu"
ln -s . s390x-redhat-linux-gnu
%endif
%if "%{cmake}" == "cmake3"
%cmake3_install
%else
%cmake_install
%endif
mkdir -vp $RPM_BUILD_ROOT/var/lib/ufastauthd
chmod 700 $RPM_BUILD_ROOT/var/lib/ufastauthd
mkdir -vp $RPM_BUILD_ROOT/var/www
cp -a var/www/ufastauthd $RPM_BUILD_ROOT/var/www
cp -a var/www/ufastauthd2 $RPM_BUILD_ROOT/var/www
mkdir -vp $RPM_BUILD_ROOT/etc
cp -a etc/ufastauthd $RPM_BUILD_ROOT/etc/
chmod 600 $RPM_BUILD_ROOT/etc/ufastauthd/snakeoil.key
chmod 600 $RPM_BUILD_ROOT/etc/ufastauthd/config.ini
mkdir -vp $RPM_BUILD_ROOT/usr/lib/systemd/system
cp usr/lib/systemd/system/ufastauthd.service $RPM_BUILD_ROOT/usr/lib/systemd/system/%{name}.service
chmod 644 $RPM_BUILD_ROOT/usr/lib/systemd/system/%{name}.service
%files
%doc
%{_bindir}/uFastAuthD
%config(noreplace) /etc/ufastauthd/ca.crt
%config(noreplace) /etc/ufastauthd/snakeoil.crt
%config(noreplace) /etc/ufastauthd/snakeoil.key
%config(noreplace) /etc/ufastauthd/config.ini
/var/www/ufastauthd/*
/var/www/ufastauthd2/*
%dir /var/lib/ufastauthd
/usr/lib/systemd/system/%{name}.service
%post
%systemd_post %{name}.service
%preun
%systemd_preun %{name}.service
%postun
%systemd_postun_with_restart %{name}.service
%changelog
