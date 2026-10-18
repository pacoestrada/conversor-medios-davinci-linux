"""Monitor selection in Tk/X11 coordinates; no display needed."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch
spec = importlib.util.spec_from_file_location('gui', Path(__file__).resolve().parents[1] / 'src/conversor-gui.py')
gui = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gui)

class Window:
    def winfo_screenwidth(self): return 5760
    def winfo_screenheight(self): return 2160
    def winfo_pointerxy(self): return self.pointer

class MonitorTest(unittest.TestCase):
    def area(self, pointer, monitors, work='0, 32, 5760, 2128'):
        window = Window()
        window.pointer = pointer
        with patch.object(gui.subprocess, 'check_output', side_effect=[
                '_NET_CURRENT_DESKTOP = 0', '_NET_WORKAREA = ' + work, monitors]):
            return gui.available_area(window)

    def test_two_monitors(self):
        monitors = 'Monitors: 2\n 0: +LEFT 1920/500x1080/300+0+0 LEFT\n 1: +*MAIN 3840/600x2160/340+1920+0 MAIN'
        self.assertEqual(self.area((2500, 500), monitors), (1920, 32, 3840, 2128))
        self.assertEqual(self.area((500, 500), monitors), (0, 32, 1920, 1048))
        self.assertEqual(self.area((-1, -1), monitors), (1920, 32, 3840, 2128))

    def test_negative_origin(self):
        monitors = 'Monitors: 2\n 0: +LEFT 1920/500x1080/300-1920+0 LEFT\n 1: +*MAIN 3840/600x2160/340+0+0 MAIN'
        self.assertEqual(self.area((-500, 500), monitors, '-1920, 0, 5760, 2160'), (-1920, 0, 1920, 1080))

    def test_logical_coordinates(self):
        monitors = 'Monitors: 2\n 0: +LEFT 1920/500x1080/300+0+0 LEFT\n 1: +*MAIN 1920/600x1080/340+1920+0 MAIN'
        self.assertEqual(self.area((2200, 500), monitors), (1920, 32, 1920, 1048))

if __name__ == '__main__': unittest.main()
