#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user to the DB

        Args:
            email: email of the user
            hashed_password: hashed password of the user
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user in the database based on the provided query arguments

        Args:
            **kwargs: Arbitrary keyword arguments rep query filters

        Returns:
            User: The first user matching the query

        Raises:
            NoResultFound: If no results are found.
            InvalidRequestError: If wrong query arguments are passed
        """
        if not kwargs:
            raise InvalidRequestError

        results = self._session.query(User).filter_by(**kwargs).first()
        if not results:
            raise NoResultFound

        return results

    def update_user(self, user_id: int, **kwargs):
        """
        Update a user in the DB  based on user_id

        Args:
            user_id: ID of the user to update
            **kwargs: keyword arguments rep updated attr

        Returns:
            None

        Raises:
            NoResultFound: If no user for the given user_id
            ValueError: If an invalid attribute is passed in kwargs
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if hasattr(User, key):
                setattr(user, key, value)
            else:
                raise ValueError

        self._session.commit()
