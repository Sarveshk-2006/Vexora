from typing import Any

from sqlalchemy.orm import Session as DBSession


class DatabasePersister:
    """Decoupled persistence service for Digital Twin entities."""

    @staticmethod
    def persist(generation_result: Any, db_session: DBSession) -> int:
        """Bulk add and commit generated entities into active SQLAlchemy DB session."""
        total_rows = 0

        db_session.add_all(generation_result.users)
        total_rows += len(generation_result.users)

        db_session.add_all(generation_result.accounts)
        total_rows += len(generation_result.accounts)

        db_session.add_all(generation_result.devices)
        total_rows += len(generation_result.devices)

        db_session.add_all(generation_result.merchants)
        total_rows += len(generation_result.merchants)

        db_session.add_all(generation_result.payment_agents)
        total_rows += len(generation_result.payment_agents)

        db_session.add_all(generation_result.sessions)
        total_rows += len(generation_result.sessions)

        db_session.add_all(generation_result.transactions)
        total_rows += len(generation_result.transactions)

        db_session.commit()
        return total_rows
