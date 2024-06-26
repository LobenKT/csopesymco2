import threading
from threading import Semaphore, Condition
import random

# Initialization
super_citizen_semaphore = Semaphore(2)  # Up to 2 Super Citizens in a team
regular_citizen_semaphore = Semaphore(3)  # Up to 3 Regular Citizens in a team
team_lock = threading.Lock()
condition = Condition(team_lock)
team_count = 0
waiting_super_citizens = 0
waiting_regular_citizens = 0
total_citizens = 0  # New: Track the total number of citizens who started the signup process
citizens_started = 0  # New: Track the number of citizens who have started the signup process
super_signed = []
regular_signed = []

def super_citizen(id):
    global waiting_super_citizens, citizens_started
    super_citizen_semaphore.acquire()
    with team_lock:
        waiting_super_citizens += 1
        citizens_started += 1
        print(f"Super Citizen {id} is signing up")
        super_signed.append(id)
        random.shuffle(super_signed)
    try_to_form_team()

def regular_citizen(id):
    global waiting_regular_citizens, citizens_started
    regular_citizen_semaphore.acquire()
    with team_lock:
        waiting_regular_citizens += 1
        citizens_started += 1
        print(f"Regular Citizen {id} is signing up")
        regular_signed.append(id)
        random.shuffle(regular_signed)
    try_to_form_team()

def try_to_form_team():
    global team_count, waiting_super_citizens, waiting_regular_citizens, citizens_started
    team_formed = False  # Flag to indicate if at least one team was formed in this call
    with condition:
        while waiting_super_citizens >= 1 and (waiting_super_citizens + waiting_regular_citizens) >= 4:
            team_formed = True
            num_super_in_team = min(2, waiting_super_citizens)  # At most 2 Super Citizens
            num_regular_in_team = 4 - num_super_in_team  # The rest are Regular Citizens
            
            # Decrement the counters for waiting citizens
            waiting_super_citizens -= num_super_in_team
            waiting_regular_citizens -= num_regular_in_team
            
            team_count += 1
            
            # Release the semaphores for the citizens that have joined a team
            for _ in range(num_super_in_team):
                super_citizen_semaphore.release()

                print(f"Super Citizen {super_signed.pop(0)} has joined the team {team_count}")
            for _ in range(num_regular_in_team):
                regular_citizen_semaphore.release()
                print(f"Regular Citizen {regular_signed.pop(0)} has joined the team {team_count}")


            print(f"team {team_count} is ready and now launching to battle (sc: {num_super_in_team} | rc: {num_regular_in_team})")

        # Notify all waiting threads to re-evaluate their conditions after attempting to form a team
        condition.notify_all()

        # End-of-Simulation Check: After all citizens have signed up
        if not team_formed and citizens_started == total_citizens:
            if waiting_super_citizens + waiting_regular_citizens < 4 or waiting_regular_citizens == 0:
                print(f"Simulation ended: Not enough citizens to form a new team. Remaining Super Citizens: {waiting_super_citizens}, Remaining Regular Citizens: {waiting_regular_citizens}")
                condition.notify_all()  # Prevent threads from waiting indefinitely

        # Additional check for early simulation end: If there are only Super Citizens left but not enough Regular Citizens to form a team
        elif waiting_regular_citizens == 0 and waiting_super_citizens > 0:
            print(f"Simulation ended early: Not enough Regular Citizens to form a new team. Remaining Super Citizens: {waiting_super_citizens}")
            condition.notify_all()  # Release any waiting Super Citizens




def start_simulation(r, s):
    global total_citizens
    total_citizens = r + s  # Set the total number of citizens based on input
    for i in range(1, r + 1):
        threading.Thread(target=regular_citizen, args=(i,)).start()
    for i in range(1, s + 1):
        threading.Thread(target=super_citizen, args=(i,)).start()

# Example simulation
start_simulation(r=1, s=10)
