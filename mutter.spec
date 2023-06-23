## START: Set by rpmautospec
## (rpmautospec version 0.3.5)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 1;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

%global glib_version 2.75.1
%global gtk3_version 3.19.8
%global gtk4_version 4.0.0
%global gsettings_desktop_schemas_version 40~alpha
%global json_glib_version 0.12.0
%global libinput_version 1.19.0
%global pipewire_version 0.3.33
%global lcms2_version 2.6
%global colord_version 1.4.5
%global mutter_api_version 12

%global gnome_version 44.2
%global tarball_version %%(echo %{gnome_version} | tr '~' '.')


Name:          mutter
Version:       %{gnome_version}.qol.2
Release:       %autorelease
Summary:       Window and compositing manager based on Clutter

License:       GPLv2+
URL:           https://www.gnome.org
Source0:       https://download.gnome.org/sources/%{name}/44/%{name}-%{tarball_version}.tar.xz

# Work-around for OpenJDK's compliance test
Patch0:        0001-window-actor-Special-case-shaped-Java-windows.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1936991
Patch1:        mutter-42.alpha-disable-tegra.patch

# https://pagure.io/fedora-workstation/issue/79
Patch2:        0001-place-Always-center-initial-setup-fedora-welcome.patch

# Support Dynamic triple/double buffering
# https://gitlab.gnome.org/GNOME/mutter/-/merge_requests/1441
Patch3:        1441.patch
# Cherry-picked on top of gnome-44 branch
# Includes post-44.2 changes in gnome-44 branch

# Backports for 44.3
# https://gitlab.gnome.org/GNOME/mutter/-/merge_requests/3056
Patch4:        3056.patch
# Implement physical pixel rounding of Wayland surfaces for compliance with fractional-scale-v1
# https://gitlab.gnome.org/GNOME/mutter/-/merge_requests/2726
# GPU optimizations for partial surface update
# https://gitlab.gnome.org/GNOME/mutter/-/merge_requests/2965
# clutter: Optimize the finish-layout step during stage updating
# https://gitlab.gnome.org/GNOME/mutter/-/merge_requests/2679

# window-actor: Fix screencast with fractionally scaled surfaces
# https://gitlab.gnome.org/GNOME/mutter/-/merge_requests/3053
Patch5:        3053.patch

# clutter/frame-clock: Avoid rapidly toggling dynamic max render time
# https://gitlab.gnome.org/GNOME/mutter/-/merge_requests/3074
Patch6:        3074.patch
# Updated for triple buffering patch

# https://gitlab.gnome.org/GNOME/mutter/-/merge_requests/3089
Patch7:        3089.patch

BuildRequires: pkgconfig(gobject-introspection-1.0) >= 1.41.0
BuildRequires: pkgconfig(sm)
BuildRequires: pkgconfig(libwacom)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xdamage)
BuildRequires: pkgconfig(xext)
BuildRequires: pkgconfig(xfixes)
BuildRequires: pkgconfig(xi)
BuildRequires: pkgconfig(xrandr)
BuildRequires: pkgconfig(xrender)
BuildRequires: pkgconfig(xcursor)
BuildRequires: pkgconfig(xcomposite)
BuildRequires: pkgconfig(x11-xcb)
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: pkgconfig(xkbcommon-x11)
BuildRequires: pkgconfig(xkbfile)
BuildRequires: pkgconfig(xtst)
BuildRequires: mesa-libEGL-devel
BuildRequires: mesa-libGLES-devel
BuildRequires: mesa-libGL-devel
BuildRequires: mesa-libgbm-devel
BuildRequires: pkgconfig(glesv2)
BuildRequires: pkgconfig(graphene-gobject-1.0)
BuildRequires: pam-devel
BuildRequires: pkgconfig(libpipewire-0.3) >= %{pipewire_version}
BuildRequires: pkgconfig(sysprof-capture-4)
BuildRequires: sysprof-devel
BuildRequires: pkgconfig(libsystemd)
BuildRequires: xorg-x11-server-Xorg
BuildRequires: xorg-x11-server-Xvfb
BuildRequires: pkgconfig(xkeyboard-config)
# see src/tests/x11-test.sh
BuildRequires: zenity
BuildRequires: desktop-file-utils
# Bootstrap requirements
BuildRequires: gtk-doc gettext-devel git-core
BuildRequires: pkgconfig(libcanberra)
BuildRequires: pkgconfig(gsettings-desktop-schemas) >= %{gsettings_desktop_schemas_version}
BuildRequires: pkgconfig(gnome-settings-daemon)
BuildRequires: meson
BuildRequires: pkgconfig(gbm)
BuildRequires: pkgconfig(gnome-desktop-4)
BuildRequires: pkgconfig(gudev-1.0)
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(libstartup-notification-1.0)
BuildRequires: pkgconfig(wayland-eglstream)
BuildRequires: pkgconfig(wayland-protocols)
BuildRequires: pkgconfig(wayland-server)
BuildRequires: pkgconfig(lcms2) >= %{lcms2_version}
BuildRequires: pkgconfig(colord) >= %{colord_version}

BuildRequires: pkgconfig(json-glib-1.0) >= %{json_glib_version}
BuildRequires: pkgconfig(libinput) >= %{libinput_version}
BuildRequires: pkgconfig(xwayland)

Requires: control-center-filesystem
Requires: gsettings-desktop-schemas%{?_isa} >= %{gsettings_desktop_schemas_version}
Requires: gnome-settings-daemon
Requires: gtk3%{?_isa} >= %{gtk3_version}
Requires: gtk4%{?_isa} >= %{gtk4_version}
Requires: json-glib%{?_isa} >= %{json_glib_version}
Requires: libinput%{?_isa} >= %{libinput_version}
Requires: pipewire%{_isa} >= %{pipewire_version}
Requires: startup-notification
Requires: dbus

Recommends: mesa-dri-drivers%{?_isa}

Provides: firstboot(windowmanager) = mutter

# Cogl and Clutter were forked at these versions, but have diverged
# significantly since then.
Provides: bundled(cogl) = 1.22.0
Provides: bundled(clutter) = 1.26.0

%description
Mutter is a window and compositing manager that displays and manages
your desktop via OpenGL. Mutter combines a sophisticated display engine
using the Clutter toolkit with solid window-management logic inherited
from the Metacity window manager.

While Mutter can be used stand-alone, it is primarily intended to be
used as the display core of a larger system such as GNOME Shell. For
this reason, Mutter is very extensible via plugins, which are used both
to add fancy visual effects and to rework the window management
behaviors to meet the needs of the environment.

%package devel
Summary: Development package for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
# for EGL/eglmesaext.h that's included from public cogl-egl-defines.h header
Requires: mesa-libEGL-devel

%description devel
Header files and libraries for developing Mutter plugins. Also includes
utilities for testing Metacity/Mutter themes.

%package  tests
Summary:  Tests for the %{name} package
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tests
The %{name}-tests package contains tests that can be used to verify
the functionality of the installed %{name} package.

%prep
%autosetup -S git -n %{name}-%{tarball_version}

%build
%meson -Degl_device=true -Dwayland_eglstream=true
%meson_build

%install
%meson_install

%find_lang %{name}

%files -f %{name}.lang
%license COPYING
%doc NEWS
%{_bindir}/mutter
%{_libdir}/lib*.so.*
%{_libdir}/mutter-%{mutter_api_version}/
%{_libexecdir}/mutter-restart-helper
%{_libexecdir}/mutter-x11-frames
%{_datadir}/GConf/gsettings/mutter-schemas.convert
%{_datadir}/glib-2.0/schemas/org.gnome.mutter.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.mutter.wayland.gschema.xml
%{_datadir}/gnome-control-center/keybindings/50-mutter-*.xml
%{_mandir}/man1/mutter.1*
%{_udevrulesdir}/61-mutter.rules

%files devel
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*

%files tests
%{_libexecdir}/installed-tests/mutter-%{mutter_api_version}
%{_datadir}/installed-tests/mutter-%{mutter_api_version}
%{_datadir}/mutter-%{mutter_api_version}/tests

%changelog
%autochangelog
