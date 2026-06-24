from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler

# --- Set up Owner ---
owner = Owner("Jessie")

# --- Set up Pets ---
biscuit = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age=3)
mochi = Pet(name="Mochi", species="cat", breed="Siamese", age=5, medications="allergy pill")

# --- Add Tasks to Biscuit ---
biscuit.add_task(Task("Evening walk",    "18:00", "daily", due_date=date.today()))
biscuit.add_task(Task("Morning feeding", "08:00", "daily", due_date=date.today()))
biscuit.add_task(Task("Vet appointment", "10:00", "once",  due_date=date.today()))

# --- Add Tasks to Mochi ---
mochi.add_task(Task("Morning feeding",  "08:00", "daily",  due_date=date.today()))  # same time as Biscuit!
mochi.add_task(Task("Give allergy pill","09:00", "daily",  due_date=date.today()))
mochi.add_task(Task("Playtime",         "15:00", "weekly", due_date=date.today()))

# --- Register pets with Owner ---
owner.add_pet(biscuit)
owner.add_pet(mochi)

# --- Create Scheduler ---
scheduler = Scheduler(owner)

# --- Print Today's Schedule ---
print("=" * 45)
print(f"  PawPal+ | Today's Schedule for {owner.name}")
print("=" * 45)

schedule = scheduler.get_daily_schedule()
for task in schedule:
    status = "[DONE]" if task.completed else "[    ]"
    print(f"  {status}  {task.time}  |  {task.pet_name:<8}  |  {task.description}")

# --- Check for Conflicts ---
print()
print("--- Conflict Check ---")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for c in conflicts:
        print(f"  WARNING: {c}")
else:
    print("  No conflicts found.")

# --- Filter: just Biscuit's tasks ---
print()
print("--- Biscuit's Tasks Only ---")
for task in scheduler.filter_tasks(pet_name="Biscuit"):
    print(f"  {task.time}  |  {task.description}  ({task.frequency})")

# --- Demo: mark a recurring task complete ---
print()
print("--- Marking 'Evening walk' complete ---")
scheduler.mark_task_complete(biscuit.tasks[0], biscuit)
print(f"  Done! Biscuit now has {len(biscuit.tasks)} tasks (tomorrow's walk auto-scheduled).")