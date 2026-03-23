"""
sessions.py
-----------
Implement the ListeningSession class for recording listening events.

Classes to implement:
  - ListeningSession
"""

from streaming.tracks import Track

class ListeningSession:
    def __init__(self, session_id: str, user, track: Track, timestamp, duration_listened_seconds: int):
        self.session_id = session_id
        self.user = user
        self.track= track
        self.timestamp = timestamp
        self.duration_listened_seconds = duration_listened_seconds

    def duration_listened_minutes(self):
        return float(self.duration_listened_seconds) / 60