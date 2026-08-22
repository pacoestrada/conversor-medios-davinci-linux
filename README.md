# Conversor de medios para DaVinci Resolve en Linux

Script gráfico para convertir en lote archivos MP4 a contenedor MOV sin recodificar el vídeo. Está pensado para facilitar el trabajo con material de cámara en DaVinci Resolve sobre Linux.

La versión 1.3 incorpora un selector gráfico de carpetas. El script puede guardarse donde resulte más cómodo y, al ejecutarlo, permite navegar por el árbol de directorios para elegir dónde están los vídeos.

## Descarga recomendada

1. Abre la sección [**Releases**](https://github.com/pacoestrada/conversor-medios-davinci-linux/releases) del repositorio y entra en la versión más reciente.
2. Despliega **Assets**.
3. Descarga únicamente `Conversor-DaVinci-Linux-v1.3.sh`.
4. No descargues **Source code (zip)** ni **Source code (tar.gz)** salvo que quieras revisar o modificar el código del proyecto.

Los archivos de la carpeta `tests` son pruebas internas y no sirven para iniciar el conversor.

Después de la descarga, abre una terminal en la carpeta donde guardaste el archivo y ejecuta:

```bash
chmod +x Conversor-DaVinci-Linux-v1.3.sh
bash Conversor-DaVinci-Linux-v1.3.sh
```

Se abrirá un selector gráfico desde el que podrás navegar por el árbol de directorios y elegir la carpeta que contiene los vídeos. No es necesario escribir ninguna ruta.

## Qué hace

- Permite elegir gráficamente la carpeta que contiene los vídeos.
- Busca todos los archivos `.mp4` de la carpeta seleccionada y de sus subcarpetas.
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

1. Descarga `Conversor-DaVinci-Linux-v1.3.sh` desde **Assets** y guárdalo donde quieras, por ejemplo en tu carpeta de aplicaciones o herramientas.
2. Dale permiso de ejecución:

   ```bash
   chmod +x Conversor-DaVinci-Linux-v1.3.sh
   ```

3. Ejecútalo con doble clic y elige **Ejecutar como un programa**, o desde una terminal:

   ```bash
   bash Conversor-DaVinci-Linux-v1.3.sh
   ```

4. En la ventana que aparece, navega por el árbol de directorios y selecciona la carpeta que contiene los vídeos.

No hay que escribir ni pegar ninguna ruta. El programa recuerda como punto de partida la carpeta donde está guardado el script, pero permite seleccionar cualquier otra. Si se cancela la selección, termina sin realizar cambios.

## Conversión utilizada

Para cada archivo, el script ejecuta el equivalente a:

```bash
ffmpeg -i entrada.mp4 -c:v copy -c:a pcm_s24le salida.mov
```

El vídeo permanece idéntico al original. Solo se cambia el contenedor y se transforma el audio a PCM de 24 bits.

## Archivos problemáticos

Un MP4 extremadamente pequeño o incompleto puede no contener ninguna pista utilizable. En ese caso FFmpeg puede mostrar `Output file does not contain any stream`. El script continúa con los demás vídeos, informa del archivo problemático y borra la salida incompleta.

## Pruebas

La prueba automática de la selección de carpeta y la conversión por lotes puede ejecutarse desde la raíz del proyecto:

```bash
bash ./tests/test_v1_3.sh
```

## Licencia

Distribuido bajo la licencia MIT.
