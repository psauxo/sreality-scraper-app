import logging
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


logger = logging.getLogger(__name__)


class SQLAlchemySessionFactory:
    """
    The SQLAlchemySessionFactory is responsible for creating a new session.
    The session is then used in the database services to execute queries.
    """

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url, echo=True)
        self.Session = sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            class_=Session,
        )

    def create_session(self):
        return self.Session()


@contextmanager
def get_session(session_factory: SQLAlchemySessionFactory) -> Session:
    """
    Context manager that creates a new session and commits the changes.
    If an error occurs, it will rollback the changes.
    If the session is not closed, it will close it.

    :param session_factory: SQLAlchemySessionFactory instance used for creating a new session
    :return: Session instance from SQLAlchemy
    """
    session = session_factory.create_session()
    try:
        logger.info("Creating a new session")
        yield session
        session.commit()
    except Exception as e:
        logger.error("Error while executing database operation: %s", e)
        session.rollback()
        raise e
    finally:
        logger.info("Closing the session")
        session.close()
