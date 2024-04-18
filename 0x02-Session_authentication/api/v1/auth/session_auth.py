#!/usr/bin/env python3
"""
A class SessionAuth that inherits from Auth
"""
from uuid import uuid4
from flask import request

from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    The class instantions
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        An instance method
        tht creates a Session ID for a user_id
        Args:
            user_id:

        Returns:
            str:
        """
        if type(user_id) is str:
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a User ID based on a Session ID:
        Args:
            session_id:

        Returns:
            str:
        """
        if type(session_id) is str:
            return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """
        Returns the User ID based on a Session ID:
        Args:
            request:

        Returns:
            User:
        """
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Destroys the user session / logout:
        Args:
            request:

        Returns:
            bool:
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if (request is None or session_id is None) or user_id is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True
