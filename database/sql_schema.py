from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Flat(Base):
    __tablename__ = "flats"

    id = Column(UUID, primary_key=True)
    title = Column(String, nullable=False)
    image_url = Column(String, nullable=True)

    def __repr__(self):
        return f"<Flat(title={self.title}, image_url={self.image_url})>"
