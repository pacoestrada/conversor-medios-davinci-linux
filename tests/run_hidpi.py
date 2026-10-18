"""Run the GUI matrix with a system Xvfb (or XVFB override)."""
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[1]
for width, height, dpi in [(1920, 1080, 96), (1366, 768, 96),
                           (3840, 2160, 192), (1920, 1080, 192)]:
    subprocess.run([
        'xvfb-run', '-a', '-s', f'-screen 0 {width}x{height}x24 -dpi {dpi}',
        'python3', str(root / 'tests/test_gui.py')],
        env={**os.environ, 'TEST_SCALE': str(dpi / 72),
             'TEST_DESKTOP_FONT': '72'}, check=True)
