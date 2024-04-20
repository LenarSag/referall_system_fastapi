from datetime import datetime, timedelta

from sqlalchemy import Column, ForeignKey, Integer, Text, String, DateTime, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, backref


class Base(DeclarativeBase):
    pass


user_referral = Table(
    "user_referral",
    Base.metadata,
    Column(
        "user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "referral_id",
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
    ),
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

    referral: Mapped[list["User"]] = relationship(
        secondary=user_referral,
        primaryjoin=id == user_referral.c.user_id,
        secondaryjoin=id == user_referral.c.referral_id,
        backref=backref("referrals", cascade="all, delete"),
    )


class ReferralCode(Base):
    __tablename__ = "referral_code"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    is_active: Mapped[bool] = mapped_column(default=True, nullable=True)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now() + timedelta(days=30)
    )

    user: Mapped["User"] = relationship("User", back_populates="referral_code")
