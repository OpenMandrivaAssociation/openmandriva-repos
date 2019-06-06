%define am_i_cooker 0
%define am_i_rolling 1

%ifarch %{x86_64}
%global secondary_distarch i686
%else
%ifarch %{aarch64}
%global secondary_distarch armv7hnl
%endif
%endif

Name:		openmandriva-repos
Version: 	4.0.1
# In Cooker, it should be 0.0.X
# In Rolling, it should be 0.1.X
# For release candidates, it should be 0.2.X
# Before final release, bump to 1
%if %am_i_cooker
Release:	0.0.4
%else
%if %am_i_rolling
Release:	0.1.4
%else
Release:	2
%endif
%endif
Summary:	OpenMandriva package repositories
Group:		System/Base
License:	MIT

# OpenMandriva GPG key
Source0:	RPM-GPG-KEY-OpenMandriva

Provides:	openmandriva-repos(%{version})
Requires:	system-release(%{version})
Requires:	openmandriva-repos-pkgprefs = %{EVRD}
Requires:	openmandriva-repos-keys = %{EVRD}

Obsoletes:	openmandriva-repos-cooker < %{EVRD}

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
Suggests:	grub2

# vim
Suggests:	vim-enhanced

# libGL.so.1 (also provided by proprietary drivers)
Suggests:	libgl1
Suggests:	lib64gl1

# Prefer openssh-askpass over openssh-askpass-gnome (for keychain)
Suggests:	openssh-askpass

# Python 3.x
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
Suggests:	phonon-gstreamer

# phonon4qt5-backend: prefer phonon4qt5-vlc over phonon4qt5-gstreamer
Suggests:	phonon4qt5-gstreamer

# mate backends
Suggests:	mate-settings-daemon-pulse
Suggests:	mate-media-pulse

## Devel

# xemacs-extras provides ctags, prefer simple ctags
Suggests:	ctags

# prefer openssl-devel over libressl-devel
Suggests:	libopenssl-devel
Suggests:	lib64openssl-devel

# preferred compiler(s)
Suggests:	clang
Suggests:	libstdc++-devel

# prefer dnf-utils over urpmi-debuginfo-install
Suggests:	dnf-utils

## Servers

# sendmail-command and mail-server
Suggests:	postfix

# imap-server
Suggests:	dovecot

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
Suggests:	systemd

# vnc
Suggests:	tigervnc

# x2goserver database backend
Suggests:	x2goserver-sqlite

## Various
# sane (also provided by saned)
Suggests:	sane-backends

# skanlite vs. xsane
Suggests:	skanlite

# virtual-notification-daemon
Suggests:	notification-daemon

# sgml-tools
# (the other choice is linuxdoc-tools which requires docbook-utils anyway)
Suggests:	docbook-utils

# input method
Suggests:	fcitx

# drupal database storage
Suggests:	drupal-mysql

# polkit-agent
Suggests:	polkit-kde-agent-1

# java
Suggests:	jre-current
Suggests:	jdk-current

# java-plugin
Suggests:	icedtea-web

Suggests:	lxsession-lite

# drupal database storage
Suggests:	drupal-mysqli

# pinentry
Suggests:	pinentry-qt5

# %{_lib}qt5-output-driver
Suggests:	libqt5gui-x11
Suggests:	lib64qt5gui-x11

%description pkgprefs
This package supplies DNF and PackageKit with global
preferences for packages in which multiple options are possible.

%prep
# Nothing to prepare

%build
# Nothing to build

%install
ARCH=%{_target_cpu}
echo $ARCH |grep -q arm && ARCH=armv7hnl
[ "$ARCH" = "i386" ] && ARCH=i686
[ "$ARCH" = "i586" ] && ARCH=i686

# Install the GPG key
mkdir -p %{buildroot}%{_sysconfdir}/pki/rpm-gpg
install %{S:0} -pm 0644 %{buildroot}%{_sysconfdir}/pki/rpm-gpg

# Install the repositories
mkdir -p %{buildroot}%{_sysconfdir}/yum.repos.d

%if %{defined secondary_distarch}
SECONDARY_ARCH=%{secondary_distarch}
%else
SECONDARY_ARCH=""
%endif

for arch in ${ARCH} ${SECONDARY_ARCH}; do
	for release in release rock rolling cooker; do
		for repo in main unsupported restricted non-free; do
			case "$repo" in
			main)
				REPO=""
				REPONAME=""
				;;
			*)
				REPO="-$repo"
				REPONAME=" - $(echo $repo |cut -b1 |tr a-z A-Z)$(echo $repo |cut -b2-)"
				;;
			esac

			vertag=$release
			case "$release" in
			release)
				NAME='OpenMandriva $releasever'"$REPONAME - $arch"
				HAS_UPDATES=true
				vertag='$releasever'
				;;
			rock)
				NAME="OpenMandriva Rock$REPONAME - $arch"
				HAS_UPDATES=true
				;;
			rolling)
				NAME="OpenMandriva Rolling$REPONAME - $arch"
				HAS_UPDATES=false
				;;
			cooker)
				NAME="OpenMandriva Cooker$REPONAME - $arch"
				HAS_UPDATES=false
				;;
			esac
			cat >>%{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-$release-$arch.repo <<EOF
[$release-$arch$REPO]
name="$NAME"
# Master repository:
# baseurl=http://abf-downloads.openmandriva.org/$vertag/repository/${arch}/${repo}/release/
mirrorlist=http://mirrors.openmandriva.org/mirrors.php?platform=$vertag&arch=${arch}&repo=${repo}&release=release
fastestmirror=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva
enabled=0

EOF

			if $HAS_UPDATES; then
				cat >>%{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-$release-$arch.repo <<EOF
[$release-updates-$arch$REPO]
name="$NAME - Updates"
# Master repository:
# baseurl=http://abf-downloads.openmandriva.org/$vertag/repository/${arch}/${repo}/updates/
mirrorlist=http://mirrors.openmandriva.org/mirrors.php?platform=$vertag&arch=${arch}&repo=${repo}&release=updates
fastestmirror=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva
enabled=0

EOF
			fi

			cat >>%{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-$release-$arch.repo <<EOF
[$release-testing-$arch$REPO]
name="$NAME - Testing"
# Master repository:
# baseurl=http://abf-downloads.openmandriva.org/$vertag/repository/${arch}/${repo}/testing/
mirrorlist=http://mirrors.openmandriva.org/mirrors.php?platform=$vertag&arch=${arch}&repo=${repo}&release=testing
fastestmirror=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva
enabled=0

EOF

			cat >>%{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-$release-$arch.repo <<EOF
[$release-$arch$REPO-debuginfo]
name="$NAME - Debug"
# Master repository:
# baseurl=http://abf-downloads.openmandriva.org/$vertag/repository/${arch}/debug_${repo}/release/
mirrorlist=http://mirrors.openmandriva.org/mirrors.php?platform=$vertag&arch=${arch}&repo=debug_${repo}&release=release
fastestmirror=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva
enabled=0

EOF

			if $HAS_UPDATES; then
				cat >>%{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-$release-$arch.repo <<EOF
[$release-updates-$arch$REPO-debuginfo]
name="$NAME - Updates - Debug"
# Master repository:
# baseurl=http://abf-downloads.openmandriva.org/$vertag/repository/${arch}/debug_${repo}/updates/
mirrorlist=http://mirrors.openmandriva.org/mirrors.php?platform=$vertag&arch=${arch}&repo=debug_${repo}&release=updates
fastestmirror=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva
enabled=0

EOF
			fi

			cat >>%{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-$release-$arch.repo <<EOF
[$release-testing-$arch$REPO-debuginfo]
name="$NAME - Testing - Debug"
# Master repository:
# baseurl=http://abf-downloads.openmandriva.org/$vertag/repository/${arch}/debug_${repo}/testing/
mirrorlist=http://mirrors.openmandriva.org/mirrors.php?platform=$vertag&arch=${arch}&repo=debug_${repo}&release=testing
fastestmirror=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva
enabled=0

EOF

			cat >>%{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-$release-$arch-source.repo <<EOF
[$release-$arch$REPO-source]
name="$NAME - Source"
# Master repository:
# baseurl=http://abf-downloads.openmandriva.org/$vertag/repository/SRPMS/${repo}/release/
mirrorlist=http://mirrors.openmandriva.org/mirrors.php?platform=$vertag&arch=SRPMS&repo=${repo}&release=release
fastestmirror=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva
enabled=0

EOF

			if $HAS_UPDATES; then
				cat >>%{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-$release-$arch-source.repo <<EOF
[$release-updates-$arch$REPO-source]
name="$NAME - Updates - Source"
# Master repository:
# baseurl=http://abf-downloads.openmandriva.org/$vertag/repository/SRPMS/${repo}/updates/
mirrorlist=http://mirrors.openmandriva.org/mirrors.php?platform=$vertag&arch=SRPMS&repo=${repo}&release=updates
fastestmirror=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva
enabled=0

EOF
			fi

			cat >>%{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-$release-$arch-source.repo <<EOF
[$release-testing-$arch$REPO-source]
name="$NAME - Testing - Source"
# Master repository:
# baseurl=http://abf-downloads.openmandriva.org/$vertag/repository/SRPMS/${repo}/testing/
mirrorlist=http://mirrors.openmandriva.org/mirrors.php?platform=$vertag&arch=SRPMS&repo=${repo}&release=testing
fastestmirror=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva
enabled=0

EOF
		done
	done
done
sed -i '$ d' %{buildroot}%{_sysconfdir}/yum.repos.d/*.repo

## And enable the one we're installing from
%if %am_i_cooker
sed -e '0,/enabled=0/s//enabled=1/' -i %{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-cooker-${ARCH}.repo
%else
%if %am_i_rolling
sed -e '0,/enabled=0/s//enabled=1/' -i %{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-rolling-${ARCH}.repo
%else
# Second occurence in $RELEASE and Rock is updates/
sed -e '0,/enabled=0/s//enabled=1/' -i %{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-rock-${ARCH}.repo
sed -e '0,/enabled=0/s//enabled=1/' -i %{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-rock-${ARCH}.repo
%endif
%endif

chmod 0644 %{buildroot}%{_sysconfdir}/yum.repos.d/*.repo

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

%files pkgprefs
