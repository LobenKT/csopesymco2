import threading
from threading import Semaphore, Condition

# Initialization
super_citizen_semaphore = Semaphore(2)  # Up to 2 Super Citizens in a team
regular_citizen_semaphore = Semaphore(3)  # Up to 3 Regular Citizens in a team
team_lock = threading.Lock()
condition = Condition(team_lock)
team_count = 0
waiting_super_citizens = 0
waiting_regular_citizens = 0

def super_citizen(id):
    global waiting_super_citizens
    super_citizen_semaphore.acquire()
    with team_lock:
        waiting_super_citizens += 1
        print(f"Super Citizen {id} is signing up")
    try_to_form_team()

def regular_citizen(id):
    global waiting_regular_citizens
    regular_citizen_semaphore.acquire()
    with team_lock:
        waiting_regular_citizens += 1
        print(f"Regular Citizen {id} is signing up")
    try_to_form_team()

def try_to_form_team():
    global team_count, waiting_super_citizens, waiting_regular_citizens
    with condition:
        if waiting_super_citizens >= 1 and (waiting_super_citizens + waiting_regular_citizens) >= 4:
            # Form a team
            num_super_in_team = min(2, waiting_super_citizens)  # At most 2 Super Citizens
            num_regular_in_team = 4 - num_super_in_team  # The rest are Regular Citizens
            waiting_super_citizens -= num_super_in_team
            waiting_regular_citizens -= num_regular_in_team
            team_count += 1
            print(f"team {team_count} is ready and now launching to battle (sc: {num_super_in_team} | rc: {num_regular_in_team})")
            # Release the semaphores for the next team
            for _ in range(num_super_in_team):
                super_citizen_semaphore.release()
            for _ in range(num_regular_in_team):
                regular_citizen_semaphore.release()
            condition.notify_all()
        elif waiting_super_citizens + waiting_regular_citizens < 4:
            # Not enough citizens to form a team, the simulation can end
            print(f"Simulation ended: Not enough citizens to form a new team. Remaining Super Citizens: {waiting_super_citizens}, Remaining Regular Citizens: {waiting_regular_citizens}")
            condition.notify_all()  # In case any threads are waiting, they should be released to end the simulation

def start_simulation(r, s):
    for i in range(1, r + 1):
        threading.Thread(target=regular_citizen, args=(i,)).start()
    for i in range(1, s + 1):
        threading.Thread(target=super_citizen, args=(i,)).start()

# Example simulation
start_simulation(r=10, s=5)
