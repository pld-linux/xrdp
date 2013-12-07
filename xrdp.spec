Summary:	Remote desktop server
Summary(pl.UTF-8):	Serwer remote desktop
Name:		xrdp
Version:	0.6.1
Release:	1
License:	GPL
Group:		X11/Applications/Networking
Source0:	http://download.sourceforge.net/xrdp/%{name}-v%{version}.tar.gz
# Source0-md5:	26099c6588943262023607c1b4e774d8
Source1:	%{name}.init
Source2:	%{name}.pamd
Source3:	%{name}.xrdp.ini
Source4:	%{name}.sesman.ini
Source5:	%{name}.README.PLD
Source6:	%{name}.README.PLD.pl
Patch0:		format-security.patch
Patch1:		build.patch
Patch2:		heimdal.patch
Patch3:		link.patch
URL:		http://xrdp.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	freerdp-devel
BuildRequires:	heimdal-devel >= 1.5.3-4
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	/usr/bin/Xvnc
Requires:	rc-scripts
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
%setup -q -n %{name}-v%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

install %{SOURCE5} README.PLD
install %{SOURCE6} README.PLD.pl
awk '{gsub("LIBDIR","%{_libdir}"); print}' < %{SOURCE3} > xrdp.ini

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
export CFLAGS="%{rpmcflags} -DHEIMDAL"
%configure \
	--enable-kerberos \
	--enable-freerdp1
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{%{name},pam.d,rc.d/init.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/xrdp
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/sesman
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/sesman.ini

%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/lib*.{a,la,so}

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
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/sesman
%attr(754,root,root) /etc/rc.d/init.d/xrdp
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/xrdp.ini
%config(noreplace) %{_sysconfdir}/%{name}/rsakeys.ini
%config(noreplace) %{_sysconfdir}/%{name}/sesman.ini
%{_sysconfdir}/%{name}/km-0407.ini
%{_sysconfdir}/%{name}/km-0409.ini
%{_sysconfdir}/%{name}/km-040c.ini
%{_sysconfdir}/%{name}/km-0410.ini
%{_sysconfdir}/%{name}/km-0419.ini
%{_sysconfdir}/%{name}/km-041d.ini
%attr(755,root,root) %{_bindir}/xrdp-dis
%attr(755,root,root) %{_bindir}/xrdp-genkeymap
%attr(755,root,root) %{_bindir}/xrdp-keygen
%attr(755,root,root) %{_bindir}/xrdp-sesadmin
%attr(755,root,root) %{_bindir}/xrdp-sesrun
%attr(755,root,root) %{_bindir}/xrdp-sestest
%attr(755,root,root) %{_sbindir}/xrdp
%attr(755,root,root) %{_sbindir}/xrdp-chansrv
%attr(755,root,root) %{_sbindir}/xrdp-sesman
%attr(755,root,root) %{_sbindir}/xrdp-sessvc
%dir %{_libdir}/xrdp
%attr(755,root,root) %{_libdir}/xrdp/libcommon.so.*
%attr(755,root,root) %{_libdir}/xrdp/libmc.so.*
%attr(755,root,root) %{_libdir}/xrdp/librdp.so.*
%attr(755,root,root) %{_libdir}/xrdp/libscp.so.*
%attr(755,root,root) %{_libdir}/xrdp/libvnc.so.*
%attr(755,root,root) %{_libdir}/xrdp/libxrdp.so.*
%attr(755,root,root) %{_libdir}/xrdp/libxrdpfreerdp1.so.*
%attr(755,root,root) %{_libdir}/xrdp/libxup.so.*
%dir %{_datadir}/xrdp
%{_datadir}/xrdp/ad24b.bmp
%{_datadir}/xrdp/ad256.bmp
%{_datadir}/xrdp/cursor0.cur
%{_datadir}/xrdp/cursor1.cur
%{_datadir}/xrdp/sans-10.fv1
%{_datadir}/xrdp/xrdp24b.bmp
%{_datadir}/xrdp/xrdp256.bmp
%{_mandir}/man5/sesman.ini.5*
%{_mandir}/man5/xrdp.ini.5*
%{_mandir}/man8/xrdp-sesman.8*
%{_mandir}/man8/xrdp-sesrun.8*
%{_mandir}/man8/xrdp.8*
