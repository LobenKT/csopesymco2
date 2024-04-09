import threading
from collections import deque

# Lock and condition for managing team formation
team_lock = threading.Lock()
condition = threading.Condition(team_lock)
team_count = 0
waiting_super_citizens = deque()
waiting_regular_citizens = deque()
total_citizens_signed_up = 0

def sign_up_citizen(citizen_id, is_super):
    global total_citizens_signed_up
    with condition:
        # Increment the total signed up citizens count
        total_citizens_signed_up += 1
        # Add citizen to the appropriate queue
        if is_super:
            waiting_super_citizens.append(citizen_id)
            print(f"Super Citizen {citizen_id} is signing up")
        else:
            waiting_regular_citizens.append(citizen_id)
            print(f"Regular Citizen {citizen_id} is signing up")
        
        # Try to form a team if possible
        try_to_form_team()
        
def try_to_form_team():
    global team_count
    with condition:
        # Check if enough citizens are available to form a team
        while len(waiting_super_citizens) >= 1 and len(waiting_super_citizens) + len(waiting_regular_citizens) >= 4:
            team_count += 1
            sc_in_team, rc_in_team = 0, 0
            
            # Assign Super Citizens to the team
            while sc_in_team < 2 and waiting_super_citizens:
                sc_id = waiting_super_citizens.popleft()
                print(f"Super Citizen {sc_id} has joined team {team_count}")
                sc_in_team += 1
            
            # Fill the rest of the team with Regular Citizens
            while len(waiting_super_citizens) + sc_in_team + rc_in_team < 4 and waiting_regular_citizens:
                rc_id = waiting_regular_citizens.popleft()
                print(f"Regular Citizen {rc_id} has joined team {team_count}")
                rc_in_team += 1
            
            print(f"team {team_count} is ready and now launching to battle (sc: {sc_in_team} | rc: {rc_in_team})")
        
        # Check if the simulation should end
        if total_citizens_signed_up == len(waiting_super_citizens) + len(waiting_regular_citizens) + (team_count * 4):
            print("No more teams can be formed. Ending simulation.")
            condition.notify_all()  # Notify any potentially waiting threads to exit wait

def super_citizen(id):
    sign_up_citizen(id, True)

def regular_citizen(id):
    sign_up_citizen(id, False)

def start_simulation(r, s):
    threads = []
    for i in range(1, s + 1):
        t = threading.Thread(target=super_citizen, args=(i,))
        t.start()
        threads.append(t)
    for i in range(1, r + 1):
        t = threading.Thread(target=regular_citizen, args=(i,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()  # Wait for all threads to finish

# Adjust the numbers as needed for your test case
start_simulation(r=1, s=10)
