#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	SVG rendering library
Name:		resvg
Version:	0.47.0
Release:	1
License:	Apache v2.0 or MIT
Group:		Libraries
Source0:	https://github.com/linebender/resvg/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	60b8ce21846f8da7f3116fe04017705c
URL:		https://github.com/linebender/resvg
BuildRequires:	cargo
BuildRequires:	rpmbuild(macros) >= 2.050
BuildRequires:	rust >= 1.87.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%{?rust_req}
ExclusiveArch:	%{rust_arches}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SVG rendering library.

%package devel
Summary:	Header files for resvg library
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Header files for resvg library.

%package static
Summary:	Static resvg library
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static resvg library.

%prep
%setup -q

%build
%cargo_build --frozen -p resvg-capi

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}}
cp -p %cargo_objdir/libresvg.so $RPM_BUILD_ROOT%{_libdir}
%{?with_static_libs:cp -p %cargo_objdir/libresvg.a $RPM_BUILD_ROOT%{_libdir}}
cp -p crates/c-api/resvg.h $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE-MIT README.md
%{_libdir}/libresvg.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/resvg.h

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libresvg.a
%endif
