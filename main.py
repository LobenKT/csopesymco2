# import threading modules
from threading import Semaphore, Condition, Thread, Lock

class Citizen:

    SUPER = "Super Citizen"
    REGULAR = "Regular Citizen"

    def __init__(self):
        self.__citizens = []
        self.teams = []
        self.super = Semaphore(2)
        self.regular = Semaphore(3)
        self.team_lock = Lock()
        self.condition = Condition(self.team_lock)
        self.total_super = 0
        self.total_regular = 0
        self.__aborted = 0
        self.__done = 0
        self.__super_count = 0
        self.__regular_count = 0
        self.__super_signed = 0
        self.__regular_signed = 0

    def generate_super(self, id):
        # acquire the semaphore for super citizens
        self.super.acquire()
        # acquire the lock for team operations
        # lock is used to prevent multiple threads from accessing the team operations simultaneously
        with self.team_lock:
            # check if team formation is aborted
            # done to prevent super citizens from signing up and waiting indefinitely
            # prevents potential deadlocks
            if self.__aborted == 1:
                # release the semaphore and return
                # release the semaphore to allow other threads to acquire it then return
                self.super.release()
                return
            # print the sign up message for the super citizen
            print(f"Super Citizen {id} is signing up")
            # add the super citizen to the list of citizens
            # citizen formatting: (type, id)
            # type: super or regular
            # id: citizen id
            self.__citizens.append((self.SUPER, id))
            # increment the count of super citizens signed up
            self.__super_count += 1
        # try to form a team
        self.try_to_form_team()

    def generate_regular(self, id):
        # acquire the semaphore for reg citizens
        self.regular.acquire()
        # acquire the lock for team operations
        # lock is used to prevent multiple threads from accessing the team operations simultaneously
        with self.team_lock:
            # check if team formation is aborted
            # done to prevent reg citizens from signing up and waiting indefinitely
            # prevents potential deadlocks
            if self.__aborted == 1:
                # release the semaphore to allow other threads to acquire it then return
                self.regular.release() 
                return
            # print the sign up message for reg citizen
            print(f"Regular Citizen {id} is signing up")
            # add reg citizen to the list of citizens
            # citizen formatting: (type, id)
            # type: super or reg
            # id: citizen id
            self.__citizens.append((self.REGULAR, id))
            # increment the count of reg citizens signed up
            self.__regular_count += 1
        # try to form a team
        self.try_to_form_team()

    def super_count(self):
        # returns the count of number of super citizens in the first four elements of the list whose first element is equal to the constant value 'super'
        return len([c for c in self.__citizens[:4] if c[0] == self.SUPER])
    
    def regular_count(self):
        # returns the count of number of reg citizens in the first four elements of the list whose first element is equal to the constant value 'regular'
        return len([c for c in self.__citizens[:4] if c[0] == self.REGULAR])

    def try_to_form_team(self):
        # acquire the lock for team operations
        # condition variable is used to wait for the team formation
        with self.condition:
            # check if there are enough citizens to form a team, requiring at least 4 citizens
            if len(self.__citizens) >= 4:
                # add the first 4 citizens to a team
                self.teams.append(self.__citizens[:4])

                # get the count of super citizens and reg citizens in the team
                num_super = self.super_count()
                num_regular = self.regular_count()
                
                # print team formation message
                for _ in range(4):
                    # remove the citizen from the list of citizens
                    citizen = self.__citizens.pop(0)

                    # print the citizen joining the team message
                    print(f"{citizen[0]} {citizen[1]} has joined a team {len(self.teams)}")

                    # release the semaphore for the citizen based on the type
                    if citizen[0] == self.SUPER:
                        # increment the count of super citizens sent off to a team
                        self.__super_signed += 1
                        # release the semaphore for super citizens, allowing other super citizens to sign up
                        self.super.release()
                    elif citizen[0] == self.REGULAR:
                        # increment the count of reg citizens sent off to a team
                        self.__regular_signed += 1
                        # release the semaphore for reg citizens, allowing other reg citizens to sign up
                        self.regular.release()

                # print the team ready message
                print(f"team {len(self.teams)} is ready and now launching to battle (sc: {num_super} | rc: {num_regular})")
                # notify all threads waiting on the condition variable
                self.condition.notify_all()

                # check if all citizens have joined a team
                if (self.total_super == self.__super_count and 
                    self.total_regular == self.__regular_count):
                    # print the message indicating all citizens have joined a team
                    print("\nAll citizens have joined a team",
                          f"Total teams sent: {len(self.teams)}",
                          sep="\n")
                    # set the team formation as done
                    self.__aborted = -1
                    self.__done = 1

            # check if team formation is still not completed
            if self.__aborted != -1:
                # check if the team formation is completed
                self.__done = self.total_super == self.__super_count and self.total_regular == self.__regular_count

                # important: The following condition prevents deadlocks

                # the following condition prevents deadlocks
                # check if there are less than 4 citizens signed up and team formation is completed
                if (
                    len(self.__citizens) < 4 and self.__done == 1 or 
                    # check if there are no citizens left to form a team and either all super citizens or all reg citizens are sent off
                    len(self.__citizens) == 0 and (self.total_super == self.__super_count or self.total_regular == self.__regular_count) or
                    # check if there are not enough super citizens to form a team or not enough reg citizens to form a team
                    # checks the state of 2 super citizens 
                    (self.super_count() == 2 and self.total_regular == self.__regular_count or
                    # checks the state of 3 reg citizens
                    self.regular_count() == 3 and self.total_super == self.__super_count)):

                    # important notify all threads waiting on the condition variable
                    self.__aborted = 1
                    self.super.release()
                    self.regular.release()
                    # print the message indicating not enough citizens to form a team
                    print(
                        "\nNot enough citizens to form a team", 
                        f"Total teams sent: {len(self.teams)}",
                        f"Remaining super citizens not sent off: {self.total_super - self.__super_signed}",
                        f"Remaining regular citizens not sent off: {self.total_regular - self.__regular_signed}",
                        sep="\n")

    """
    starts the program with the given number of reg and super citizens.
    
    args:
        r (int): # of reg citizens
        s (int): # of super citizens.
    """

    def start(self, r, s):
        self.total_super = s    # set the total num of super citizens
        self.total_regular = r  # set the total num of reg citizens
        
        # start the threads for generating reg citizens
        for i in range(r):
            Thread(target=self.generate_regular, args=(i+1,)).start()
        # start the threads for generating super citizens
        for i in range(s):
            Thread(target=self.generate_super, args=(i+1,)).start()

# main func
if __name__ == "__main__":
    c = Citizen()   # create a citizen object
    c.start(10, 5)  # start the program with 10 reg citizens and 5 super citizens
