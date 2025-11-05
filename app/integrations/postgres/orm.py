from sqlalchemy import String, ForeignKey, DOUBLE_PRECISION
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass



class CompanyORM(Base):
    __tablename__ = 'companies'

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    building_id: Mapped[int] = mapped_column(
        ForeignKey("buildings.id", ondelete="CASCADE"),
        nullable=False
    )
    building: Mapped["BuildingORM"] = relationship("BuildingORM", back_populates="companies")

    telephones: Mapped[list["TelephoneORM"]] = relationship(
        "TelephoneORM",
        back_populates="company",
        cascade="all, delete-orphan"
    )

    activities: Mapped[list["ActivityORM"]] = relationship(
        "ActivityORM",
        secondary="company_activity_relations",
        back_populates="companies"
    )

class TelephoneORM(Base):
    __tablename__ = "telephones"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    number: Mapped[str] = mapped_column(String(20), nullable=False)

    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"))
    company: Mapped["CompanyORM"] = relationship("CompanyORM", back_populates="telephones")

class BuildingORM(Base):
    __tablename__ = 'buildings'

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    address: Mapped[str] = mapped_column(String(200), nullable=False)
    latitude: Mapped[float] = mapped_column(DOUBLE_PRECISION, nullable=False)
    longitude: Mapped[float] = mapped_column(DOUBLE_PRECISION, nullable=False)

    companies: Mapped[list["CompanyORM"]] = relationship(
        "CompanyORM",
        back_populates="building",
        cascade="all, delete-orphan"
    )


class ActivityORM(Base):
    __tablename__ = 'activities'

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("activities.id"))
    depth: Mapped[int] = mapped_column(nullable=False, default=1)
    parent: Mapped["ActivityORM"] = relationship(
        "ActivityORM",
        remote_side=[id],
        back_populates="children",
    )
    children: Mapped[list["ActivityORM"]] = relationship(
        "ActivityORM",
        back_populates="parent",
        cascade="all, delete-orphan"
    )
    companies: Mapped[list["CompanyORM"]] = relationship(
        "CompanyORM",
        secondary="company_activity_relations",
        back_populates="activities"
    )

class CompanyActivityRelationsORM(Base):
    __tablename__ = "company_activity_relations"

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"),
        primary_key=True
    )
    activity_id: Mapped[int] = mapped_column(
        ForeignKey("activities.id", ondelete="CASCADE"),
        primary_key=True
    )