import threading
from threading import Semaphore, Lock

# Initialize semaphores and locks
super_citizen_semaphore = Semaphore(2)  # Up to 2 Super Citizens
regular_citizen_semaphore = Semaphore(3)  # Up to 3 Regular Citizens
team_lock = Lock()  # Ensure atomic team checks and formations
team_count = 0

def super_citizen(id):
    with super_citizen_semaphore:
        print(f"Super Citizen {id} is signing up")
        try_to_form_team("Super Citizen", id)

def regular_citizen(id):
    with regular_citizen_semaphore:
        print(f"Regular Citizen {id} is signing up")
        try_to_form_team("Regular Citizen", id)

def try_to_form_team(citizen_type, id):
    global team_count
    with team_lock:
        # Logic to check if a team can be formed goes here
        # This is a simplification. You need to implement the actual checks based on the task's rules.
        print(f"{citizen_type} {id} has joined team {team_count}")
        # If team is ready, increment team_count and release semaphores accordingly
        team_count += 1
        print(f"team {team_count} is ready and now launching to battle")

# Example of starting threads for citizens
def start_simulation(r, s):
    for i in range(1, r + 1):
        threading.Thread(target=regular_citizen, args=(i,)).start()
    for i in range(1, s + 1):
        threading.Thread(target=super_citizen, args=(i,)).start()

# Call this function with the number of Regular and Super Citizens
start_simulation(r=10, s=5)
