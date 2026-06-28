# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
The UML diagram shows four classes connected by arrows.

Owner sits at the top and has a one-to-many relationship with Pet, meaning one owner can have multiple pets. Pet has a one-to-many relationship with Task, meaning each pet can have multiple care tasks assigned to it. Scheduler connects to Owner and uses it as a way to reach all pets and their tasks without storing any data itself. The arrows show that Owner "owns" Pets, Pet "has" Tasks, and Scheduler "manages" the Owner.


classDiagram
    class Task {
        +String description
        +String time
        +String frequency
        +Boolean completed
        +Date due_date
        +String pet_name
        +mark_complete() Task
    }

    class Pet {
        +String name
        +String breed
        +Int age
        +String allergies
        +String medications
        +List tasks
        +add_task(task) None
        +get_tasks() List
    }

    class Owner {
        +String name
        +List pets
        +add_pet(pet) None
        +get_all_tasks() List
    }

    class Scheduler {
        +Owner owner
        +sort_by_time(tasks) List
        +filter_tasks(pet_name, completed) List
        +detect_conflicts() List
        +mark_task_complete(task, pet) Task
        +get_daily_schedule() List
    }

    Owner "1" --> "0..*" Pet : owns
    Pet "1" --> "0..*" Task : has
    Scheduler --> Owner : manages

- What classes did you include, and what responsibilities did you assign to each?

- Task: Represents one care activity. It holds a description (like "Morning walk"), a scheduled time, how often it repeats (once/daily/weekly), and whether it's been completed.

- Pet: Stores a pet's details (name, breed, age, allergies, and medications). It also holds a list of Task objects for everything that pet needs done.

- Owner: Holds the owner's name and a list of their pets. It's the top-level container that connects everything.

- Scheduler: The "brain" of the system. It takes the Owner's pets and tasks and organizes them: sorting by time, detecting conflicts, and returning today's schedule.


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
I originally listed walk, feed, groom, and play as separate things, but I realized those are just values for the description field inside one Task class, not separate classes themselves. I also added allergies and medications as Pet attributes since a real pet care app needs that info.

I kept Owner and Scheduler as regular classes instead of dataclasses because they manage mutable state (lists that grow over time) and have more complex behavior than just storing data. Task and Pet became dataclasses since they mainly hold information.




---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
The scheduler considers three constraints: time (tasks are sorted chronologically by their HH:MM value), due date (only tasks due today appear in the daily schedule), and completion status (completed tasks are filtered out of the active view).

- How did you decide which constraints mattered most?
Time was the most important constraint because a pet care routine is inherently time-driven, a feeding at 08:00 and a medication at 09:00 need to happen in order. Due date mattered because showing all tasks ever added would clutter the schedule. Completion status mattered so owners aren't reminded to do things they've already done. Priority and duration were not considered because the app is designed for simple daily routines, not complex scheduling problems.


**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
The scheduler only checks for exact time matches when detecting conflicts, if two tasks are both scheduled at "08:00", it flags a warning. But it doesn't account for tasks that overlap in duration. For example, a 30-minute walk starting at 07:45 and a feeding at 08:00 would never be flagged, even if they can't both happen at once.

- Why is that tradeoff reasonable for this scenario?
This tradeoff is reasonable for this scenario because pet care tasks don't have strict durations, a "feeding" could take 2 minutes or 10 minutes depending on the day. Requiring duration data would make the system more complex to use without meaningfully improving it for most pet owners. Exact time matching covers the most common real conflict: two things literally scheduled at the same moment.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
