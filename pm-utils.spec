#specfile originally created for Fedora, modified for Moblin Linux
Name: pm-utils
Summary: Power management utilities and scripts for Moblin
License: GPLv2
Version: 1.4.1
Release: 1
Group: System/Base
URL: http://pm-utils.freedesktop.org
# Disabled: usermode
# Removed as no calls to lspci, setpci or update-pciids is done.
# Requires: pciutils >= 2.2.1
# for on_ac_power
Source0: http://pm-utils.freedesktop.org/releases/pm-utils-%{version}.tar.gz
Source1: pm-suspend.pam
Source2: pm-hibernate.pam
Source3: pm-powersave.pam
Source4: pm-suspend-hybrid.pam
Source5: pm-quirks-20100316.tar.gz


Source11: pm-suspend.app
Source12: pm-hibernate.app
Source13: pm-powersave.app
Source14: pm-suspend-hybrid.app

Source23: pm-utils-bugreport-info.sh
Patch0  : dell-1012-s3-resume-failure-workaround.patch
Patch1  : pm-utils-10umount-SD.patch

# touch is in coreutils
Requires(post): coreutils

%description
The pm-utils package contains utilities and scripts useful for tasks related
to power management.

%package devel
Summary: Files for development using %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the pkg-config files for development
when building programs that use %{name}.

%prep
%setup -q 
%patch0 -p1
%patch1 -p1


%build
%configure
make %{?_smp_mflags}

%install

%make_install

install -m 0755 -d $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d
for pamsource in %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} ; do
	filename=$(basename ${pamsource} .pam)
	install -T -p -m 0644 ${pamsource} $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/${filename}
done

install -m 0755 -d $RPM_BUILD_ROOT/%{_sysconfdir}/security/console.apps/
for source in %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} ; do
	filename=$(basename ${source} .app)
	install -T -p -m 0644 ${source} $RPM_BUILD_ROOT/%{_sysconfdir}/security/console.apps/${filename}
done

install -m 0755 -d $RPM_BUILD_ROOT/%{_bindir}
pushd $RPM_BUILD_ROOT/%{_bindir}
for binary in pm-hibernate pm-powersave pm-suspend pm-suspend-hybrid; do
	ln -sf consolehelper ${binary}
done
popd

install -D -m 0600 /dev/null $RPM_BUILD_ROOT%{_localstatedir}/log/pm-suspend.log
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/pm-utils/{locks,storage}

install -D -m 0755 %{SOURCE23} $RPM_BUILD_ROOT%{_bindir}/pm-utils-bugreport-info.sh

install -D -m 0644 %{SOURCE5} $RPM_BUILD_ROOT/%{_libdir}/pm-utils/video-quirks.tar.gz
pushd $RPM_BUILD_ROOT/%{_libdir}/pm-utils/
tar xzfv video-quirks.tar.gz
popd
rm -f $RPM_BUILD_ROOT/%{_libdir}/pm-utils/video-quirks.tar.gz

%pre
if [ -f %{_sysconfdir}/sysconfig/pm ]; then
	mkdir -p %{_sysconfdir}/pm/config.d
	mv %{_sysconfdir}/sysconfig/pm %{_sysconfdir}/pm/config.d/01oldconfig.conf
fi


%post
if [ -f %{_sysconfdir}/pm/config.rpmsave ]; then
	mv %{_sysconfdir}/pm/config.rpmsave %{_sysconfdir}/pm/config.d/02oldconfig.conf
fi
touch -a %{_localstatedir}/log/pm-suspend.log
if [ -f %{_localstatedir}/log/pm-suspend.log ] ; then
	chmod 0600 %{_localstatedir}/log/pm-suspend.log
	[ -x /sbin/restorecon ] && restorecon  %{_localstatedir}/log/pm-suspend.log > /dev/null 2>&1 ||:
fi


%files
%defattr(-,root,root,-)
%doc COPYING
%doc %{_docdir}/pm-utils
%{_sysconfdir}/pm/
%{_sysconfdir}/security/console.apps/pm-hibernate
%{_sysconfdir}/security/console.apps/pm-powersave
%{_sysconfdir}/security/console.apps/pm-suspend
%{_sysconfdir}/security/console.apps/pm-suspend-hybrid
%{_sysconfdir}/pam.d/pm-hibernate
%{_sysconfdir}/pam.d/pm-powersave
%{_sysconfdir}/pam.d/pm-suspend
%{_sysconfdir}/pam.d/pm-suspend-hybrid
%dir %{_libdir}/pm-utils/
%{_libdir}/pm-utils/bin/
%{_libdir}/pm-utils/defaults
%{_libdir}/pm-utils/functions
%{_libdir}/pm-utils/pm-functions
%{_libdir}/pm-utils/power.d/
%{_libdir}/pm-utils/sleep.d/
%{_libdir}/pm-utils/module.d
%{_libdir}/pm-utils/20-video-quirk-pm*
%{_bindir}/on_ac_power
%{_bindir}/pm-hibernate
%{_bindir}/pm-is-supported
%{_bindir}/pm-powersave
%{_bindir}/pm-suspend
%{_bindir}/pm-suspend-hybrid
%{_bindir}/pm-utils-bugreport-info.sh
%{_sbindir}/pm-hibernate
%{_sbindir}/pm-powersave
%{_sbindir}/pm-suspend
%{_sbindir}/pm-suspend-hybrid
%{_localstatedir}/run/pm-utils/
%exclude /usr/lib/pm-utils/power.d/sched-powersave

%ghost %verify(not md5 size mtime) %{_localstatedir}/log/pm-suspend.log

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/pm-utils.pc

