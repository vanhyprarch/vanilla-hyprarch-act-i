# SPDX-License-Identifier: GPL-2.0-only
import unittest
from unittest.mock import Mock
from services.session.window_actions import close_active_window


class CloseWindowTests(unittest.TestCase):
    def window(self, **values):
        return dict({'address':'0x123', 'class':'org.example.AnyApplication',
                     'workspace':{'id':4}}, **values)

    def test_unknown_application_uses_graceful_close_and_returns_home(self):
        hypr = Mock()
        hypr.query.return_value = self.window()
        self.assertTrue(close_active_window(hypr))
        hypr.dispatch.assert_called_once_with('hl.dsp.window.close({window="address:0x123"})')
        hypr.home_if_active.assert_called_once_with(4)

    def test_home_workspace_is_protected(self):
        hypr = Mock()
        hypr.query.return_value = self.window(workspace={'id':1})
        self.assertFalse(close_active_window(hypr))
        hypr.dispatch.assert_not_called()

    def test_launcher_is_protected_even_if_moved(self):
        hypr = Mock()
        hypr.query.return_value = self.window(**{'class':'org.quickshell'})
        self.assertFalse(close_active_window(hypr))
        hypr.dispatch.assert_not_called()

    def test_empty_workspace_does_not_close_other_apps(self):
        hypr = Mock()
        hypr.query.return_value = {}
        self.assertFalse(close_active_window(hypr))
        hypr.dispatch.assert_not_called()
