# SPDX-License-Identifier: GPL-2.0-only
import unittest
from adapters.catalog import Application
from services.session.workspaces import target_workspace

APPS = [Application('jellyfin','Jellyfin','Media','org.example.Jellyfin',2,'jellyfin'),
        Application('moonlight','Moonlight','Games','org.example.Moonlight',3,'moonlight')]
CLIENTS = [{'class':'jellyfin','mapped':True,'workspace':{'id':2}},
           {'class':'moonlight','mapped':True,'workspace':{'id':3}}]


class WorkspaceTests(unittest.TestCase):
    def test_cycle_open_apps_in_both_directions(self):
        self.assertEqual(target_workspace('next', APPS, CLIENTS, 2), 3)
        self.assertEqual(target_workspace('previous', APPS, CLIENTS, 2), 3)
        self.assertEqual(target_workspace('next', APPS, CLIENTS, 3), 2)

    def test_home_chooses_first_or_last_open_app(self):
        self.assertEqual(target_workspace('next', APPS, CLIENTS, 1), 2)
        self.assertEqual(target_workspace('previous', APPS, CLIENTS, 1), 3)

    def test_closed_apps_are_skipped_without_launch(self):
        self.assertEqual(target_workspace('next', APPS, CLIENTS[:1], 2), 2)
        self.assertEqual(target_workspace('previous', APPS, CLIENTS[:1], 1), 2)
        self.assertEqual(target_workspace('next', APPS, [], 1), 1)

    def test_unmapped_and_unrelated_windows_are_excluded(self):
        clients = [{'class':'moonlight','mapped':False,'workspace':{'id':3}},
                   {'class':'another','mapped':True,'workspace':{'id':2}}]
        self.assertEqual(target_workspace('next', APPS, clients, 3), 1)

    def test_home_always_returns_workspace_one(self):
        self.assertEqual(target_workspace('home', APPS, CLIENTS, 3), 1)
