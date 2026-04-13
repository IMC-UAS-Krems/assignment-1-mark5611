"""
tracks.py
---------
Implement the class hierarchy for all playable content on the platform.

Classes to implement:
  - Track (abstract base class)
    - Song
      - SingleRelease
      - AlbumTrack
    - Podcast
      - InterviewEpisode
      - NarrativeEpisode
    - AudiobookTrack
"""
from abc import ABC

class Track(ABC):
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str):
        self.track_id = track_id
        self.title = title
        self.duration_seconds = duration_seconds
        self.genre = genre

    def duration_minutes(self):
        return float(self.duration_seconds) / 60

    def __eq__(self, track):
        if isinstance(track, Track):
            return self.track_id == track.track_id
        return False

from streaming.artists import Artist
class Song(Track):
    def __init__(self, artist: Artist, track_id: str, title: str, duration_seconds: int, genre: str):
        super().__init__(track_id, title, duration_seconds, genre)
        self.artist = artist

class SingleRelease(Song):
    def __init__(self, artist: Artist, track_id: str, title: str, duration_seconds: int, genre: str, release_date):
        super().__init__(artist, track_id, title, duration_seconds, genre)
        self.release_date = release_date

class AlbumTrack(Song):
    from streaming.albums import Album
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, artist: Artist, track_number: int,
                 album: Album | None = None):
        super().__init__(artist, track_id, title, duration_seconds, genre)
        self.track_number = track_number
        self.album = album

class Podcast(Track):
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, host: str = None, description: str  = ""):
        super().__init__(track_id, title, duration_seconds, genre)
        self.host = host
        self.description = description

class InterviewEpisode(Podcast):
    def __init__(self, guest: str, host: str, track_id: str, title: str, duration_seconds: int,
                 genre: str, description: str = ""):
        super().__init__(track_id, title, duration_seconds, genre, host, description)
        self.guest = guest

class NarrativeEpisode(Podcast):
    def __init__(self, season: int, episode_number: int, host: str, track_id: str, title: str,
                 duration_seconds: int, genre: str, description: str = ""):
        super().__init__(track_id, title, duration_seconds, genre, host, description)
        self.season = season
        self.episode_number = episode_number

class AudiobookTrack(Track):
    def __init__(self, author: str, narrator: str, track_id: str, title: str, duration_seconds: int, genre: str):
        super().__init__(track_id, title, duration_seconds, genre)
        self.author = author
        self.narrator = narrator