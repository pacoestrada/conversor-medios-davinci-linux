Name:           conversor-mp4-mov
Version:        2.1.0
Release:        1%{?dist}
Summary:        Conversor gráfico de MP4 a MOV
License:        MIT
URL:            https://github.com/pacoestrada/conversor-medios-davinci-linux
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch
Requires:       bash
Requires:       ffmpeg
Requires:       zenity

%description
Aplicación gráfica para convertir uno o varios vídeos MP4, o una carpeta
completa, a MOV. Conserva vídeo y audio sin recodificación cuando es posible.

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
install -Dm755 src/conversor-medios %{buildroot}%{_bindir}/conversor-medios
install -Dm644 data/com.pacoestrada.ConversorMp4Mov.desktop \
    %{buildroot}%{_datadir}/applications/com.pacoestrada.ConversorMp4Mov.desktop
for tamano in 48 64 128 256 512; do
    install -Dm644 \
        data/icons/${tamano}x${tamano}/com.pacoestrada.ConversorMp4Mov.png \
        %{buildroot}%{_datadir}/icons/hicolor/${tamano}x${tamano}/apps/com.pacoestrada.ConversorMp4Mov.png
done

%files
%license LICENSE
%{_bindir}/conversor-medios
%{_datadir}/applications/com.pacoestrada.ConversorMp4Mov.desktop
%{_datadir}/icons/hicolor/*/apps/com.pacoestrada.ConversorMp4Mov.png

%changelog
* Sat Oct 17 2026 Paco Estrada - 2.1.0-1
- Nuevo icono con atribución y primer paquete RPM.
