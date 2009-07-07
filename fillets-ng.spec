
%define	_game_ver	0.9.1
%define _data_ver	0.9.0

Summary:	Fish Fillets - Next Generation
Summary(pl.UTF-8):	Fish Fillets - Next Generation (linuksowy port gry)
Name:		fillets-ng
Version:	%{_game_ver}
Release:	1
License:	GPL v2+
Group:		X11/Applications/Games
Source0:	http://dl.sourceforge.net/fillets/%{name}-%{version}.tar.gz
# Source0-md5:	13bb4f98d73bc0b6aff39ee1c9582adb
Source1:	http://dl.sourceforge.net/fillets/%{name}-data-%{_data_ver}.tar.gz
# Source1-md5:	5d733a990212a4b038d1ee76f700c54e
Source2:	%{name}.desktop
Source3:	%{name}.png
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
Summary(pl.UTF-8):	Instrukcja do gry Fish Fillets NG
Group:		X11/Applications/Games
Requires:	%{name} = %{version}-%{release}

%description docs
A manual for Fish Fillets NG.

%description docs -l pl.UTF-8
Instrukcja do gry Fish Fillets.

%package data
Summary:	Data files for Fish Fillets NG
Summary(pl.UTF-8):	Pliki z danymi do gry Fish Fillets NG
Group:		X11/Applications/Games
Requires:	%{name} = %{version}-%{release}

%description data
Data files for Fish Fillets NG.

%description data -l pl.UTF-8
Pliki z danymi do gry Fish Fillets NG.

%package intro
Summary:	Introduction video to Fish Fillets NG game
Summary(pl.UTF-8):	Film wprowadzający do gry Fish Fillets NG
Group:		X11/Applications/Games
Requires:	%{name} = %{version}-%{release}
Requires:	mplayer

%description intro
Introduction video to Fish Fillets NG game.

%description intro -l pl.UTF-8
Film wprowadzający do gry Fish Fillets NG.

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

install %{name}-data-%{_data_ver}/images/menu/intro.mpg $RPM_BUILD_ROOT%{_gamedatadir}
cat > $RPM_BUILD_ROOT%{_desktopdir}/fillets-ng-intro.desktop << EOF
[Desktop Entry]
Name=Fish Fillets Intro
Comment=Fish Fillets NG - Introduction
Comment[pl]=Fish Fillets NG - Wprowadzenie
Exec=mplayer -fs %{_gamedatadir}/intro.mpg
Icon=fillets-ng.png
Terminal=false
Type=Application
Encoding=UTF-8
Categories=Game;LogicGame;
# vi: encoding=utf-8
EOF

find $RPM_BUILD_ROOT%{_gamedatadir} -type d -fprintf %{name}.dirs '%%%%dir %{_gamedatadir}/%%P\n'

rm -rf $RPM_BUILD_ROOT%{_gamedatadir}/images/menu/intro.mpg

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS TODO
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/%{name}
%{_mandir}/man6/fillets.*
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png

%files data -f %{name}.dirs
%defattr(644,root,root,755)
%doc %{_gamedatadir}/images/menu/flags/copyright
%{_gamedatadir}/font/*
%{_gamedatadir}/images/*.png
%{_gamedatadir}/images/*/*.png
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
%{_gamedatadir}/intro.mpg
%{_desktopdir}/%{name}-intro.desktop
