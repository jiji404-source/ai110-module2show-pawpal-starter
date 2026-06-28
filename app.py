import streamlit as st
from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler

if "owner" not in st.session_state:
    st.session_state.owner = Owner("My Owner")

owner = st.session_state.owner
scheduler = Scheduler(owner)

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")
st.title("🐾 PawPal+")
st.caption("Smart pet care management system")

# ── Sidebar: Owner name + Add Pet ──────────────────────────────────────────
with st.sidebar:
    st.header("Setup")

    st.subheader("Owner")
    new_name = st.text_input("Your name", value=owner.name)
    if st.button("Update name"):
        st.session_state.owner.name = new_name
        st.success(f"Name updated to {new_name}!")

    st.divider()

    st.subheader("Add a Pet")
    pet_name  = st.text_input("Pet name")
    species   = st.selectbox("Species", ["dog", "cat", "rabbit", "bird", "other"])
    breed     = st.text_input("Breed (optional)")
    age       = st.number_input("Age", min_value=0, max_value=30, value=1)
    allergies = st.text_input("Allergies (optional)")
    meds      = st.text_input("Medications (optional)")

    if st.button("Add Pet", type="primary"):
        if pet_name.strip():
            existing = [p.name for p in owner.pets]
            if pet_name in existing:
                st.warning(f"{pet_name} is already added.")
            else:
                owner.add_pet(Pet(pet_name, species, breed, age, allergies, meds))
                st.success(f"Added {pet_name}!")
        else:
            st.error("Please enter a pet name.")

    if owner.pets:
        st.divider()
        st.subheader("Your Pets")
        for p in owner.pets:
            st.write(f"**{p.name}** — {p.species}" + (f", {p.breed}" if p.breed else ""))

# ── Main area ──────────────────────────────────────────────────────────────
if not owner.pets:
    st.info("Start by adding a pet in the sidebar.")
    st.stop()

tab1, tab2, tab3 = st.tabs(["Add Task", "Today's Schedule", "Manage Tasks"])

# ── Tab 1: Add Task ────────────────────────────────────────────────────────
with tab1:
    st.header("Schedule a Task")

    col1, col2 = st.columns(2)
    with col1:
        selected_pet = st.selectbox("Pet", [p.name for p in owner.pets])
        task_desc    = st.text_input("What needs to happen?", placeholder="e.g. Morning walk")
    with col2:
        task_time  = st.time_input("Time")
        frequency  = st.selectbox("Frequency", ["once", "daily", "weekly"])

    if st.button("Schedule Task", type="primary"):
        if task_desc.strip():
            pet      = next(p for p in owner.pets if p.name == selected_pet)
            time_str = task_time.strftime("%H:%M")
            pet.add_task(Task(task_desc, time_str, frequency, due_date=date.today()))
            st.success(f"Scheduled '{task_desc}' for {selected_pet} at {time_str}!")
        else:
            st.error("Please enter a task description.")

# ── Tab 2: Today's Schedule ────────────────────────────────────────────────
with tab2:
    st.header("Today's Schedule")

    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for c in conflicts:
            st.warning(f"⚠️ {c}")

    schedule = scheduler.get_daily_schedule()
    if not schedule:
        st.info("No tasks scheduled for today. Add some in the 'Add Task' tab.")
    else:
        st.table([
            {
                "Time":      t.time,
                "Pet":       t.pet_name,
                "Task":      t.description,
                "Frequency": t.frequency,
                "Status":    "Done ✓" if t.completed else "Pending",
            }
            for t in schedule
        ])

# ── Tab 3: Manage Tasks ────────────────────────────────────────────────────
with tab3:
    st.header("Manage Tasks")

    col1, col2 = st.columns(2)
    with col1:
        filter_pet    = st.selectbox("Filter by pet",    ["All"] + [p.name for p in owner.pets])
    with col2:
        filter_status = st.selectbox("Filter by status", ["All", "Pending", "Done"])

    pet_filter       = None if filter_pet    == "All"     else filter_pet
    completed_filter = None if filter_status == "All"     else (filter_status == "Done")

    filtered = scheduler.sort_by_time(
        scheduler.filter_tasks(pet_name=pet_filter, completed=completed_filter)
    )

    if not filtered:
        st.info("No tasks match this filter.")
    else:
        for i, task in enumerate(filtered):
            col_btn, col_info = st.columns([1, 8])
            with col_info:
                st.write(f"**{task.time}** | {task.pet_name} | {task.description} | *{task.frequency}*")
            with col_btn:
                if not task.completed:
                    if st.button("Complete", key=f"complete_{i}"):
                        pet = next(p for p in owner.pets if p.name == task.pet_name)
                        scheduler.mark_task_complete(task, pet)
                        st.rerun()
                else:
                    st.success("Done")