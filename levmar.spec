# TODO: PLASMA parallel library (http://icl.cs.utk.edu/plasma/)
#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	LEVMAR - Levenberg-Marquardt non-linear least squares algorithm
Summary(pl.UTF-8):	LEVMAR - nieliniowy algorytm najmniejszych kwadratów Levenberga-Marquardta
Name:		levmar
Version:	2.6
Release:	3
License:	GPL v2+
Group:		Libraries
Source0:	http://www.ics.forth.gr/~lourakis/levmar/%{name}-%{version}.tgz
# Source0-md5:	16bc34efa1617219f241eef06427f13f
Patch0:		%{name}-make.patch
URL:		http://www.ics.forth.gr/~lourakis/levmar/
%{?with_static_libs:BuildRequires:	cmake >= 2.6}
BuildRequires:	blas-devel
BuildRequires:	lapack-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LEVMAR is a copylefted C/C++ implementation of the Levenberg-Marquardt
non-linear least squares algorithm. LEVMAR includes double and single
precision LM versions, both with analytic and finite difference
approximated Jacobians. LEVMAR also has some support for constrained
non-linear least squares, allowing linear equation, box and linear
inequality constraints.

%description -l pl.UTF-8
LEVMAR to wydana na wolnej licencji implementacja w C/C++ nieliniowego
algorytmu najmniejszych kwadratów Levenberga-Marquardta. LEVMAR
zawiera wersje LM podwójnej i pojedynczej precyzji, z jakobianami
zarówno analitycznymi, jak i aproksymowanymi metodą różnic
skończonych. LEVMAR ma także obsługę w pewnym zakresie nieliniowego
algorytmu najmniejszych kwadratów z ograniczeniami w postaci równań
liniowych, przedziałów oraz nierówności liniowych.

%package devel
Summary:	Header files for LEVMAR library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki LEVMAR
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for LEVMAR library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki LEVMAR.

%package static
Summary:	Static LEVMAR library
Summary(pl.UTF-8):	Statyczna biblioteka LEVMAR
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static LEVMAR library.

%description static -l pl.UTF-8
Statyczna biblioteka LEVMAR.

%prep
%setup -q
%patch -P0 -p1

%build
# shared library (cmake suite doesn't support it)
install -d sobj
%{__make} -f Makefile.so \
	CC="%{__cc}" \
	CFLAGS='%{rpmcflags} %{rpmcppflags} $(CONFIGFLAGS) -Wall -fPIC' \
	LAPACKLIBS="-llapack -lblas -lm"
# now static
%if %{with static_libs}
install -d build
cd build
%cmake .. \
	-DLAPACKBLAS_DIR=%{_libdir} \
	-DF2C_LIB_NAME=m

%{__make}
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}}

install sobj/liblevmar.so.2.2 $RPM_BUILD_ROOT%{_libdir}
ln -sf liblevmar.so.2.2 $RPM_BUILD_ROOT%{_libdir}/liblevmar.so.2
ln -sf liblevmar.so.2.2 $RPM_BUILD_ROOT%{_libdir}/liblevmar.so
cp -p levmar.h $RPM_BUILD_ROOT%{_includedir}
%if %{with static_libs}
install build/liblevmar.a $RPM_BUILD_ROOT%{_libdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.txt 
%attr(755,root,root) %{_libdir}/liblevmar.so.*.*
%attr(755,root,root) %ghost %{_libdir}/liblevmar.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblevmar.so
%{_includedir}/levmar.h

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/liblevmar.a
%endif
