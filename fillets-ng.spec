
%define	_game_ver	0.7.4
%define _data_ver	0.7.4

Summary:	Fish Fillets - Next Generation
Summary(pl.UTF-8):	Fish Fillets - Next Generation (linuksowy port gry)
Name:		fillets-ng
Version:	%{_game_ver}
Release:	2
License:	GPL v2+
Group:		X11/Applications/Games
Source0:	http://dl.sourceforge.net/fillets/%{name}-%{version}.tar.gz
# Source0-md5:	912c146e70d90092a3dc89928e0be0f8
Source1:	http://dl.sourceforge.net/fillets/%{name}-data-%{_data_ver}.tar.gz
# Source1-md5:	0a2a651342d1035c292817048a4e373c
Source2:	%{name}.desktop
Source3:	%{name}.png
Source4:	http://fillets.sourceforge.net/intro.avi
# Source4-md5:	1bb4daa05062cd0c8f867320d70e84d9
URL:		http://fillets.sourceforge.net/
BuildRequires:	SDL-devel >= 1.2.0
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	SDL_ttf-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	fribidi-devel
BuildRequires:	lua50-devel
BuildRequires:	sed >= 4.0
Requires:	%{name}-data = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_gamedatadir	%{_datadir}/games/%{name}

%description
Fish Fillets NG is a Linux port of wonderful puzzle game Fish Fillets
from ALTAR interactive. Fish Fillets NG is strictly a puzzle game.
The goal in every of the seventy levels is always the same: find
a safe way out.

%description -l pl.UTF-8
Fish Fillets NG to port wspaniałej gry logicznej Fish Fillets
napisanej przez ALTAR interactive. To gra na myślenie. Zadanie gracza
w każdym z siedemdziesięciu poziomów jest zawsze takie same: odnaleźć
bezpieczne wyjście.

%package docs
Summary:	A manual for Fish Fillets NG
Summary(pl.UTF-8):	Instrukcja do Fish Fillets NG
Group:		X11/Applications/Games
Requires:	%{name} = %{version}-%{release}

%description docs
A manual for Fish Fillets NG.

%description docs -l pl.UTF-8
Instrukcja do Fish Fillets.

%package data
Summary:	Data files for Fish Fillets NG
Summary(pl.UTF-8):	Pliki z danymi dla Fish Fillets NG
Group:		X11/Application/Games
Requires:	%{name} = %{version}-%{release}

%description data
Data files for Fish Fillets NG.

%description data -l pl.UTF-8
Pliki z danymi dla Fish Fillets NG

%package intro
Summary:	Introduction video to Fish Fillets NG game
Summary(pl.UTF-8):	Film wprowadzający do gry Fish Fillets NG
Group:		X11/Application/Games
Requires:	%{name} = %{version}-%{release}
Requires:	mplayer

%description intro
Introduction video to Fish Fillets NG game

%description intro -l pl.UTF-8
Film wprowadzający do gry Fish Fillets NG

%prep
%setup -q -a1

%build
%{__aclocal}
%{__autoconf}
%{__automake}

%configure \
	--with-lua=/usr/include/lua50

# Now isn't that nasty? but I don't know how to do this better
find -name Makefile -exec \
	%{__sed} -i 's|LUA_LIBS = -L/usr/include/lua50 -llua -llualib|LUA_LIBS = -llua50 -llualib50|' {} \
	\;
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/%{name},%{_desktopdir},%{_pixmapsdir}}
install -d $RPM_BUILD_ROOT%{_gamedatadir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	bindir=%{_bindir}

install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE3} $RPM_BUILD_ROOT%{_pixmapsdir}
cp -Rfa %{name}-data-%{_data_ver}/{images,font,music,script,sound} $RPM_BUILD_ROOT%{_gamedatadir}
cp -Rfa %{name}-data-%{_data_ver}/doc $RPM_BUILD_ROOT%{_datadir}/%{name}
mv $RPM_BUILD_ROOT%{_bindir}/fillets $RPM_BUILD_ROOT%{_bindir}/fillets.bin
cat > $RPM_BUILD_ROOT%{_bindir}/fillets << EOF
#!/bin/sh

%{_bindir}/fillets.bin systemdir=%{_gamedatadir} \$@
EOF

install %{SOURCE4} $RPM_BUILD_ROOT%{_gamedatadir}
cat > $RPM_BUILD_ROOT%{_desktopdir}/fillets-ng-intro.desktop << EOF
[Desktop Entry]
Name=Fish Fillets Intro
Comment=Fish Fillets NG - Introduction
Exec=mplayer -fs %{_gamedatadir}/intro.avi
Icon=fillets-ng.png
Terminal=false
Type=Application
Encoding=UTF-8
Categories=Game;LogicGame;
# vi: encoding=utf-8
EOF

find $RPM_BUILD_ROOT%{_gamedatadir} -type d -fprintf %{name}.dirs '%%%%dir %{_gamedatadir}/%%P\n'


%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS TODO
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/%{name}
%{_mandir}/man*/*
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png

%files data -f %{name}.dirs
%defattr(644,root,root,755)
%doc %{_gamedatadir}/images/menu/flags/copyright
%{_gamedatadir}/font/*
%{_gamedatadir}/images/*.png
%{_gamedatadir}/images/*/*.png
%{_gamedatadir}/images/*/*.svg
%{_gamedatadir}/images/*/*.xcf
%{_gamedatadir}/images/*/*/*.png
%{_gamedatadir}/images/*/*/*/*.png
%{_gamedatadir}/images/*/*/*/*/*.png
%{_gamedatadir}/music/*.ogg
%{_gamedatadir}/script/*.lua
%{_gamedatadir}/script/*/*.lua
%{_gamedatadir}/sound/*/*.ogg
%{_gamedatadir}/sound/*/*/*.ogg
%{_gamedatadir}/sound/*/*/*/*.ogg

%files docs
%defattr(644,root,root,755)
%dir %{_datadir}/%{name}/doc
%{_datadir}/%{name}/doc/html

%files intro
%defattr(644,root,root,755)
%{_gamedatadir}/intro.avi
%{_desktopdir}/%{name}-intro.desktop
