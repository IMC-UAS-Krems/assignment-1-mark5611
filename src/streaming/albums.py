"""
albums.py
---------
Implement the Album class for collections of AlbumTrack objects.

Classes to implement:
  - Album
"""
from streaming.tracks import AlbumTrack

class Album:
    def __init__(self, album_id: str, title: str, artist, release_year: int):
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self.tracks = []

    def add_track(self, track: AlbumTrack):
        self.tracks.append(track)

    def track_ids(self):
        track_ids = set()
        for track in self.tracks:
            track_ids.add(track.track_id)
        return track_ids

    def duration_seconds(self):
        duration = 0
        for track in self.tracks:
            duration += track.duration_seconds
        return duration