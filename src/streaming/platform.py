"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
import datetime
from typing import Optional, List

from streaming.albums import Album
from streaming.playlists import Playlist, CollaborativePlaylist
from streaming.sessions import ListeningSession
from streaming.tracks import Track, Song
from streaming.users import User, PremiumUser, FreeUser, FamilyAccountUser, FamilyMember
from streaming.artists import Artist


class StreamingPlatform:
    def __init__(self, name: str, session: List[ListeningSession] = None):
        if session is None:
            session = []
        self.name = name
        self._catalogue = {}
        self._users = {}
        self._artists = {}
        self._albums = {}
        self._playlists = {}
        self._sessions = session

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
        total_minutes = 0.0

        for session in self._sessions:
            if start <= session.timestamp >= end:
                total_minutes += session.duration_listened_seconds / 60

        return total_minutes

    def avg_unique_tracks_per_premium_user(self, days = 30):
        tracks = set()

        premium_users = []
        for key, user in self._users.items():
            if isinstance(user, PremiumUser):
                premium_users.append(user)

        if not premium_users or len(self._sessions) == 0:
            return 0.0

        max_back = datetime.date.today() - datetime.timedelta(days=days)

        all_tracks = 0
        for session in self._sessions:
            for tracks in session.track:
                all_tracks += 1

        for Puser in premium_users:
            for session in self._sessions:
                if session.timestamp >= max_back and session.user == Puser:
                    tracks.add(session.track)

        return len(tracks)/all_tracks



    def track_with_most_distinct_listeners(self):
        if len(self._sessions) == 0:
            return None

        tracks = {}

        for session in self._sessions:
            track = session.track
            if track not in tracks.keys():
                tracks[track] = 1
            else:
                tracks[track] += 1

        return sorted(tracks.items(),key= lambda x:x[1], reverse=False)[0][0]


    def avg_session_duration_by_user_type(self):

        final = []
        by_user_type = {}
        total = 0

        for session in self._sessions:
            user_type = session.user.__name__
            dur = session.duration_listened_seconds
            total += dur
            if user_type not in by_user_type.keys():
                by_user_type[user_type] = dur
            else:
                by_user_type[user_type] += dur

        for type, duration in by_user_type.items():
            final.append((type, duration))

        return final

    def total_listening_time_underage_sub_users_minutes(self, age_threshold = 18):
        total_listening_time = 0.0
        for key, user in self._users.items():
            if isinstance(user, FamilyMember) and user.age < age_threshold:
                total_listening_time += user.total_listening_minutes()
        return total_listening_time

    def top_artists_by_listening_time(self, n: int = 5):
        top_artists = {}
        final = []

        for session in self._sessions:
            track = session.track
            if isinstance(track, Song):
                artist = track.artist
                if artist not in top_artists.keys():
                    top_artists[artist] = session.duration_listened_seconds
                else:
                    top_artists[artist] += session.duration_listened_seconds

        for artist, listening_time in top_artists.items():
            final.append((artist, listening_time))

        return final[:n]

    def user_top_genre(self, user_id: str):

        top_listen = {}
        final = None
        total_time = 0

        if len(self._users) == 0:
            return None

        fuser = None
        for key, user in self._users.items():
            if user.user_id == user_id:
                fuser = user

        for session in self._sessions:
            if session.user == fuser:
                total_time += session.duration_listened_seconds
                track = session.track
                genre = track.genre
                if genre not in top_listen.keys():
                    top_listen[genre] = session.duration_listened_seconds
                else:
                    top_listen[genre] += session.duration_listened_seconds

        if len(top_listen) == 0:
            return None
        else:
            final = (max(top_listen.items(), key=lambda x:x[1]))
            return final[0], final[1] / total_time



    def collaborative_playlists_with_many_artists(self, threshold: int = 3):
        playlistsl = []

        for key, playlist in self._playlists.items():
            if isinstance(playlist, CollaborativePlaylist):
                if len(playlist.contributors) >= threshold:
                    playlistsl.append(playlist)

        return playlistsl


    def avg_tracks_per_playlist_type(self):

        by_playlists = {
            "Playlist": 0.0,
            "CollaborativePlaylist": 0.0
        }
        playlists = 0.0
        collabs = 0.0


        for key, playlist in self._playlists.items():
            tracks_num = len(playlist.tracks)
            if type(playlist) == Playlist:
                playlist += 1
                by_playlists["Playlist"] += tracks_num
            elif isinstance(playlist, CollaborativePlaylist):
                collabs += 1
                by_playlists["CollaborativePlaylist"] += tracks_num

        for type, tracks in by_playlists.items():
            if type == "Playlist":
                if playlists == 0:
                    by_playlists[type] = 0.0
                else:
                    by_playlists[type] = tracks/playlists
            else:
                if collabs == 0:
                    by_playlists[type] = 0.0
                else:
                    by_playlists[type] = tracks / collabs

        return  by_playlists

    def users_who_completed_albums(self):

        final = []

        for key, user in self._users.items():
            users_tracks = set()

            for session in self._sessions:
                if session.user == user:
                    users_tracks.add(session.track)

            for key, album in self._albums.items():
                albumtracks = set()
                for track in album.tracks:
                    albumtracks.add(track.track_id)
                if albumtracks.issubset(users_tracks):
                    final.append(user)
        return final