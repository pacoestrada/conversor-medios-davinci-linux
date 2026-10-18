Name:           conversor-mp4-mov
Version:        2.3.6
Release:        1%{?dist}
Summary:        Conversor gráfico bidireccional MP4 y MOV
License:        MIT
URL:            https://github.com/pacoestrada/conversor-medios-davinci-linux
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch
Requires:       bash
Requires:       ffmpeg
Requires:       zenity
Requires:       python3
Requires:       python3-tkinter
Requires:       xrandr

%description
Aplicación gráfica que convierte MP4 a MOV con PCM y MOV a MP4 con AAC,
copiando el vídeo sin recodificar y verificando el resultado.

%prep
%autosetup

%build

%install
install -Dm755 src/conversor-gui.py %{buildroot}%{_bindir}/conversor-medios
install -Dm755 src/conversor-medios %{buildroot}/usr/lib/conversor-medios/conversor-medios
install -Dm644 data/com.pacoestrada.ConversorMp4Mov.desktop %{buildroot}%{_datadir}/applications/com.pacoestrada.ConversorMp4Mov.desktop
for tamano in 48 64 128 256 512; do
    install -Dm644 data/icons/${tamano}x${tamano}/com.pacoestrada.ConversorMp4Mov.png \
        %{buildroot}%{_datadir}/icons/hicolor/${tamano}x${tamano}/apps/com.pacoestrada.ConversorMp4Mov.png
done

%files
%license LICENSE
%{_bindir}/conversor-medios
/usr/lib/conversor-medios/conversor-medios
%{_datadir}/applications/com.pacoestrada.ConversorMp4Mov.desktop
%{_datadir}/icons/hicolor/*/apps/com.pacoestrada.ConversorMp4Mov.png

%changelog
* Sun Oct 18 2026 Paco Estrada - 2.3.6-1
- Corrige la versión mostrada en los diálogos del conversor.

* Sun Oct 18 2026 Paco Estrada - 2.3.5-1
- Ventana inicial adaptable y cabecera neutra.

* Sat Oct 17 2026 Paco Estrada - 2.3.0-1
- Nuevo icono firmado y primer paquete RPM.
