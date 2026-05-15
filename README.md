# Tennis-Scheduler
Schedule tennis drop in matches for players of various USTA levels and preferences (Singles, Doubles, Either).

The system will give a preference for doubles for players willing to play either, and will move players to singles matches if needed.

A close average rating between doubles pairs is attempted, when possible. If the average rating goes past the threshold set in the UI, a warning will be displayed for that match up.

If courts are limited such that not everyone can play, those preferring singles will get added to doubles matches to attempt to ensure everyone can play. If there are still too many players for the number of courts available, some players will be put "on deck."
