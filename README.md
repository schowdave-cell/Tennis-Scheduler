# Tennis-Scheduler
Schedule tennis drop in matches for players of various USTA levels and preferences (Singles, Doubles, Either).

The system will give a preference for doubles for players willing to play either, and will move players to singles matches if needed.

A close average rating between doubles pairs is attempted, when possible. If the average rating goes past the threshold set in the UI, a warning will be displayed for that match up.

If courts are limited such that not everyone can play, those preferring singles will get added to doubles matches to attempt to ensure everyone can play. If there are still too many players for the number of courts available, some players will be put "on deck." If there are an odd number of players, one player will be put "on deck." 

To use: 
On the left side, input the number of courts available. Also, if you want a warning when the average USTA levels between opposing doubles pairings or opposing singles pairings is above a certain amount, set that to your desired value (ex. if you leave it at the default of 0.5, the matchups where the differnce is higher than 0.5 will be highlighted).

Input your Google sheet URL in the designated input box, then hit your Enter button or the "Load" button. Next, hit "Generate Matchups". You can hit "Generate Matchups" as many times as you like. Each time you hit it, new match ups will be created.
