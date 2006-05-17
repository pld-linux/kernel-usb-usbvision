#
# Conditional build:
%bcond_without	dist_kernel     # allow non-distribution kernel
%bcond_without	kernel          # don't build kernel modules
%bcond_without	smp             # don't build SMP module
%bcond_with	verbose         # verbose build (V=1)
#
%define		_snap	20050721
%define	rel	0.%{_snap}.1
Summary:	USBvision Linux device driver
Summary(de):	USBvision Linux Treiber
Summary(pl):	Sterownik dla Linuksa do urz±dzeñ USBvision
Name:		kernel-usb-usbvision
Version:	0.9.8.2
Release:	%{rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	usbvision.tar.gz
# Source0-md5:	a5afbc855fcc619146a4d50e384c37ec
Patch0:		%{name}_build.patch
URL:		http://usbvision.sourceforge.net/
%{?with_dist_kernel:BuildRequires:	kernel-source >= 2.6.0}
BuildRequires:	rpmbuild(macros) >= 1.118
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a Linux driver for the video grabber USBVision, a USB-only
cable used in many "webcam" devices. It supports streaming and capture
of color or monochrome video via the Video4Linux API.

%description -l de
Dies ist ein Linux Treiber für den Videoabfänger USBVision, der nur
mit USB Kabel Gereten wie Webcams zusammenarbeitet. Er unterstützt
Videowiedergabe in Farbe oder Monochrom durch die Video4Linux API.

%description -l pl
Ten pakiet zawiera sterownik dla Linuksa do urz±dzeñ przechwytuj±cych
obraz USBVision - dzia³ajacego wy³±cznie z USB kabla u¿ywanego w wielu
urz±dzeniach typu webcam. Obs³uguje strumienie oraz przechwytywanie
obrazu kolorowego lub monochromatycznego poprzez API Video4Linux.

%package -n kernel-smp-usb-usbvision
Summary:	USBvision Linux SMP device driver
Summary(de):	USBvision Linux SMP Treiber
Summary(pl):	Sterownik dla Linuksa SMP do urz±dzeñ USBvision
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-usb-usbvision
This is a Linux SMP driver for the video grabber USBVision, a USB-only
cable used in many "webcam" devices. It supports streaming and capture
of color or monochrome video via the Video4Linux API.

%description -n kernel-smp-usb-usbvision -l de
Dies ist ein Linux SMP Treiber für den Videoabfänger USBVision, der
nur mit USB Kabel Gereten wie Webcams zusammenarbeitet. Er unterstützt
Videowiedergabe in Farbe oder Monochrom durch die Video4Linux API.

%description -n kernel-smp-usb-usbvision -l pl
Ten pakiet zawiera sterownik dla Linuksa SMP do urz±dzeñ
przechwytuj±cych obraz USBVision - dzia³ajacego wy³±cznie z USB kabla
u¿ywanego w wielu urz±dzeniach typu webcam. Obs³uguje strumienie oraz
przechwytywanie obrazu kolorowego lub monochromatycznego poprzez API
Video4Linux.

%prep
%setup -q -n usbvision
%patch0 -p1

%build
cd src
%if %{with kernel}
# kernel module(s)
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	install -d $cfg
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -rf o
	install -d o/include/linux
	ln -sf %{_kernelsrcdir}/config-$cfg o/.config
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg o/Module.symvers
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h o/include/linux/autoconf.h
%if %{with dist_kernel}
	%{__make} -C %{_kernelsrcdir} O=$PWD/o prepare scripts
%else
	install -d o/include/config
	touch o/include/config/MARKER
#	ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
%endif

#
#	patching/creating makefile(s) (optional)
#
	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		SYSSRC=%{_kernelsrcdir} \
		SYSOUT=$PWD/o \
		M=$PWD O=$PWD/o \
		CONFIG_MODULES=y \
		CONFIG_NET_RADIO=y \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
		CC="%{__cc}" CPP="%{__cpp}" \
		SYSSRC=%{_kernelsrcdir} \
		SYSOUT=$PWD/o \
		M=$PWD O=$PWD/o \
		CONFIG_MODULES=y \
		CONFIG_NET_RADIO=y \
		%{?with_verbose:V=1}

	mv *.ko $cfg
done
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/kernel/drivers/usb/media

%if %{with kernel}
install src/%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}/*.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/usb/media
%if %{with smp} && %{with dist_kernel}
install src/smp/*.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/usb/media
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%post	-n kernel-smp-usb-usbvision
%depmod %{_kernel_ver}smp

%postun	-n kernel-smp-usb-usbvision
%depmod %{_kernel_ver}smp

%if %{with kernel}
%files
%defattr(644,root,root,755)
%doc FAQ
/lib/modules/%{_kernel_ver}/kernel/drivers/usb/media/*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-usb-usbvision
%defattr(644,root,root,755)
%doc FAQ
/lib/modules/%{_kernel_ver}smp/kernel/drivers/usb/media/*
%endif
%endif
