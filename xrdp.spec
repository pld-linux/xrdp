#
# Conditional build:
%bcond_without	fuse	# clipboard file/drive redir via libfuse

Summary:	Remote desktop server
Summary(pl.UTF-8):	Serwer remote desktop
Name:		xrdp
Version:	0.10.4.1
Release:	2
License:	Apache v2.0
Group:		X11/Applications/Networking
#Source0Download: https://github.com/neutrinolabs/xrdp/releases
Source0:	https://github.com/neutrinolabs/xrdp/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	0da8c16ade55010f786ea4ca1627235a
Source1:	%{name}.init
Source2:	%{name}.pamd
Source3:	%{name}.README.PLD
Source4:	%{name}.README.PLD.pl
Source5:	startwm.sh
Patch0:		config.patch
Patch1:		quiet.patch
Patch2:		x32.patch
URL:		https://www.xrdp.org/
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.7.2
BuildRequires:	fdk-aac-devel >= 0.1.0
BuildRequires:	freetype-devel >= 1:2.8.0
BuildRequires:	imlib2-devel >= 1.4.5
BuildRequires:	lame-libs-devel
BuildRequires:	libfuse-devel >= 2.6
BuildRequires:	libjpeg-turbo-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	nasm
BuildRequires:	openssl-devel >= 0.9.8
BuildRequires:	opus-devel
BuildRequires:	pam-devel
BuildRequires:	pixman-devel >= 0.1.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	systemd-units
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXrandr-devel
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires:	/usr/bin/Xvnc
Requires:	fdk-aac >= 0.1.0
Requires:	freetype >= 1:2.8.0
Requires:	imlib2 >= 1.4.5
Requires:	libfuse >= 2.6
Requires:	openssl >= 0.9.8
Requires:	pixman >= 0.1.0
Requires:	rc-scripts
Requires:	systemd-units >= 38
Requires:	xinitrc-ng
Obsoletes:	xrdp-libs < 0.10
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

%package devel
Summary:	Header files for xrdp libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek xrdp
Group:		Development/Libraries
Obsoletes:	xrdp-static < 0.10.1-2

%description devel
Header files for xrdp libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek xrdp.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

install %{SOURCE3} README.PLD
install %{SOURCE4} README.PLD.pl

%build
CPPFLAGS="%{rpmcppflags} -D_FILE_OFFSET_BITS=64"
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
cd libpainter
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
cd ../librfxcodec
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
cd ..
%configure \
	--disable-silent-rules \
	--enable-fdkaac \
	%{?with_fuse:--enable-fuse} \
	--enable-ipv6 \
	--enable-mp3lame \
	--enable-opus \
	--enable-painter \
	--enable-pam-config=redhat \
	--enable-pixman \
	--enable-tjpeg \
	--enable-vsock \
	--enable-x264 \
	--with-freetype2 \
	--with-imlib2

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},/etc/{pam.d,rc.d/init.d,security}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/xrdp
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/sesman
%{__rm} $RPM_BUILD_ROOT/etc/pam.d/xrdp-sesman
%{__ln_s} sesman $RPM_BUILD_ROOT/etc/pam.d/xrdp-sesman
:> $RPM_BUILD_ROOT/etc/security/blacklist.sesman

%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/startwm.sh
cp -p %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/startwm.sh

%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/lib*.{a,la}
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%pre
%groupadd -g 183 xrdp

%post
/sbin/chkconfig --add xrdp
%service xrdp restart "xrdp server"
%systemd_post xrdp.service xrdp-sesman.service

%preun
if [ "$1" = "0" ]; then
	%service xrdp stop
	/sbin/chkconfig --del xrdp
fi
%systemd_preun xrdp.service xrdp-sesman.service

%postun
if [ "$1" = "0" ]; then
	%groupremove xrdp
fi
%systemd_reload

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING NEWS.md README.md README.PLD
%lang(pl) %doc README.PLD.pl
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/sesman
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.sesman
%attr(640,root,root) /etc/pam.d/xrdp-sesman
%attr(754,root,root) /etc/rc.d/init.d/xrdp
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/pulse
%config(noreplace) %{_sysconfdir}/%{name}/cert.pem
%config(noreplace) %{_sysconfdir}/%{name}/gfx.toml
%config(noreplace) %{_sysconfdir}/%{name}/key.pem
%config(noreplace) %{_sysconfdir}/%{name}/rsakeys.ini
%config(noreplace) %{_sysconfdir}/%{name}/sesman.ini
%config(noreplace) %{_sysconfdir}/%{name}/xrdp.ini
%config(noreplace) %{_sysconfdir}/%{name}/xrdp_keyboard.ini
%{_sysconfdir}/%{name}/km-*.ini
%config(noreplace) %{_sysconfdir}/%{name}/pulse/default.pa
%attr(755,root,root) %{_sysconfdir}/xrdp/reconnectwm.sh
%attr(755,root,root) %{_sysconfdir}/xrdp/startwm.sh
%attr(755,root,root) %{_bindir}/xrdp-dis
%attr(755,root,root) %{_bindir}/xrdp-dumpfv1
%attr(755,root,root) %{_bindir}/xrdp-genkeymap
%attr(755,root,root) %{_bindir}/xrdp-keygen
%attr(755,root,root) %{_bindir}/xrdp-mkfv1
%attr(755,root,root) %{_bindir}/xrdp-sesadmin
%attr(755,root,root) %{_bindir}/xrdp-sesrun
%attr(755,root,root) %{_sbindir}/xrdp
%attr(755,root,root) %{_sbindir}/xrdp-chansrv
%attr(755,root,root) %{_sbindir}/xrdp-sesman
%dir %{_libdir}/xrdp
%{_libdir}/xrdp/libcommon.so*
%{_libdir}/xrdp/libipm.so*
%{_libdir}/xrdp/libmc.so*
%{_libdir}/xrdp/libsesman.so*
%{_libdir}/xrdp/libtoml.so*
%{_libdir}/xrdp/libvnc.so*
%{_libdir}/xrdp/libxrdp.so*
%{_libdir}/xrdp/libxrdpapi.so*
%{_libdir}/xrdp/libxup.so*
%if "%{_libexecdir}" != "%{_libdir}"
%dir %{_libexecdir}/xrdp
%endif
%attr(755,root,root) %{_libexecdir}/xrdp/waitforx
%attr(755,root,root) %{_libexecdir}/xrdp/xrdp-droppriv
%attr(755,root,root) %{_libexecdir}/xrdp/xrdp-sesexec
%{systemdunitdir}/xrdp.service
%{systemdunitdir}/xrdp-sesman.service
%dir %{_datadir}/xrdp
%attr(755,root,root) %{_datadir}/xrdp/xrdp-chkpriv
%{_datadir}/xrdp/ad24b.bmp
%{_datadir}/xrdp/ad256.bmp
%{_datadir}/xrdp/cursor0.cur
%{_datadir}/xrdp/cursor1.cur
%{_datadir}/xrdp/sans-10.fv1
%{_datadir}/xrdp/xrdp24b.bmp
%{_datadir}/xrdp/xrdp256.bmp
%{_datadir}/xrdp/xrdp_logo.bmp
%{_datadir}/xrdp/README.logo
%{_datadir}/xrdp/sans-18.fv1
%{_datadir}/xrdp/xrdp_logo.png
%{_mandir}/man1/xrdp-dis.1*
%{_mandir}/man5/sesman.ini.5*
%{_mandir}/man5/gfx.toml.5*
%{_mandir}/man5/xrdp.ini.5*
%{_mandir}/man8/xrdp-chansrv.8*
%{_mandir}/man8/xrdp-dumpfv1.8*
%{_mandir}/man8/xrdp-genkeymap.8*
%{_mandir}/man8/xrdp-keygen.8*
%{_mandir}/man8/xrdp-mkfv1.8*
%{_mandir}/man8/xrdp-sesadmin.8*
%{_mandir}/man8/xrdp-sesman.8*
%{_mandir}/man8/xrdp-sesrun.8*
%{_mandir}/man8/xrdp.8*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libpainter.a
%{_libdir}/librfxencode.a
%{_includedir}/ms-*.h
%{_includedir}/painter.h
%{_includedir}/rfxcodec_common.h
%{_includedir}/rfxcodec_decode.h
%{_includedir}/rfxcodec_encode.h
%{_includedir}/xrdp_client_info.h
%{_includedir}/xrdp_constants.h
%{_includedir}/xrdp_rail.h
%{_includedir}/xrdp_sockets.h
%{_pkgconfigdir}/libpainter.pc
%{_pkgconfigdir}/rfxcodec.pc
%{_pkgconfigdir}/xrdp.pc
