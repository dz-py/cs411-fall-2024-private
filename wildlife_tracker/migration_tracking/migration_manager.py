from typing import Optional

from wildlife_tracker.migration_tracking.migration import Migration
from wildlife_tracker.migration_tracking.migration_path import MigrationPath
from wildlife_tracker.habitat_management.habitat import Habitat


class MigrationManager:
    def __init__(self) -> None:
        self.migrations: dict[int, Migration] = {}
        self.migration_paths: dict[int, MigrationPath] = {}

    def get_migration_by_id(self, migration_id: int) -> Optional[Migration]:
        pass

    def schedule_migration(self, migration: Migration) -> None:
        pass

    def cancel_migration(self, migration_id: int) -> None:
        pass

    def update_migration_details(self, migration_id: int, **kwargs) -> None:
        pass

    def create_migration_path(self, migration_path: MigrationPath) -> None:
        pass

    def remove_migration_path(self, path_id: int) -> None:
        pass

    def get_migration_path_by_id(self, path_id: int) -> Optional[MigrationPath]:
        pass

    def get_migrations(self) -> list[Migration]:
        pass

    def get_migrations_by_current_location(self, current_location: str) -> list[Migration]:
        pass

    def get_migrations_by_migration_path(self, migration_path_id: int) -> list[Migration]:
        pass

    def get_migrations_by_start_date(self, start_date: str) -> list[Migration]:
        pass

    def get_migrations_by_status(self, status: str) -> list[Migration]:
        pass

    def get_migration_path_details(self, path_id: str) -> dict:
        pass
