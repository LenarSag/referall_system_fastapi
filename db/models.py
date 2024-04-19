from datetime import datetime, timedelta

from sqlalchemy import Column, ForeignKey, Integer, Text, String, DateTime, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


user_referral = Table(
    "user_referral",
    Base.metadata,
    Column("referrer_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("referee_id", Integer, ForeignKey("user.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)

    referral_code: Mapped["ReferralCode"] = relationship(
        "ReferralCode", back_populates="user", cascade="all, delete-orphan"
    )
    referees: Mapped[list["User"]] = relationship(
        "User",
        secondary=user_referral,
        primaryjoin=id == user_referral.c.referrer_id,
        secondaryjoin=id == user_referral.c.referee_id,
        back_populates="referrers",
    )
    referrers: Mapped[list["User"]] = relationship(
        "User",
        secondary=user_referral,
        primaryjoin=id == user_referral.c.referee_id,
        secondaryjoin=id == user_referral.c.referrer_id,
        back_populates="referees",
    )


class ReferralCode(Base):
    __tablename__ = "referral_code"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    expires_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now() + timedelta(days=30)
    )

    user: Mapped["User"] = relationship("User", back_populates="referral_code")
