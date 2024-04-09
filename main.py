import threading
from threading import Semaphore, Condition
from collections import deque

# Initialization
super_citizen_semaphore = Semaphore(2)  # Up to 2 Super Citizens in a team
regular_citizen_semaphore = Semaphore(3)  # Up to 3 Regular Citizens in a team
team_lock = threading.Lock()
condition = Condition(team_lock)
team_count = 0
waiting_super_citizens = deque()  # Queue of Super Citizen IDs
waiting_regular_citizens = deque()  # Queue of Regular Citizen IDs
total_citizens = 0
citizens_started = 0

def super_citizen(id):
    global citizens_started
    super_citizen_semaphore.acquire()
    with team_lock:
        waiting_super_citizens.append(id)
        citizens_started += 1
        print(f"Super Citizen {id} is signing up")
    try_to_form_team()

def regular_citizen(id):
    global citizens_started
    regular_citizen_semaphore.acquire()
    with team_lock:
        waiting_regular_citizens.append(id)
        citizens_started += 1
        print(f"Regular Citizen {id} is signing up")
    try_to_form_team()

def try_to_form_team():
    global team_count, citizens_started
    with condition:
        while len(waiting_super_citizens) >= 1 and (len(waiting_super_citizens) + len(waiting_regular_citizens)) >= 4:
            team_count += 1
            num_super_in_team = min(2, len(waiting_super_citizens))  # At most 2 Super Citizens in a team
            num_regular_in_team = 4 - num_super_in_team
            
            for _ in range(num_super_in_team):  # Assign Super Citizens to the team
                sc_id = waiting_super_citizens.popleft()
                print(f"Super Citizen {sc_id} has joined team {team_count}")
                super_citizen_semaphore.release()  # Release after joining
                
            for _ in range(num_regular_in_team):  # Assign Regular Citizens to the team
                rc_id = waiting_regular_citizens.popleft()
                print(f"Regular Citizen {rc_id} has joined team {team_count}")
                regular_citizen_semaphore.release()  # Release after joining
                
            print(f"team {team_count} is ready and now launching to battle (sc: {num_super_in_team} | rc: {num_regular_in_team})")
            condition.notify_all()

        if citizens_started == total_citizens:
            if len(waiting_super_citizens) + len(waiting_regular_citizens) < 4 or len(waiting_regular_citizens) == 0:
                # Not enough citizens to form a new team or not enough Regular Citizens left
                print(f"Simulation ended: Not enough citizens to form a new team. Remaining Super Citizens: {len(waiting_super_citizens)}, Remaining Regular Citizens: {len(waiting_regular_citizens)}")
                condition.notify_all()  # Signal all waiting threads

def start_simulation(r, s):
    global total_citizens
    total_citizens = r + s
    for i in range(1, s + 1):
        threading.Thread(target=super_citizen, args=(i,)).start()
    for i in range(1, r + 1):
        threading.Thread(target=regular_citizen, args=(i,)).start()

# Example simulation call
start_simulation(r=1, s=10)
