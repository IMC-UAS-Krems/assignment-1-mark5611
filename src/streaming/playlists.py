"""
playlists.py
------------
Implement playlist classes for organizing tracks.

Classes to implement:
  - Playlist
    - CollaborativePlaylist
"""
from streaming.users import User
from streaming.tracks import Track

class Playlist:
    def __init__(self, playlist_id: str, name: str, owner: User, tracks: list[Track]):
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks = tracks

    def add_track(self, track: Track):
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
    def __init__(self, contributors: list[User], playlist_id: str, name: str, owner: User, tracks: list[Track]):
        super().__init__(playlist_id, name, owner, tracks)
        self.contributors = contributors

    def add_contributor(self, user):
        self.contributors.append(user)

    def remove_contributor(self, user):
        self.contributors.remove(user)