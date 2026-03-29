"""
artists.py
----------
Implement the Artist class representing musicians and content creators.

Classes to implement:
  - Artist
"""
from typing import List

from streaming.tracks import Track

class Artist:
    def __init__(self, artist_id: str, name: str, genre: str, tracks: List[Track] = None):
        if tracks is None:
            tracks = []
        self.artist_id = artist_id
        self.name = name
        self.genre = genre
        self.tracks = tracks

    def add_track(self, track: Track):
        self.tracks.append(track)

    def track_count(self):
        return len(self.tracks)