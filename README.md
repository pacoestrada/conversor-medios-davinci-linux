# Conversor MP4 a MOV para Linux

Aplicación gráfica para convertir archivos MP4 a MOV de forma sencilla y sin
perder calidad.

Permite seleccionar uno o varios archivos, o una carpeta completa con sus
subcarpetas. Intenta copiar vídeo y audio sin recodificarlos. Cuando el audio no
es compatible con MOV, mantiene el vídeo intacto y convierte únicamente el audio
a PCM de 24 bits.

## Descargar e instalar

Descarga la última versión desde la página de
[**Releases**](https://github.com/pacoestrada/conversor-medios-davinci-linux/releases/latest).

El archivo que necesitas es:

`conversor-mp4-mov_2.0.1_all.deb`

### Instalación gráfica

Haz doble clic sobre el archivo `.deb` descargado y pulsa **Instalar**.

### Instalación desde la terminal

Abre una terminal en la carpeta donde lo has descargado y ejecuta:

```bash
sudo apt install ./conversor-mp4-mov_2.0.1_all.deb
```

El instalador añadirá automáticamente las dependencias necesarias.

## Cómo usarlo

1. Abre **Conversor MP4 a MOV** desde el menú de aplicaciones.
2. Elige si quieres seleccionar una carpeta o uno o varios archivos MP4.
3. Confirma la selección y espera a que finalice el proceso.
4. Revisa el resumen de archivos convertidos, omitidos y fallidos.

Los archivos MOV se guardan junto a sus MP4 originales. Si un MOV ya existe, la
aplicación lo omite y no lo sobrescribe.

## Funciones principales

- Selección gráfica de archivos o carpetas completas.
- Búsqueda de MP4 en todas las subcarpetas.
- Conversión sin recodificar vídeo ni audio cuando es posible.
- Vídeo siempre intacto, incluso cuando el audio necesita conversión.
- Indicador gráfico de progreso.
- Resumen final de convertidos, omitidos y fallidos.
- Explicación útil para cada archivo que no se haya podido convertir.
- Eliminación automática de salidas incompletas.
- Icono y lanzador integrados en el menú de aplicaciones.

## Requisitos

- Debian, Ubuntu, Linux Mint o una distribución compatible con paquetes `.deb`.
- FFmpeg y Zenity, instalados automáticamente como dependencias.

## Desinstalar

```bash
sudo apt purge conversor-mp4-mov
```

## Para desarrolladores

Construir el paquete Debian:

```bash
bash packaging/build-deb.sh
```

Ejecutar las pruebas automáticas:

```bash
bash tests/test_v2.sh
```

La estructura para un futuro paquete RPM está preparada en `packaging/rpm/`.

## Versión anterior

La documentación y las descargas de la antigua versión 1.3 siguen disponibles
en la [release v1.3](https://github.com/pacoestrada/conversor-medios-davinci-linux/releases/tag/v1.3).

## Licencia

Distribuido bajo la licencia MIT.
