from uuid import uuid4
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()), unique=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role_id = Column(ForeignKey("roles.id"), default=1)
    is_confirmed = Column(Boolean())
    confirmation_sent = Column(DateTime())
    confirmation_date = Column(DateTime())

    role = relationship("Role", back_populates="users")

    def __str__(self):
        return f"Пользователь {self.email}"
    

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)

    users = relationship("Users", back_populates="role")

    def __str__(self):
        return f"{self.name}"
    