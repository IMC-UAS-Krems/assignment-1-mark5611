"""
users.py
--------
Implement the class hierarchy for platform users.

Classes to implement:
  - User (base class)
    - FreeUser
    - PremiumUser
    - FamilyAccountUser
    - FamilyMember
"""
from streaming.sessions import ListeningSession
from typing import List, Optional

class User:

    def __init__(self, user_id: str, name: str, age: int, session: Optional[List[ListeningSession]] = None):
        if session is None:
            session = []
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = session

    def add_session(self, session: ListeningSession):
        if session not in self.sessions:
            self.sessions.append(session)

    def total_listening_seconds(self):
        tls = 0
        for session in self.sessions:
            if isinstance(session, ListeningSession):
                tls += session.duration_listened_seconds
        return tls

    def total_listening_minutes(self):
        return self.total_listening_seconds()/60

    def unique_tracks_listened(self):
        ut = []
        for session in self.sessions:
            if isinstance(session, ListeningSession):
                ut.append(session.track.track_id)
        return set(ut)

class FreeUser(User):
    def __init__(self, user_id: str, name: str, age: int):
        super().__init__(user_id, name, age)
        self.MAX_SKIPS_PER_HOUR = 6

class PremiumUser(User):
    def __init__(self, user_id: str, name: str, age: int, subscription_start):
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start

class FamilyAccountUser(User):
    def __init__(self, user_id: str, name: str = None, age: int = None, sub_users: Optional[List[User]] = None):
        super().__init__(user_id, name, age)
        if sub_users is None:
            sub_users = []
        self.sub_users = sub_users

    def add_sub_user(self, sub_user):
        self.sub_users.append(sub_user)

    def all_members(self):
        return [self] + self.sub_users


class FamilyMember(User):
    def __init__(self, user_id: str, name: str, age: int, parent: FamilyAccountUser):
        super().__init__(user_id, name, age)
        self.parent = parent
