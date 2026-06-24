from pawpal_system import Task, Pet


def test_mark_complete_changes_status():
    task = Task("Morning walk", "08:00", "once")
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Biscuit", species="dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task("Walk", "08:00", "daily"))
    assert len(pet.tasks) == 1