# NOTE:
# - xrdp-signals.patch has been applied upstream in CVS, so it should be
#   removed for xrdp > 0.4.1
#
Summary:	Remote desktop server
Summary(pl.UTF-8):	Serwer remote desktop
Name:		xrdp
Version:	0.4.1
Release:	2
License:	GPL
Group:		X11/Applications/Networking
Source0:	http://dl.sourceforge.net/xrdp/%{name}-%{version}.tar.gz
# Source0-md5:	86a2afcb8d304d5003ecbbdbf46058c0
Source1:	%{name}.init
Source2:	%{name}.pamd
Source3:	%{name}.xrdp.ini
Source4:	%{name}.sesman.ini
Source5:	%{name}.README.PLD
Source6:	%{name}.README.PLD.pl
Patch0:		%{name}-paths.patch
Patch1:		%{name}-make.patch
Patch2:		%{name}-signals.patch
URL:		http://xrdp.sourceforge.net/
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Requires:	tightvnc-server
Requires:	xinitrc-ng
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
xrdp is an open source Remote Desktop Protocol (rdp) server for
UNIX-like systems. It is capable of accepting connections from
rdesktop and Microsoft's own terminal server / remote desktop clients.

Unlike Windows NT/2000/2003 server, xrdp will not display a Windows
desktop but an X window desktop to the user.

Xrdp uses Xvnc or X11rdp backends to manage the X session.

%description -l pl.UTF-8
xrdp jest serwerem protokołu Remote Desktop (rdp) dla systemów
UNIXowych. Do xrdp można się łączyć zarówno programem rdesktop, jak i
klientami protokołu rdp Microsoftu.

xrdp używa jako backendu Xvnc lub X11rdp.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

install %{SOURCE5} README.PLD
install %{SOURCE6} README.PLD.pl
awk '{gsub("LIBDIR","%{_libdir}"); print}' < %{SOURCE3} > xrdp.ini

%build
%{__make} \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/xrdp,%{_sbindir},%{_docdir},%{_localstatedir}/run,%{_datadir}/%{name}} \
	$RPM_BUILD_ROOT%{_mandir}/man{5,8} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{%{name},pam.d,rc.d/init.d} \
	$RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/xrdp
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/sesman
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/sesman.ini
install xrdp.ini $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/xrdp.ini
install libxrdp/libxrdp.so $RPM_BUILD_ROOT%{_libdir}/libxrdp.so
install rdp/librdp.so $RPM_BUILD_ROOT%{_libdir}/xrdp/librdp.so
install sesman/sessvc $RPM_BUILD_ROOT%{_sbindir}/sessvc
install sesman/sesman $RPM_BUILD_ROOT%{_sbindir}/sesman
install sesman/startwm.sh $RPM_BUILD_ROOT%{_sbindir}/startwm.sh
install sesman/libscp/libscp.so $RPM_BUILD_ROOT%{_libdir}/libscp.so
install sesman/tools/sesrun $RPM_BUILD_ROOT%{_sbindir}/sesrun
install sesman/tools/sestest $RPM_BUILD_ROOT%{_sbindir}/sestest
install vnc/libvnc.so $RPM_BUILD_ROOT%{_libdir}/xrdp/libvnc.so
install xrdp/xrdp $RPM_BUILD_ROOT%{_sbindir}/xrdp
install xrdp/ad256.bmp $RPM_BUILD_ROOT%{_datadir}/%{name}/ad256.bmp
install xrdp/xrdp256.bmp $RPM_BUILD_ROOT%{_datadir}/%{name}/xrdp256.bmp
install xrdp/cursor0.cur $RPM_BUILD_ROOT%{_datadir}/%{name}/cursor0.cur
install xrdp/cursor1.cur $RPM_BUILD_ROOT%{_datadir}/%{name}/cursor1.cur
install xrdp/Tahoma-10.fv1 $RPM_BUILD_ROOT%{_datadir}/%{name}/Tahoma-10.fv1
install xrdp/rsakeys.ini $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/rsakeys.ini
install xup/libxup.so $RPM_BUILD_ROOT%{_libdir}/xrdp/libxup.so
install docs/man/sesman.8 $RPM_BUILD_ROOT%{_mandir}/man8/sesman.8
install docs/man/sesrun.8 $RPM_BUILD_ROOT%{_mandir}/man8/sesrun.8
install docs/man/xrdp.8 $RPM_BUILD_ROOT%{_mandir}/man8/xrdp.8
install docs/man/sesman.ini.5 $RPM_BUILD_ROOT%{_mandir}/man5/sesman.ini.5
install docs/man/xrdp.ini.5 $RPM_BUILD_ROOT%{_mandir}/man5/xrdp.ini.5

%post
/sbin/ldconfig
/sbin/chkconfig --add xrdp
%service xrdp restart "xrdp server"

%postun -p /sbin/ldconfig

%preun
if [ "$1" = "0" ]; then
	%service xrdp stop
	/sbin/chkconfig --del xrdp
fi


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.txt
%doc README.PLD
%doc README.PLD.pl
%dir %{_sysconfdir}/%{name}
%dir %{_localstatedir}/run
%{_libdir}/libscp.so
%{_libdir}/libxrdp.so
%{_libdir}/xrdp
%{_datadir}/xrdp
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/sesman
%attr(754,root,root) /etc/rc.d/init.d/xrdp
%config(noreplace) %{_sysconfdir}/%{name}/xrdp.ini
%config(noreplace) %{_sysconfdir}/%{name}/rsakeys.ini
%config(noreplace) %{_sysconfdir}/%{name}/sesman.ini
%{_mandir}/man8/*
%{_mandir}/man5/*
