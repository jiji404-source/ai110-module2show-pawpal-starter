from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, time as dt_time, timedelta


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
        """Mark this task done and return a new Task for the next occurrence if daily or weekly, otherwise None."""
        self.completed = True
        base = self.due_date or date.today()
        if self.frequency == "daily":
            return Task(self.description, self.time, self.frequency,
                        due_date=base + timedelta(days=1), pet_name=self.pet_name)
        if self.frequency == "weekly":
            return Task(self.description, self.time, self.frequency,
                        due_date=base + timedelta(weeks=1), pet_name=self.pet_name)
        return None


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
        task.pet_name = self.name
        self.tasks.append(task)

    def get_tasks(self) -> list:
        """Return all tasks for this pet."""
        return self.tasks


class Owner:
    """Manages multiple pets and provides access to all their tasks."""

    def __init__(self, name: str):
        self.name = name
        self.pets = []

    def add_pet(self, pet: Pet) -> None:
        """Register a pet with this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list:
        """Collect and return every task across all pets."""
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks())
        return tasks


class Scheduler:
    """The brain: retrieves, organizes, and manages tasks across all pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def sort_by_time(self, tasks=None) -> list:
        """Return tasks sorted chronologically using parsed HH:MM time values, not string order."""
        if tasks is None:
            tasks = self.owner.get_all_tasks()
        return sorted(tasks, key=lambda t: dt_time.fromisoformat(t.time))

    def filter_tasks(self, pet_name=None, completed=None) -> list:
        """Return tasks matching the given pet name and/or completion status in a single pass over all tasks."""
        return [
            t for t in self.owner.get_all_tasks()
            if (pet_name is None or t.pet_name == pet_name)
            and (completed is None or t.completed == completed)
        ]

    def detect_conflicts(self) -> list:
        """Return warning strings for every time slot where two or more tasks are scheduled simultaneously."""
        slots = defaultdict(list)
        for task in self.owner.get_all_tasks():
            slots[task.time].append(task.description)
        return [
            f"Conflict at {time}: " + ", ".join(f"'{d}'" for d in descs)
            for time, descs in slots.items()
            if len(descs) > 1
        ]

    def mark_task_complete(self, task: Task, pet: Pet):
        """Mark a task complete and auto-schedule the next occurrence if recurring."""
        next_task = task.mark_complete()
        if next_task is not None:
            pet.add_task(next_task)
        return next_task

    def get_daily_schedule(self) -> list:
        """Return today's pending tasks sorted by time."""
        today = date.today()
        tasks = [
            t for t in self.owner.get_all_tasks()
            if not t.completed and (t.due_date is None or t.due_date == today)
        ]
        return self.sort_by_time(tasks)