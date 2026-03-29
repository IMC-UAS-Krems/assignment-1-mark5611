"""
playlists.py
------------
Implement playlist classes for organizing tracks.

Classes to implement:
  - Playlist
    - CollaborativePlaylist
"""
from typing import Optional, List

from streaming.users import User
from streaming.tracks import Track

class Playlist:
    def __init__(self, playlist_id: str, name: str, owner: User, tracks: Optional[List[Track]] = None):
        if tracks is None:
            tracks = []
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks = tracks

    def add_track(self, track):
        if track not in self.tracks:
            self.tracks.append(track)

    def remove_track(self, track_id):
        for track in self.tracks:
            if track.track_id == track_id:
                self.tracks.remove(track)
                break

    def total_duration_seconds(self):
        duration = 0
        for track in self.tracks:
            duration+= track.duration_seconds
        return duration

class CollaborativePlaylist(Playlist):
    def __init__(self, playlist_id: str = None, name: str = None, owner: User = None, tracks: Optional[List[Track]] = None, contributors: Optional[List[User]] = None):
        super().__init__(playlist_id, name, owner, tracks)
        if contributors is None:
            contributors = []
        contributors.append(owner)
        self.contributors = contributors

    def add_contributor(self, user):
        if user not in self.contributors:
            self.contributors.append(user)

    def remove_contributor(self, user):
        if user != self.owner:
            self.contributors.remove(user)