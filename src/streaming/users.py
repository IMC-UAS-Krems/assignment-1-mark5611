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
from typing import List
from streaming.sessions import ListeningSession

class User:

    def __init__(self, user_id: str, name: str, age: int):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = []

    def add_session(self, session: ListeningSession):
        self.sessions.append(session)

    def total_listening_seconds(self):
        tls = 0


class FreeUser(User):
    def __init__(self, user_id: str, name: str, age: int):
        super().__init__(user_id, name, age)
        self.MAX_SKIPS_PsER_HOUR = 6

class PremiumUser(User):
    def __init__(self, user_id: str, name: str, age: int, subscription_start):
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start

class FamilyAccountUser(User):
    def __init__(self, sub_users: list, user_id: str, name: str, age: int):
        super().__init__(user_id, name, age, )
        self.sub_users = sub_users

    def add_sub_user(self, sub_user):
        self.sub_users.append(sub_user)

    def all_members(self):
        return self.sub_users


class FamilyMember(User):
    def __init__(self, family_account_user: FamilyAccountUser, user_id: str, name: str, age: int):
        super().__init__(user_id, name, age)
        self.familyAccountUser = family_account_user
