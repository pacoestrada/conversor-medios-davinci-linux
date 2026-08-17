# Conversor de medios para DaVinci Resolve en Linux

Script gráfico para convertir en lote archivos MP4 a contenedor MOV sin recodificar el vídeo. Está pensado para facilitar el trabajo con material de cámara en DaVinci Resolve sobre Linux.

## Qué hace

- Busca todos los archivos `.mp4` de la carpeta donde está el script y de sus subcarpetas.
- Genera cada `.mov` junto al archivo original.
- Copia el vídeo sin pérdida ni recodificación (`-c:v copy`).
- Convierte el audio a PCM de 24 bits (`pcm_s24le`), compatible con flujos de edición.
- Omite los archivos que ya tienen su MOV correspondiente.
- Muestra el progreso y el resumen final mediante una ventana gráfica.
- Si un archivo está dañado o no contiene vídeo o audio válido, lo incluye en el informe y elimina el MOV incompleto.

## Requisitos

- Linux con Bash.
- [FFmpeg](https://ffmpeg.org/).
- Zenity.

En Ubuntu y distribuciones derivadas:

```bash
sudo apt update
sudo apt install ffmpeg zenity
```

## Uso

1. Descarga `convertir_medios.sh` y colócalo dentro de la carpeta que contiene los vídeos.
2. Dale permiso de ejecución:

   ```bash
   chmod +x convertir_medios.sh
   ```

3. Ejecútalo con doble clic y elige **Ejecutar como un programa**, o desde una terminal:

   ```bash
   ./convertir_medios.sh
   ```

No hay que escribir ni pegar ninguna ruta. El programa toma automáticamente como origen su propia carpeta.

## Conversión utilizada

Para cada archivo, el script ejecuta el equivalente a:

```bash
ffmpeg -i entrada.mp4 -c:v copy -c:a pcm_s24le salida.mov
```

El vídeo permanece idéntico al original. Solo se cambia el contenedor y se transforma el audio a PCM de 24 bits.

## Archivos problemáticos

Un MP4 extremadamente pequeño o incompleto puede no contener ninguna pista utilizable. En ese caso FFmpeg puede mostrar `Output file does not contain any stream`. El script continúa con los demás vídeos, informa del archivo problemático y borra la salida incompleta.

## Licencia

Distribuido bajo la licencia MIT.
