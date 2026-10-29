# SPDX-License-Identifier: GPL-2.0-only
import unittest
from evdev import ecodes as E
from services.session.gamepad import Navigation


class NavigationTests(unittest.TestCase):
    def pad(self, vendor=0x057E):
        pad = Navigation(vendor, {E.ABS_X: (0, 255), E.ABS_Y: (0, 255)})
        pad.set_focus(True)
        return pad

    def test_nintendo_physical_a_and_b(self):
        pad = self.pad()
        self.assertEqual(pad.feed(E.EV_KEY, E.BTN_EAST, 1, 0), "select")
        self.assertEqual(pad.feed(E.EV_KEY, E.BTN_SOUTH, 1, 0), "back")

    def test_standard_south_confirm_east_back(self):
        pad = self.pad(vendor=0x045E)
        self.assertEqual(pad.feed(E.EV_KEY, E.BTN_SOUTH, 1, 0), "select")
        self.assertEqual(pad.feed(E.EV_KEY, E.BTN_EAST, 1, 0), "back")

    def test_press_has_one_action_and_release_rearms(self):
        pad = self.pad()
        self.assertEqual(pad.feed(E.EV_KEY, E.BTN_EAST, 1, 0), "select")
        self.assertIsNone(pad.feed(E.EV_KEY, E.BTN_EAST, 1, 1))
        self.assertIsNone(pad.feed(E.EV_KEY, E.BTN_EAST, 2, 2))
        self.assertIsNone(pad.feed(E.EV_KEY, E.BTN_EAST, 0, 3))
        self.assertEqual(pad.feed(E.EV_KEY, E.BTN_EAST, 1, 4), "select")

    def test_repeat_delay_and_release(self):
        pad = self.pad()
        self.assertEqual(pad.feed(E.EV_ABS, E.ABS_HAT0X, 1, 0), "next")
        self.assertIsNone(pad.repeat(0.39))
        self.assertEqual(pad.repeat(0.4), "next")
        self.assertIsNone(pad.repeat(0.5))
        self.assertEqual(pad.repeat(0.56), "next")
        pad.feed(E.EV_ABS, E.ABS_HAT0X, 0, 0.6)
        self.assertIsNone(pad.repeat(1))

    def test_focus_loss_blocks_all_actions_and_cancels_repeat(self):
        pad = self.pad()
        pad.feed(E.EV_ABS, E.ABS_HAT0X, 1, 0)
        pad.set_focus(False)
        self.assertIsNone(pad.repeat(1))
        self.assertIsNone(pad.feed(E.EV_KEY, E.BTN_EAST, 1, 1))
        pad.set_focus(True)
        self.assertIsNone(pad.repeat(2))
        self.assertIsNone(pad.feed(E.EV_ABS, E.ABS_HAT0X, 1, 2))
        self.assertIsNone(pad.feed(E.EV_KEY, E.BTN_EAST, 1, 2))
        pad.feed(E.EV_ABS, E.ABS_HAT0X, 0, 3)
        self.assertEqual(pad.feed(E.EV_ABS, E.ABS_HAT0X, -1, 4), "previous")

    def test_unsigned_stick_deadzone_and_direction(self):
        pad = self.pad()
        self.assertIsNone(pad.feed(E.EV_ABS, E.ABS_X, 128, 0))
        self.assertIsNone(pad.feed(E.EV_ABS, E.ABS_X, 150, 0))
        self.assertEqual(pad.feed(E.EV_ABS, E.ABS_X, 255, 1), "next")
        self.assertEqual(pad.feed(E.EV_ABS, E.ABS_X, 0, 2), "previous")
        self.assertIsNone(pad.feed(E.EV_ABS, E.ABS_X, 128, 3))
        self.assertIsNone(pad.repeat(4))

    def test_short_home_press_does_not_return_home(self):
        pad = self.pad()
        self.assertIsNone(pad.feed(E.EV_KEY, E.BTN_MODE, 1, 0))
        self.assertIsNone(pad.repeat(4.99))
        pad.feed(E.EV_KEY, E.BTN_MODE, 0, 4.99)
        self.assertIsNone(pad.repeat(5.1))

    def test_held_home_returns_once_while_app_has_focus(self):
        pad = self.pad()
        pad.set_focus(False)
        pad.feed(E.EV_KEY, E.BTN_MODE, 1, 0)
        self.assertIsNone(pad.repeat(4.99))
        self.assertEqual(pad.repeat(5), "home")
        self.assertIsNone(pad.repeat(10))
        pad.feed(E.EV_KEY, E.BTN_MODE, 0, 11)
        pad.feed(E.EV_KEY, E.BTN_MODE, 1, 12)
        self.assertEqual(pad.repeat(17), "home")

    def test_stream_quit_buttons_have_no_home_action(self):
        pad = self.pad()
        for code in (E.BTN_TL, E.BTN_TR, E.BTN_SELECT, E.BTN_START):
            self.assertIsNone(pad.feed(E.EV_KEY, code, 1, 0))


if __name__ == "__main__":
    unittest.main()
