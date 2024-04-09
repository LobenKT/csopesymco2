import threading
from collections import deque

# Using simple threading conditions and locks instead of semaphores for fine-grained control
team_lock = threading.Lock()
condition = threading.Condition(team_lock)
team_count = 0
waiting_super_citizens = deque()  # Queue of Super Citizen IDs
waiting_regular_citizens = deque()  # Queue of Regular Citizen IDs
total_citizens = 0
citizens_signed_up = 0  # Counter for signed up citizens

def citizen_signup(id, is_super):
    global citizens_signed_up
    with team_lock:
        citizens_signed_up += 1
        if is_super:
            waiting_super_citizens.append(id)
            print(f"Super Citizen {id} is signing up")
        else:
            waiting_regular_citizens.append(id)
            print(f"Regular Citizen {id} is signing up")
        
        # Attempt to form a team after each signup
        try_to_form_team()
        
        # If all citizens have signed up, check if we can form more teams or need to end the simulation
        if citizens_signed_up == total_citizens:
            try_to_form_team(check_end_condition=True)

def try_to_form_team(check_end_condition=False):
    global team_count
    while len(waiting_super_citizens) + len(waiting_regular_citizens) >= 4 and len(waiting_super_citizens) > 0:
        team_count += 1
        sc_in_team = min(2, len(waiting_super_citizens))  # At most 2 Super Citizens per team
        rc_in_team = 4 - sc_in_team  # Fill the rest with Regular Citizens
        
        # Assign Super and Regular Citizens to the team
        for _ in range(sc_in_team):
            sc_id = waiting_super_citizens.popleft()
            print(f"Super Citizen {sc_id} has joined team {team_count}")
        for _ in range(rc_in_team):
            rc_id = waiting_regular_citizens.popleft()
            print(f"Regular Citizen {rc_id} has joined team {team_count}")
            
        print(f"team {team_count} is ready and now launching to battle (sc: {sc_in_team} | rc: {rc_in_team})")
        
    # Check if no more teams can be formed and if all citizens have signed up
    if check_end_condition and (len(waiting_super_citizens) + len(waiting_regular_citizens) < 4 or len(waiting_regular_citizens) == 0 or citizens_signed_up == total_citizens):
        print(f"Simulation ended: Not enough citizens to form a new team. Remaining Super Citizens: {len(waiting_super_citizens)}, Remaining Regular Citizens: {len(waiting_regular_citizens)}")
        condition.notify_all()  # Ensure all waiting threads are not left hanging

def super_citizen(id):
    citizen_signup(id, True)

def regular_citizen(id):
    citizen_signup(id, False)

def start_simulation(r, s):
    global total_citizens
    total_citizens = r + s
    for i in range(1, r + 1):
        threading.Thread(target=regular_citizen, args=(i,)).start()
    for i in range(1, s + 1):
        threading.Thread(target=super_citizen, args=(i,)).start()

# Example simulation call
start_simulation(r=1, s=10)
