# csopesymco2
Process Synchronization
Helldivers Synchronization Problem
The Ministry of Defense (MoD) has initiated a crucial operation to counter the invasion of Automatons and Terminids threatening Super Earth. As part of this operation, elite soldiers (i.e. Helldivers) are deployed on missions and engage in intense battles against the enemy forces.

The recent propaganda information dissemination efforts by the MoD have resulted in a sharp increase in patriotism -- leading to massive numbers of citizen signups. The upper command is concerned with the quality of the recruits while hoping to send out Helldivers as soon as possible. Democracy must continue to spread! Hence, to ensure the success of each mission, all succeeding missions must have the following:

Each mission must consist of exactly 4 Helldivers
Among the 4 Helldivers, there must be at least 1 "Super Citizen," an elite member highly skilled in combat and tactics
Missions can accommodate up to 2 Super Citizens at most
Regular Citizens, though not as highly skilled as Super Citizens, are still valuable assets and must compose the remaining slots in the team.
Mission signups are on a first-come, first-served basis, so if a certain type of citizen builds up a queue, they must wait until they can be served (headquarters can only do so much...)
Once the team has been properly composed, the Helldivers are directly launched into their mission
If a team cannot be formed (e.g. only 2 Regular Citizens and 1 Super Citizen are left), then the remaining citizens are sent home
Task
Your task is to develop a synchronization mechanism to ensure that teams are assembled correctly according to the rules described above. Your solution should not result in deadlock or starvation and should exit only when teams cannot be formed and/or there are no more citizens left.

You may implement the program in your language of preference. In other words, feel free to pick your own PL for the MCO. Please select a PL that everyone in your group is comfortable with.

Input
The program accepts two inputs from the user, described as follows:

r – the number of Regular Citizens
s – the number of Super Citizens

Output
Given that thread execution may vary per execution, it is possible that any sample output would not align with your output. Hence, utilize the following rules as a guide for producing output:

When a Regular Citizen is signing up, display Regular Citizen <rc_id> is signing up
When a Super Citizen is signing up, display Super Citizen <sc_id> is signing up
When any Citizen joins a team, display <citizen_type> <citizen_id> has joined team <team_id>
When a team is properly composed and ready to launch, display team <team_id> is ready and now launching to battle (sc: <super_count> | rc: <regular_count>)
Once all teams have been launched and/or there are not enough citizens to form teams, the program should display the total teams sent and the number of Regular and Super Citizens that were not sent off

Required Program Interaction
There should be minimal program interaction. The program will ask the user to input the values for r and s.