# Tennis-Scheduler
Schedule tennis drop in matches for players of various USTA levels and preferences (Singles, Doubles, Either).

The system will give a preference for doubles for players willing to play either, and will move players to singles matches if needed.

A close average rating between singles and doubles pairs is attempted, when possible. If the average rating goes past the threshold set in the UI, a warning will be displayed for that match up.

If courts are limited such that not everyone can play, those preferring singles will get added to doubles matches to attempt to ensure everyone can play. If there are still too many players for the number of courts available, some players will be put "on deck." If there are an odd number of players, one or more players will be put "on deck." 

You can assign matchups early for Singles play, before you actually generate the matches for the full session. For each singles match you assign early, check both players and make sure to select the Opponent in the drop down for at least one of them. For example, if John wants to play Doug, check both John and Doug and for John, select Doug as the Opponent (or select John as the opponent for Doug. You only need to do this for one of the players of that match).

To use: 
On the left side, input the number of courts available. Also, if you want a warning when the average USTA levels between opposing doubles pairings or opposing singles pairings is above a certain amount, set that to your desired value (ex. if you leave it at the default of 0.5, the matchups where the differnce is higher than 0.5 will be highlighted).

Input your Google sheet URL in the designated input box, then hit your Enter button or the "Load" button. Check each player that is here, override any of their preferences, and enter any guest players and enter their preferences. Next, hit "Generate Matchups". You can hit "Generate Matchups" as many times as you like. Each time you hit it, new match ups will be created.

What currently can't be accommodated:

If someone wants to play the same opponent in Singles both rounds.

If a person wants to play doubles with a specific person in the first round but someone else in the second round.

Assigning courts early for doubles play. For example, if you want to assign a court to 4 people who can play before the start time, there isn't a way to set that up in the system. One workaround is for any courts that are assigned manually (not using this app) for Round 1, then those players should not be checked when generating the match ups. After generating the matchups, ignore the second round matches, check all the players that were assigned to courts manually, then re-run the generation of matchups and use the results from Round 1 for Round 2. 
