# -*- coding: utf-8 -*-

import os
from phrydy import MediaFile


class Bundler(object):

    def __init__(self, folder):
        self.album = []
        self.album_title = ''
        for root_path, subdirs, files in os.walk(folder):
            subdirs.sort()
            files.sort()

            album_title = ''

            for file in files:
                path = os.path.join(root_path, file)
                if path.lower().endswith((".mp3", ".m4a", ".flac", ".wma")):
                    self.make_bundles(path)

    def make_bundles(self, path):
        media = MediaFile(path)
        record = {}
        record['title'] = media.album
        record['track'] = media.track
        record['path'] = path
        if not self.album_title or self.album_title != media.album:
            self.album_title = media.album
            self.explore_album()
            self.album = []
        self.album.append(record)

    def check_quantity(self, quantity=6):
        if len(self.album) > quantity:
            return True
        else:
            return False

    def check_completeness(self):
        max_track = 0
        for record in self.album:
            if record['track'] > max_track:
                max_track = record['track']

        if len(self.album) == max_track:
            return True
        else:
            return False

    def execute(self):
        for record in self.album:
            print(record['path'])

    def explore_album(self):
        if self.check_quantity() and self.check_completeness():
            self.execute()