
%define	_game_ver	0.7.3
%define _data_ver	0.7.1

Summary:	Fish Fillets - Next Generation
Summary(pl):	Fish Fillets - Next Generation
Name:		fillets-ng
Version:	%{_game_ver}
Release:	1
License:	GPLv2+
Group:		X11/Applications/Games
Source0:	http://dl.sourceforge.net/fillets/%{name}-%{version}.tar.gz
# Source0-md5:	3cdb20616c8bf4498f2990f4e0d526a1
Source1:	http://dl.sourceforge.net/fillets/%{name}-data-%{_data_ver}.tar.gz
# Source1-md5:	dabb8aa5dcce57e782a2a27343c40cc6
Source2:	%{name}.desktop
Source3:	%{name}.png
URL:		http://fishfillets.sourceforge.net/
BuildRequires:	SDL-devel >= 1.2.0
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	SDL_ttf-devel
BuildRequires:	fribidi-devel
BuildRequires:	lua50-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	sed >= 4.0
Requires:	%{name}-data = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_gamedatadir	%{_datadir}/games/%{name}

%description
Fish Fillets NG is a Linux port of wonderful puzzle game Fish Fillets
from ALTAR interactive. Fish Fillets NG is strictly a puzzle game.
The goal in every of the seventy levels is always the same: find
a safe way out.

%description -l pl
Fish Fillets NG to port wspania³ej gry logicznej Fish Fillets napisanej
przez ALTAR interactive. To gra na my¶lenie. Zadanie gracza w ka¿dym
z siedemdziesiêciu poziomów jest zawsze takie same: odnale¼æ bezpieczne
wyj¶cie.

%package docs
Summary:	A manual for Fish Fillets NG
Summary(pl):	Instrukcja do Fish Fillets NG
Group:	X11/Applications/Games
Requires:	%{name} = %{version}-%{release}

%description docs
A manual for Fish Fillets NG

%description docs -l pl
Instrukcja do Fish Fillets

%package data
Summary:	Data files for Fish Fillets NG
Summary(pl):	Pliki z danymi dla Fish Fillets NG
Group:	X11/Application/Games
Requires:	%{name} = %{version}-%{release}

%description data
Data files for Fish Fillets NG.

%description data -l pl
Pliki z danymi dla Fish Fillets NG

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
	%{__sed} -i 's|LUA_LIBS = -L/usr/include/lua50 -llua -llualib|LUA_LIBS = -L/usr/include/lua50 -llua50 -llualib50|' {} \
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

%files data
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
%{_datadir}/%{name}/doc/html/*
