"""Admin use cases."""


class RunMigrationsUseCase:
    def __init__(self, engine):
        self.engine = engine

    def execute(self):
        from infrastructure.migrations import run_migrations
        with self.engine.begin() as conn:
            run_migrations(conn)
        return {"status": "ok", "message": "Migration applied"}
