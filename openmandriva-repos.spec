%define am_i_cooker 1

%if %{_arch} == "x86_64"
%global secondary_distarch i586
%endif

Name:		openmandriva-repos
Version: 	1
Release:	0.0.4
Summary:	OpenMandriva package repositories
Group:		System/Base
License:	MIT

# OpenMandriva GPG key
Source0:	RPM-GPG-KEY-OpenMandriva

# OpenMandriva release repo config templates
Source1:	openmandriva-main-repo
Source2:	openmandriva-extrasect-repo
Source3:	openmandriva-main-srcrepo
Source4:	openmandriva-extrasect-srcrepo

# Cooker repo config templates
Source5:	cooker-main-repo
Source6:	cooker-extrasect-repo
Source7:	cooker-main-srcrepo
Source8:	cooker-extrasect-srcrepo

Provides:	openmandriva-repos(%{version})
Requires:	system-release(%{version})
Requires:	openmandriva-repos-pkgprefs = %{EVRD}
Requires:	openmandriva-repos-keys = %{EVRD}

%if %{am_i_cooker}
Requires:	openmandriva-repos-cooker = %{EVRD}
%endif

%description
OpenMandriva package repository files for DNF and PackageKit
with GPG public keys.

%package keys
Summary:	OpenMandriva repository GPG keys
Group:		System/Base
# GPG keys are architecture independent
BuildArch:	noarch

%description keys
OpenMandriva GPG keys for validating packages from OpenMandriva repositories by
DNF and PackageKit.

%package pkgprefs
# (ngompa): See the following page on why this exists:
# https://fedoraproject.org/wiki/PackagingDrafts/ProvidesPreferences#Distribution_preference
Summary:	OpenMandriva repository package preferences
Group:		System/Base
# Preferences list is architecture independent
BuildArch:	noarch

## Base packages

# webfetch
Suggests:	curl

# webclient
Suggests:	lynx

# bootloader
Suggests:	grub

# vim
Suggests:	vim-minimal

# Always prefer perl-base over weird packages auto-providing same modules
Suggests:	perl-base

# libGL.so.1 (also provided by proprietary drivers)
Suggests:	libmesagl1
Suggests:	lib64mesagl1

# Prefer openssl over libressl
Suggests:	libopenssl1.0.0
Suggests:	lib64openssl1.0.0

# Prefer openssh-askpass over openssh-askpass-gnome (for keychain)
Suggests:	openssh-askpass

# Python 2.7
Suggests:	python

# Initrd
Suggests:	dracut

## Multimedia

# festival-voice
Suggests:	festvox-kallpc16k

# gnome-speech-driver
Suggests:	gnome-speech-driver-espeak

# esound
Suggests:	pulseaudio-esound-compat

# gst-install-plugins-helper
Suggests:	packagekit-gstreamer-plugin

# libbaconvideowidget.so.0 (totem backend)
Suggests:	libbaconvideowidget-gstreamer0
Suggests:	lib64baconvideowidget-gstreamer0

# phonon-backend: prefer phonon-vlc over phonon-gstreamer
Suggests:	phonon-vlc

# phonon4qt5-backend: prefer phonon4qt5-vlc over phonon4qt5-gstreamer
Suggests:	phonon4qt5-vlc

# mate backends
Suggests:	mate-settings-daemon-pulse
Suggests:	mate-media-pulse

## Devel

# xemacs-extras provides ctags, prefer simple ctags
Suggests:	ctags

# prefer openssl-devel over libressl-devel
Suggests:	libopenssl-devel
Suggests:	lib64openssl-devel

# prefer gcc over gcc3.3
# (gcc-cpp and gcc-c++ are no more needed, but keeping just in case)
Suggests:	gcc
Suggests:	gcc-cpp
Suggests:	gcc-c++
Suggests:	libstdc++-devel

## Servers

# sendmail-command and mail-server
Suggests:	postfix

# webserver
Suggests:	apache

# nfs-server
Suggests:	nfs-utils

# ftpserver
Suggests:	proftpd

# postgresql
Suggests:	libpq5
Suggests:	lib64pq5

# syslog-daemon
Suggests:	rsyslog

# vnc
Suggests:	tigervnc

# x2goserver database backend
Suggests:	x2goserver-sqlite

## Various
# sane (also provided by saned)
Suggests:	sane-backends

# virtual-notification-daemon
Suggests:	notification-daemon

# sgml-tools
# (the other choice is linuxdoc-tools which requires docbook-utils anyway)
Suggests:	docbook-utils

# input method
Suggests:	ibus
Suggests:	pyzy-db-open-phrase
Suggests:	ibus-ui-gtk3
# plasma-applet-kimpanel-backend: prefer plasma-applet-kimpanel-backend-ibus to plasma-applet-kimpanel-backend-scim
# Removed due to bug 8459
#plasma-applet-kimpanel-backend-ibus 

# drupal database storage
Suggests: drupal-mysql

# polkit-agent
Suggests:	mate-polkit

# java
Suggests:	java-1.8.0-openjdk
Suggests:	java-1.8.0-openjdk-devel

# java-plugin
Suggests:	icedtea-web

# kde-display-management: prefer kscreen to krandr for mga4
Suggests:	kscreen

# lightdm greeter
Suggests:	lightdm-gtk3-greeter


%description pkgprefs
This package supplies DNF and PackageKit with global
preferences for packages in which multiple options are possible.


%package cooker
Summary:	Cooker repo definitions
Group:		System/Base
Requires:	openmandriva-repos = %{EVRD}

%description cooker
This package provides the Cooker repo definitions.


%prep
# Nothing to prepare

%build
# Nothing to build

%install
# Install the GPG key
mkdir -p %{buildroot}%{_sysconfdir}/pki/rpm-gpg
install %{S:0} -pm 0644 %{buildroot}%{_sysconfdir}/pki/rpm-gpg

# Install the repositories
mkdir -p %{buildroot}%{_sysconfdir}/yum.repos.d

## Create the repositories for various sections
install %{S:1} -pm 0644 %{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-%{_arch}.repo
install %{S:3} -pm 0644 %{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-%{_arch}-source.repo
install %{S:4} -pm 0644 %{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-nonfree-%{_arch}-source.repo
install %{S:4} -pm 0644 %{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-restricted-%{_arch}-source.repo
install %{S:2} -pm 0644 %{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-nonfree-%{_arch}.repo
install %{S:2} -pm 0644 %{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-restricted-%{_arch}.repo

## Create the repositories for Cooker
install %{S:5} -pm 0644 %{buildroot}%{_sysconfdir}/yum.repos.d/cooker-%{_arch}.repo
install %{S:7} -pm 0644 %{buildroot}%{_sysconfdir}/yum.repos.d/cooker-%{_arch}-source.repo
install %{S:8} -pm 0644 %{buildroot}%{_sysconfdir}/yum.repos.d/cooker-nonfree-%{_arch}-source.repo
install %{S:8} -pm 0644 %{buildroot}%{_sysconfdir}/yum.repos.d/cooker-restricted-%{_arch}-source.repo
install %{S:6} -pm 0644 %{buildroot}%{_sysconfdir}/yum.repos.d/cooker-nonfree-%{_arch}.repo
install %{S:6} -pm 0644 %{buildroot}%{_sysconfdir}/yum.repos.d/cooker-restricted-%{_arch}.repo

## Fill in the correct values for the installed repo files
sed -e "s/@DIST_ARCH@/%{_arch}/g" -i %{buildroot}%{_sysconfdir}/yum.repos.d/*%{_arch}*.repo

sed -e "s/@DIST_SECTION@/nonfree/g" \
    -e "s/@DIST_SECTION_NAME@/Nonfree/g" \
    -i %{buildroot}%{_sysconfdir}/yum.repos.d/*nonfree*%{_arch}*.repo

sed -e "s/@DIST_SECTION@/restricted/g" \
    -e "s/@DIST_SECTION_NAME@/Restricted/g" \
    -i %{buildroot}%{_sysconfdir}/yum.repos.d/*restricted*%{_arch}*.repo

## Disable all nonfree and restricted repositories by default
sed -e "s/enabled=1/enabled=0/g" -i %{buildroot}%{_sysconfdir}/yum.repos.d/*nonfree*%{_arch}*.repo
sed -e "s/enabled=1/enabled=0/g" -i %{buildroot}%{_sysconfdir}/yum.repos.d/*restricted*%{_arch}*.repo

## For architectures with a secondary arch, we need to create repositories for them, too
%if %{defined secondary_distarch}
### Create the repositories for various sections, excluding sources (as they are identical to primary arch ones)
install %{S:1} -pm 0644 %{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-%{secondary_distarch}.repo
install %{S:2} -pm 0644 %{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-nonfree-%{secondary_distarch}.repo
install %{S:2} -pm 0644 %{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-restricted-%{secondary_distarch}.repo

### Create the repositories for Cooker, excluding sources (as they are identical to primary arch ones)
install %{S:5} -pm 0644 %{buildroot}%{_sysconfdir}/yum.repos.d/cooker-%{secondary_distarch}.repo
install %{S:6} -pm 0644 %{buildroot}%{_sysconfdir}/yum.repos.d/cooker-nonfree-%{secondary_distarch}.repo
install %{S:6} -pm 0644 %{buildroot}%{_sysconfdir}/yum.repos.d/cooker-restricted-%{secondary_distarch}.repo

### Fill in the correct values for the installed repo files
sed -e "s/@DIST_ARCH@/%{secondary_distarch}/g" -i %{buildroot}%{_sysconfdir}/yum.repos.d/*%{secondary_distarch}*.repo

sed -e "s/@DIST_SECTION@/nonfree/g" \
    -e "s/@DIST_SECTION_NAME@/Nonfree/g" \
    -i %{buildroot}%{_sysconfdir}/yum.repos.d/*nonfree*%{secondary_distarch}*.repo

sed -e "s/@DIST_SECTION@/restricted/g" \
    -e "s/@DIST_SECTION_NAME@/Restricted/g" \
    -i %{buildroot}%{_sysconfdir}/yum.repos.d/*restricted*%{secondary_distarch}*.repo

### Disable all secondary arch repositories by default
sed -e "s/enabled=1/enabled=0/g" -i %{buildroot}%{_sysconfdir}/yum.repos.d/*%{secondary_distarch}*.repo

%endif


%check
%if %{am_i_cooker}
case %{release} in 
    0.*) ;;
    *)
    echo "Cooker distro should have this package with release < 1"
    exit 1
    ;;
esac
%endif


%files
%dir %{_sysconfdir}/yum.repos.d
%config(noreplace) %{_sysconfdir}/yum.repos.d/openmandriva*.repo

%files keys
%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva

%files cooker
%config(noreplace) %{_sysconfdir}/yum.repos.d/cooker*.repo

%files pkgprefs
