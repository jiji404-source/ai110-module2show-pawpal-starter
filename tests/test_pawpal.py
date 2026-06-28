from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


# --- Existing tests (required by Phase 2) ---

def test_mark_complete_changes_status():
    task = Task("Morning walk", "08:00", "once")
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Biscuit", species="dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task("Walk", "08:00", "daily"))
    assert len(pet.tasks) == 1


# --- New tests (required by Phase 5) ---

def test_sort_by_time_returns_chronological_order():
    # ARRANGE: Add three tasks in the WRONG order on purpose
    pet = Pet(name="Biscuit", species="dog")
    pet.add_task(Task("Evening walk",  "18:00", "once"))  # added first
    pet.add_task(Task("Lunchtime snack", "12:00", "once"))  # added second
    pet.add_task(Task("Morning walk",   "08:00", "once"))  # added third

    owner = Owner("Jessie")
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    # ACT: ask the scheduler to sort them
    sorted_tasks = scheduler.sort_by_time()

    # ASSERT: the times should now be earliest → latest, not the order we added them
    times = [t.time for t in sorted_tasks]
    assert times == ["08:00", "12:00", "18:00"]


def test_daily_recurrence_creates_next_day_task():
    # ARRANGE: a daily task with a known due date
    today = date.today()
    task = Task("Feed Biscuit", "07:00", "daily", due_date=today)

    # ACT: mark it complete — this should return a brand-new Task
    next_task = task.mark_complete()

    # ASSERT 1: a next task was actually created (not None)
    assert next_task is not None

    # ASSERT 2: the new task is scheduled for TOMORROW, not today
    assert next_task.due_date == today + timedelta(days=1)


def test_detect_conflicts_flags_duplicate_times():
    # ARRANGE: two tasks scheduled at exactly the same time
    pet = Pet(name="Biscuit", species="dog")
    pet.add_task(Task("Feed Biscuit",  "08:00", "once"))
    pet.add_task(Task("Walk Biscuit",  "08:00", "once"))  # same time — conflict!

    owner = Owner("Jessie")
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    # ACT: ask the scheduler to look for conflicts
    conflicts = scheduler.detect_conflicts()

    # ASSERT: there should be at least one conflict warning
    assert len(conflicts) > 0