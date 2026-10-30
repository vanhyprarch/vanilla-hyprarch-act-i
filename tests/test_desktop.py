# SPDX-License-Identifier: GPL-2.0-only
import unittest
import asyncio
import io
import subprocess
from unittest.mock import Mock, AsyncMock, patch
from adapters.catalog import Application
from services.session.desktop import DesktopMonitor

APP = Application('jellyfin','Jellyfin','Media','org.example.Jellyfin',2,'jellyfin')
WINDOW = {'address':'0x123','class':'jellyfin','mapped':True,'workspace':{'id':2}}


class DesktopFocusTests(unittest.TestCase):
    def run_refresh(self, workspace, active, clients=None):
        hypr = Mock()
        data = {'activeworkspace':{'id':workspace}, 'clients':clients or [WINDOW], 'activewindow':active}
        hypr.query.side_effect = data.__getitem__
        callback = Mock()
        DesktopMonitor(hypr,[APP],callback).refresh()
        return hypr, callback

    def test_missing_player_focus_is_repaired_without_workspace_switch(self):
        hypr, callback = self.run_refresh(2,{})
        hypr.dispatch.assert_called_once_with('hl.dsp.focus({window="address:0x123"})')
        callback.assert_called_once_with(2)

    def test_window_recreation_keeps_same_workspace_policy(self):
        hypr, callback = self.run_refresh(2,{})
        callback.assert_called_once_with(2)
        self.assertNotIn('workspace=',hypr.dispatch.call_args.args[0])

    def test_home_does_not_activate_background_player(self):
        hypr, callback = self.run_refresh(1,{'address':'0xhome','workspace':{'id':1}})
        hypr.dispatch.assert_not_called()
        callback.assert_called_once_with(1)

    def test_valid_focused_dialog_is_not_overridden(self):
        hypr, _ = self.run_refresh(2,{'address':'0xdialog','workspace':{'id':2}})
        hypr.dispatch.assert_not_called()

    def test_stale_other_workspace_focus_is_repaired(self):
        hypr, _ = self.run_refresh(2,{'address':'0xhome','workspace':{'id':1}})
        hypr.dispatch.assert_called_once()


class DesktopPolicyRecoveryTests(unittest.TestCase):
    def test_workspace_policy_runs_before_optional_focus_query_failure(self):
        hypr = Mock()
        hypr.query.side_effect = [{'id': 1}, OSError('transient clients query failure')]
        callback = Mock()
        monitor = DesktopMonitor(hypr, [APP], callback)
        with self.assertRaises(OSError):
            monitor.refresh()
        callback.assert_called_once_with(1)


class DesktopConnectionRecoveryTests(unittest.IsolatedAsyncioTestCase):
    async def test_transient_ipc_failure_reconnects_and_is_reported(self):
        for error in (OSError('closed socket'), ValueError('invalid transient JSON'),
                      subprocess.TimeoutExpired('hyprctl', 5)):
            with self.subTest(error=type(error).__name__):
                monitor = DesktopMonitor(Mock(), [APP], Mock())
                monitor._watch = AsyncMock(side_effect=[error, asyncio.CancelledError()])
                output = io.StringIO()
                with patch('services.session.desktop.asyncio.sleep', new_callable=AsyncMock) as delay, \
                        patch('sys.stderr', output):
                    with self.assertRaises(asyncio.CancelledError):
                        await monitor.run()
                self.assertEqual(monitor._watch.await_count, 2)
                delay.assert_awaited_once_with(1)
                self.assertIn('Workspace monitor unavailable', output.getvalue())

    async def test_clean_stream_eof_reconnects(self):
        monitor = DesktopMonitor(Mock(), [APP], Mock())
        monitor._watch = AsyncMock(side_effect=[None, asyncio.CancelledError()])
        with patch('services.session.desktop.asyncio.sleep', new_callable=AsyncMock) as delay, \
                patch('sys.stderr', new_callable=io.StringIO) as output:
            with self.assertRaises(asyncio.CancelledError):
                await monitor.run()
        self.assertEqual(monitor._watch.await_count, 2)
        delay.assert_awaited_once_with(1)
        self.assertIn('event stream closed', output.getvalue())
