from dataclasses import dataclass, field
from datetime import date


@dataclass
class Task:
    """Represents a single pet care activity."""
    description: str
    time: str          # "HH:MM" format
    frequency: str     # "once", "daily", or "weekly"
    completed: bool = False
    due_date: date | None = None
    pet_name: str = ""

    def mark_complete(self):
        """Mark this task as done and return the next occurrence if recurring."""
        pass


@dataclass
class Pet:
    """Stores a pet's details and their list of tasks."""
    name: str
    species: str
    breed: str = ""
    age: int = 0
    allergies: str = ""
    medications: str = ""
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's list."""
        pass

    def get_tasks(self) -> list:
        """Return all tasks for this pet."""
        pass


class Owner:
    """Manages multiple pets and provides access to all their tasks."""

    def __init__(self, name: str):
        self.name = name
        self.pets = []

    def add_pet(self, pet: Pet) -> None:
        """Register a pet with this owner."""
        pass

    def get_all_tasks(self) -> list:
        """Collect and return every task across all pets."""
        pass


class Scheduler:
    """The brain: retrieves, organizes, and manages tasks across all pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def sort_by_time(self, tasks=None) -> list:
        """Return tasks sorted chronologically by time."""
        pass

    def filter_tasks(self, pet_name=None, completed=None) -> list:
        """Filter tasks by pet name and/or completion status."""
        pass

    def detect_conflicts(self) -> list:
        """Return warning strings for any tasks sharing the same time slot."""
        pass

    def mark_task_complete(self, task: Task, pet: Pet):
        """Mark a task complete and auto-schedule the next occurrence if recurring."""
        pass

    def get_daily_schedule(self) -> list:
        """Return today's pending tasks sorted by time."""
        pass