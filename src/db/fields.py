from uuid import uuid4
from sqlmodel import Field, Column, DateTime, text, UUID, func


# Get timestamp (utc zone) from database.
utc_now = text("TIMEZONE('utc', now())")
gen_random_uuid = text("gen_random_uuid()")

def uuid4_pk():
    """Return uuid4 primary key field."""
    return Field(
        default_factory=uuid4, 
        sa_column=Column(
            UUID,
            primary_key=True,
            server_default=gen_random_uuid,
            nullable=False
        )
    )

def created_at():
    """Return created_at field."""
    return Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), 
            server_default=utc_now, 
            nullable=False
        ),
    )


def updated_at():
    """Return updated_at field."""
    return Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), 
            onupdate=utc_now,
            nullable=True
            ),
    )
    
def deleted_at():
    """Return deleted_at field."""
    return Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), 
            nullable=True
            ),
    )
    
def timezone_column():
    """Return timezone column."""
    return Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), 
            nullable=True
            ),
    )
    