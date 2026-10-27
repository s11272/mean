from typing import Any

from sqlalchemy import Engine, text


class DbClient:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def fetch_one(
        self, query: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any] | None:
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            row = result.mappings().first()
            return dict(row) if row else None

    def fetch_all(
        self, query: str, params: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            return [dict(r) for r in result.mappings().all()]

    def execute(
        self, query: str, params: dict[str, Any] | None = None
    ) -> None:
        with self.engine.begin() as conn:
            conn.execute(text(query), params or {})