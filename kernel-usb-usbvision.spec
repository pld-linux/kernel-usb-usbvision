#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
#
%define		_snap	20060524
%define	rel	0.%{_snap}.1
Summary:	USBvision Linux device driver
Summary(de.UTF-8):   USBvision Linux Treiber
Summary(pl.UTF-8):   Sterownik dla Linuksa do urządzeń USBvision
Name:		kernel-usb-usbvision
Version:	0.9.8.3
Release:	%{rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	usbvision-%{version}-%{_snap}.tar.gz
# Source0-md5:	46f8067489bacf4c1759416cedf84405
URL:		http://usbvision.sourceforge.net/
%{?with_dist_kernel:BuildRequires:	kernel-source >= 2.6.0}
BuildRequires:	rpmbuild(macros) >= 1.330
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a Linux driver for the video grabber USBVision, a USB-only
cable used in many "webcam" devices. It supports streaming and capture
of color or monochrome video via the Video4Linux API.

%description -l de.UTF-8
Dies ist ein Linux Treiber für den Videoabfänger USBVision, der nur
mit USB Kabel Gereten wie Webcams zusammenarbeitet. Er unterstützt
Videowiedergabe in Farbe oder Monochrom durch die Video4Linux API.

%description -l pl.UTF-8
Ten pakiet zawiera sterownik dla Linuksa do urządzeń przechwytujących
obraz USBVision - działajacego wyłącznie z USB kabla używanego w wielu
urządzeniach typu webcam. Obsługuje strumienie oraz przechwytywanie
obrazu kolorowego lub monochromatycznego poprzez API Video4Linux.

%package -n kernel-smp-usb-usbvision
Summary:	USBvision Linux SMP device driver
Summary(de.UTF-8):   USBvision Linux SMP Treiber
Summary(pl.UTF-8):   Sterownik dla Linuksa SMP do urządzeń USBvision
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-usb-usbvision
This is a Linux SMP driver for the video grabber USBVision, a USB-only
cable used in many "webcam" devices. It supports streaming and capture
of color or monochrome video via the Video4Linux API.

%description -n kernel-smp-usb-usbvision -l de.UTF-8
Dies ist ein Linux SMP Treiber für den Videoabfänger USBVision, der
nur mit USB Kabel Gereten wie Webcams zusammenarbeitet. Er unterstützt
Videowiedergabe in Farbe oder Monochrom durch die Video4Linux API.

%description -n kernel-smp-usb-usbvision -l pl.UTF-8
Ten pakiet zawiera sterownik dla Linuksa SMP do urządzeń
przechwytujących obraz USBVision - działajacego wyłącznie z USB kabla
używanego w wielu urządzeniach typu webcam. Obsługuje strumienie oraz
przechwytywanie obrazu kolorowego lub monochromatycznego poprzez API
Video4Linux.

%prep
%setup -q -n usbvision

%build
%build_kernel_modules -m usbvision,i2c-algo-usb -C src

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m src/usbvision,src/i2c-algo-usb -d kernel/drivers/usb/media

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
