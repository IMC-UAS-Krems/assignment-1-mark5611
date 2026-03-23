"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
import datetime

from streaming.albums import Album
from streaming.playlists import Playlist
from streaming.sessions import ListeningSession
from streaming.tracks import Track
from streaming.users import User, PremiumUser
from streaming.artists import Artist


class StreamingPlatform:
    def __init__(self, name: str):
        self.name = name
        self._catalogue = {}
        self._users = {}
        self._artists = {}
        self._albums = {}
        self._playlists = {}
        self._sessions = []

    def add_track(self, track: Track):
        self._catalogue[str(len(self._catalogue)+1)] = track

    def add_user(self, user: User):
        self._users[str(len(self._users)+1)] = user

    def add_artist(self, artist: Artist):
        self._artists[str(len(self._artists)+1)] = artist

    def add_album(self, album: Album):
        self._albums[str(len(self._albums)+1)] = album

    def add_playlist(self, playlist: Playlist):
        self._playlists[str(len(self._playlists)+1)] = playlist

    def record_session(self, session: ListeningSession):
        self._sessions.append(session)

    def get_track(self, track_id):
        for key, track in self._catalogue.items():
            if track.track_id == track_id:
                return track
        return None

    def get_user(self, user_id):
        for key, user in self._users.items():
            if user.user_id == user_id:
                return user
        return None

    def get_artist(self, artist_id):
        for key, artist in self._artists.items():
            if artist.artist_id == artist_id:
                return artist
        return None

    def get_album(self, album_id):
        for key, album in self._albums.items():
            if album.album_id == album_id:
                return album
        return None

    def all_users(self):
        users = []
        for key, user in self._users.items():
            users.append(user)
        return users

    def all_tracks(self):
        tracks = []
        for key, track in self._catalogue.items():
            tracks.append(track)
        return tracks

    def total_listening_time_minutes(self, start: datetime.timedelta, end: datetime.timedelta):
        lt = end - start
        if not self._sessions:
            return 0.0
        else:
            return float(lt.total_seconds()/60)

    def avg_unique_tracks_per_premium_user(self, days = 30):
        premium_users = []
        if PremiumUser not in self._users:
            return 0.0
        else:
            for user in self._users:
                for k, playlist in self._playlists.items():
                    if playlist.owner == user:
                        pass




    def track_with_most_distinct_listeners(self):
        if not self._users:
            return None
        return None

    def avg_session_duration_by_user_type(self):
        for Id, user in self._users.items():
            if user is PremiumUser:
                return ("a", "b")
