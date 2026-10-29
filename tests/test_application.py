# SPDX-License-Identifier: GPL-2.0-only
import json
import tempfile
import unittest
from unittest.mock import Mock

from adapters import jellyfin
from adapters.catalog import Application
from adapters.jellyfin import WINDOW_CLASS, prepare_profile
from services.session.application import ApplicationSession

APP = Application('jellyfin', 'Jellyfin', 'Movies & series',
                  'com.github.iwalton3.jellyfin-mpv-shim', 2)


class ProfileTests(unittest.TestCase):
    def test_existing_preferences_and_credentials_are_unchanged(self):
        with tempfile.TemporaryDirectory() as directory:
            profile = prepare_profile(APP.flatpak_id, directory)
            conf = profile / 'conf.json'
            credentials = profile / 'cred.json'
            # Deliberately preserve the opposite face-button preference too.
            content = json.dumps({'gamepad_swap_confirm': True, 'fullscreen': False})
            conf.write_text(content)
            credentials.write_text('private-placeholder')
            prepare_profile(APP.flatpak_id, directory)
            self.assertEqual(conf.read_text(), content)
            self.assertEqual(credentials.read_text(), 'private-placeholder')

    def test_new_profile_does_not_force_face_button_layout(self):
        with tempfile.TemporaryDirectory() as directory:
            profile = prepare_profile(APP.flatpak_id, directory)
            settings = json.loads((profile / 'conf.json').read_text())
            self.assertNotIn('gamepad_swap_confirm', settings)
            self.assertTrue(settings['input_gamepad'])
            self.assertEqual((profile / 'conf.json').stat().st_mode & 0o777, 0o600)

    def test_custom_mpv_profile_is_never_replaced(self):
        with tempfile.TemporaryDirectory() as directory:
            profile = prepare_profile(APP.flatpak_id, directory)
            mpv = profile / 'mpv.conf'
            custom = 'wayland-app-id=another-profile\n'
            mpv.write_text(custom)
            with self.assertRaises(ValueError):
                prepare_profile(APP.flatpak_id, directory)
            self.assertEqual(mpv.read_text(), custom)


class LifecycleTests(unittest.TestCase):
    def test_last_app_window_close_requests_conditional_home(self):
        hypr = Mock()
        hypr.query.side_effect = [[{'class': WINDOW_CLASS, 'mapped': True}], []]
        session = ApplicationSession(APP, hypr, jellyfin)
        self.assertTrue(session.refresh())
        self.assertFalse(session.refresh())
        hypr.home_if_active.assert_called_once_with(2)

    def test_initial_no_window_is_not_mistaken_for_app_exit(self):
        hypr = Mock()
        hypr.query.return_value = []
        session = ApplicationSession(APP, hypr, jellyfin)
        self.assertTrue(session.refresh())
        hypr.home_if_active.assert_not_called()

    def test_other_app_windows_do_not_keep_jellyfin_session_alive(self):
        hypr = Mock()
        hypr.query.return_value = [{'class': 'another-app', 'mapped': True}]
        session = ApplicationSession(APP, hypr, jellyfin)
        session.seen_window = True
        self.assertFalse(session.refresh())

    def test_reentry_focuses_workspace_and_restores_existing_fullscreen(self):
        hypr = Mock()
        hypr.query.return_value = [{'class': WINDOW_CLASS, 'mapped': True,
                                    'fullscreen': 0, 'address': '0x123'}]
        ApplicationSession(APP, hypr, jellyfin).focus()
        expressions = [c.args[0] for c in hypr.dispatch.call_args_list]
        self.assertIn('workspace=2', expressions[0])
        self.assertIn('address:0x123', expressions[1])
        self.assertIn('action="set"', expressions[1])
        self.assertIn('internal=2,client=0', expressions[1])


if __name__ == '__main__':
    unittest.main()
