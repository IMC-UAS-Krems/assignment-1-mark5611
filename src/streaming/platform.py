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
    def __init__(self, name: str, session: Optional[List[ListeningSession]] = None):
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
        lt = end - start
        if not self._sessions:
            return 0.0
        else:
            return float(lt.total_seconds()/60)

    def avg_unique_tracks_per_premium_user(self, days = 30):
        avg_u_track = []
        pu = 0
        if PremiumUser not in self._users:
            return 0.0
        else:
            for user in self._users:
                if user is PremiumUser:
                    pu += 1
                    for session in self._sessions:
                        if session.timestamp > datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(days=days):
                            avg_u_track.append(user.unique_tracks_listened())
        return len(set(avg_u_track)) / pu


    def track_with_most_distinct_listeners(self):
        dt = {}
        if not self._users:
            return None
        else:
            for key, user in self._users.items():
                for tracks in user.unique_tracks_listened():
                    if tracks in dt.keys():
                        dt[tracks] += 1
                    else:
                        dt[tracks] = 1
        print(max(dt)[0])
        return max(dt)[0]



    def avg_session_duration_by_user_type(self):
        asdbut = []
        userTypes = [FreeUser, PremiumUser, FamilyAccountUser, FamilyMember]
        for type in userTypes:
            typeDuration = 0
            tu = 0
            for key, user in self._users.items():
                if user is type:
                    typeDuration += user.total_listening_seconds()
                    tu += 1
            if tu == 0:
                asdbut.append((str(type), 0.0))
            else:
                asdbut.append((str(type), typeDuration/tu))
        return asdbut

    def total_listening_time_underage_sub_users_minutes(self):
        total_listening_time = 0.0
        for user in self._users:
            if user is FamilyMember and user.age < 18:
                total_listening_time += user.total_listening_minutes()
        return total_listening_time

    def top_artists_by_listening_time(self, n: int = 5):
        top_songs = {}
        top_artists = {}
        list = []
        for session in self._sessions:
            Ctrack = session.track
            if isinstance(Ctrack, Song):
                if Ctrack in top_songs.keys():
                    top_songs[Ctrack] += Ctrack.duration_minutes()
                else:
                    top_songs[Ctrack] = Ctrack.duration_minutes()
        sorted_songs = sorted(top_songs)[:n]
        for artist in self._artists:
            for song in sorted_songs:
                if song in artist.tracks:
                    top_artists[artist] = top_songs.get(song)

        for artist, duration in top_artists.items():
            list.append((artist, duration))
        return list

    def user_top_genre(self, userid: str):
        top_genre = {}
        unique_tracks = []
        sum_time = 0
        tries = 0
        for key, user in self._users.items():
            if user.user_id == userid:
                unique_tracks = user.unique_tracks_listened()
                sum_time = user.total_listening_minutes()
                break
            tries += 1

        for track in unique_tracks:
            top_genre[track.genre] = track.duration_seconds

        most_listened_genre = sorted(top_genre)[:1]
        if most_listened_genre != []:
            return (most_listened_genre, sum_time)
        else:
            return None


    def collaborative_playlists_with_many_artists(self, threshold: int = 3):
        tracks_and_artists = {}
        good = []
        for playlist in self._playlists:
            if isinstance(playlist, CollaborativePlaylist):
                for track in playlist.tracks:
                    if isinstance(track, Song):
                        for artist in self._artists:
                            if track in artist.tracks:
                                tracks_and_artists[track] += 1

        for key, value in tracks_and_artists.items():
            if value >= threshold:
                good.append(key)
        return good

    def avg_tracks_per_playlist_type(self):
        sumPlaylists = 0.0
        avg = {"Playlist": 0.0, "CollaborativePlaylist": 0.0}
        for playlist in self._playlists:
            tracks = 0
            if isinstance(playlist, Playlist):
                for track in playlist.tracks:
                    sumPlaylists += 1.0
                    tracks += 1.0
                avg["Playlist"] += tracks
            elif isinstance(playlist, CollaborativePlaylist):
                for track in playlist.tracks:
                    sumPlaylists += 1.0
                    tracks += 1.0
                avg["CollaborativePlaylist"] += tracks

        for key, value in avg.items():
            if value != 0.0:
                avg[key] = sumPlaylists / value

        return avg

    def users_who_completed_albums(self):
        completed = []
        for userId, user in self._users.items():
            if isinstance(user, User):
                userUniqueTracks = list(user.unique_tracks_listened())
                print(userUniqueTracks)
                for albumId, album in self._albums.items():
                    if isinstance(album, Album):
                        if album.tracks in userUniqueTracks and album.tracks != []:
                            completed.append((user,[album.title, album.release_year]))

        completed = sorted(completed, key= lambda x:x[1][1])
        return completed