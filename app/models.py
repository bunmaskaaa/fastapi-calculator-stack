from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    calculations = relationship(
        "Calculation",
        back_populates="user",
        cascade="all, delete-orphan",
    )


from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database import Base


class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    operation = Column(String, nullable=False)

    # IMPORTANT: these names match the DB columns and schemas
    operand_a = Column(Float, nullable=False)
    operand_b = Column(Float, nullable=False)

    result = Column(Float, nullable=False)

    # make them nullable to avoid NOT NULL constraint surprises
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=True,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )

    user = relationship("User", back_populates="calculations")