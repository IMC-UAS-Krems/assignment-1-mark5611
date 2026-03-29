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
class Track:
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str):
        self.track_id = track_id
        self.title = title
        self.duration_seconds = duration_seconds
        self.genre = genre

    def duration_minutes(self):
        return float(self.duration_seconds) / 60

from streaming.artists import Artist
class Song(Track):
    def __init__(self, artist: Artist, track_id: str, title: str, duration_seconds: int, genre: str):
        super().__init__(track_id, title, duration_seconds, genre)
        self.artist = artist

class SingleRelease(Song):
    def __init__(self, release_date, artist: Artist, track_id: str, title: str, duration_seconds: int, genre: str):
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
    def __init__(self, host: str, description: str, track_id: str, title: str, duration_seconds: int, genre: str):
        super().__init__(track_id, title, duration_seconds, genre)
        self.host = host
        self.description = description

class InterviewEpisode(Podcast):
    def __init__(self, guest: str, host: str, description: str, track_id: str, title: str, duration_seconds: int,
                 genre: str):
        super().__init__(host, description, track_id, title, duration_seconds, genre)
        self.guest = guest

class NarrativeEpisode(Podcast):
    def __init__(self, season: int, episode_number: int, host: str, description: str, track_id: str, title: str,
                 duration_seconds: int, genre: str):
        super().__init__(host, description, track_id, title, duration_seconds, genre)
        self.season = self
        self.episode_number = episode_number

class AudiobookTrack:
    def __init__(self, author: str, narrator: str):
        self.author = author
        self.narrator = narrator