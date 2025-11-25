import unittest
from utils import cartesian_cw_or_ccw, cartesian_heading_to_gps, cartesian_to_screen, find_distance, angle_between_positions
from utils import CW, CCW
from utils import smallest_angle_difference
from utils import gps_heading_to_cartesian

class TestVexSimulator(unittest.TestCase):

    def test_gps_heading_to_cartesian(self):
        # 0° GPS (north) -> 90° Cartesian (east)
        self.assertAlmostEqual(gps_heading_to_cartesian(0), 90.0)
        # 90° GPS (east) -> 0° Cartesian (x+)
        self.assertAlmostEqual(gps_heading_to_cartesian(90), 0.0)
        # 180° GPS (south) -> -90° Cartesian (y-)
        self.assertAlmostEqual(gps_heading_to_cartesian(180), -90.0)
        # -90° GPS (west) -> 180° Cartesian (x-)
        self.assertAlmostEqual(gps_heading_to_cartesian(-90), 180.0)
        # 135° GPS -> -45° Cartesian
        self.assertAlmostEqual(gps_heading_to_cartesian(135), -45.0)
        # -135° GPS -> 225°-360° = -135° Cartesian
        self.assertAlmostEqual(gps_heading_to_cartesian(-135), -135.0)

        # create identity conversions
        # avoid 180 and -180 boundary issues
        for angle in range(-179, 179, 1):
            cartesian_angle = gps_heading_to_cartesian(angle)
            gps_converted_back = cartesian_heading_to_gps(cartesian_angle)
            self.assertAlmostEqual(angle, gps_converted_back, msg=f"Failed at angle {angle}")

    def test_smallest_angle_difference(self):
        # No difference
        self.assertEqual(smallest_angle_difference(0, 0), (0, CCW))
        self.assertEqual(smallest_angle_difference(90, 90), (0, CCW))
        # 90 deg CCW
        self.assertEqual(smallest_angle_difference(90, 0), (90, CCW))
        # 90 deg CW
        self.assertEqual(smallest_angle_difference(0, 90), (90, CW))
        # 180 deg (should be CCW by convention)
        self.assertEqual(smallest_angle_difference(180, 0), (180, CCW))
        self.assertEqual(smallest_angle_difference(0, 180), (180, CCW))
        # Wrap around
        self.assertEqual(smallest_angle_difference(10, 350), (20, CCW))
        self.assertEqual(smallest_angle_difference(350, 10), (20, CW))
        # Wrap around but using negative angles
        self.assertEqual(smallest_angle_difference(-170, 170), (20, CCW))
        self.assertEqual(smallest_angle_difference(170, -170), (20, CW))
        # more wrap around with negative angles
        self.assertEqual(smallest_angle_difference(-10, 10), (20, CW))
        self.assertEqual(smallest_angle_difference(10, -10), (20, CCW))

    def test_angle_between_positions(self):
        x1, y1 = 0, 0
        step = 1
        self.angle_between_positions_worker(x1, y1, step)
        x1 = 10
        y1 = 10
        step = 1
        self.angle_between_positions_worker(x1, y1, step)
        step = 20
        self.angle_between_positions_worker(x1, y1, step)

    def angle_between_positions_worker(self, x1, y1, step):

        right = 0.0
        up_right = 45.0
        up = 90.0
        up_left = 135.0
        left = 180.0
        down_left = -135.0
        down = -90.0
        down_right = -45.0

        # Horizontal right
        self.assertAlmostEqual(angle_between_positions((x1, y1), (x1+step, y1)), right)
        # Horizontal left
        self.assertAlmostEqual(angle_between_positions((x1, y1), (x1-step, y1)), left)
        # Vertical up
        self.assertAlmostEqual(angle_between_positions((x1, y1), (x1, y1+step)), up)
        # Vertical down
        self.assertAlmostEqual(angle_between_positions((x1, y1), (x1, y1-step)), down)
        # 45 degrees (up-right)
        self.assertAlmostEqual(angle_between_positions((x1, y1), (x1+step, y1+step)), up_right)
        # -135 degrees (down-left)
        self.assertAlmostEqual(angle_between_positions((x1, y1), (x1-step, y1-step)), down_left)
        # 135 degrees (up-left)
        self.assertAlmostEqual(angle_between_positions((x1, y1), (x1-step, y1+step)), up_left)
        # -45 degrees (down-right)
        self.assertAlmostEqual(angle_between_positions((x1, y1), (x1+step, y1-step)), down_right)

    def test_cartesian_cw_or_ccw(self):
        # (target, current) -> expected direction
        self.assertEqual(cartesian_cw_or_ccw(90, 0), CCW)
        self.assertEqual(cartesian_cw_or_ccw(0, 90), CW)
        self.assertEqual(cartesian_cw_or_ccw(180, 0), CCW)
        self.assertEqual(cartesian_cw_or_ccw(0, 180), CW)
        self.assertEqual(cartesian_cw_or_ccw(-45, -90), CCW)
        self.assertEqual(cartesian_cw_or_ccw(-90, -45), CW)
        self.assertEqual(cartesian_cw_or_ccw(-90, -180), CCW)
        self.assertEqual(cartesian_cw_or_ccw(-180, -90), CW)
        self.assertEqual(cartesian_cw_or_ccw(-180, 45), CW)
        self.assertEqual(cartesian_cw_or_ccw(45, -180), CCW)

    def test_cartesian_heading_to_gps(self):
        self.assertEqual(cartesian_heading_to_gps(0), 90)
        self.assertEqual(cartesian_heading_to_gps(90), 0)
        self.assertEqual(cartesian_heading_to_gps(180), -90)
        self.assertEqual(cartesian_heading_to_gps(-90), 180)

    def test_cartesian_to_screen(self):
        # Center
        self.assertEqual(cartesian_to_screen(0, 0), (400, 400))
        # Top right
        self.assertEqual(cartesian_to_screen(400, 400), (800, 0))
        # Bottom left
        self.assertEqual(cartesian_to_screen(-400, -400), (0, 800))

    def test_find_distance(self):
        self.assertAlmostEqual(find_distance((0, 0), (3, 4)), 5.0)
        self.assertAlmostEqual(find_distance((1, 2), (4, 6)), 5.0)

if __name__ == "__main__":
    unittest.main()
