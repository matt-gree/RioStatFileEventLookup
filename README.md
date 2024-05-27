# RioStatFileEventLookup
 Looks up events in ProjectRio stat files based on parameter inputs.

# Usage
The program makes use of both parameters followed by an argument as well as flags, which simply denote a characterisitic of the play. Use the config flie to set the path to the folder contianing the stat files you wish to look through. By default, the script contains a directory of stat files from games recorded on the MattGree youtube channel. This allows the user to find clips of events they are searching for. **Note**: Only works with project Rio 1.9.6 stat files and later (~ April 2023)

# Parameters
- ***-firstFielderPos***: Position in the field of the character who first picks up the ball during the event. Accepted postions: P, C, 1B, 2B, 3B, SS, LF, CF, RF.
- ***-batter***: Name of the batting character during the event.
- ***-pitcher***: Name of the pitching character during the event.
- ***-fielder***: Name of the first character to field the ball during the event.
- ***-inning***: Inning number for the event to occur in. A negative input returns all events during or after the specified inning. Accepts multiple space seperated inputs.
- ***-halfInning***: Half inning for the event to occur in (O for top and 1 for bottom)
- ***-runnersOnBase***: Input the numbers of the bases characters are to appear on during the event. The input is a list of a maximum of three numbers -3 to 3. If the base number is positive, then the returned events will all have a runner on that base. If the base number is negative, then the returned events will not care whether a runner appears on that base or not. If the base number is not provided, then the returned events will not have a runner on that base
Examples:
    -1,2 will return events that had runners only on both 1st and 2nd base
    1,2, -3 will return events that had runners on both 1st or 2nd whether or not a runner is on 3rd
    -1, -2, -3 will return events any time any runners are on any base
    -1, -2, 0 will return events with no runners, or runners on first or second, but none that have runners on 3rd 
- ***-outsInInning***: Number of outs in the inning at the time of the event. A negative input returns events with at least that many outs.
- ***-balls***: Number of balls in the count at the time of the event. A negative input returns events with at least that many balls.
- ***-strikes***: Number of strikes in the count at the time of the event. A negative input returns events with at least that many strikes.
- ***-chemOnBase***: Number of chem links on base at the time of the event. A negative input returns events with at least that many chem links.
- ***-rbi***: Number of RBI during the event A negative input returns events with at least that many RBI.
- ***-battingPlayer***: Rio Username of the batter during the event.
- ***-pitchingPlayer***: Rio Username of the pitcher during the event.
- ***-swingType***: Type of swing during the event. Accepted Values: none, slap, charge, star, bunt.
- ***-ballStrikezonePos***: Returns all events with a Ball Strikezone Position of at least the amount input. Will return based on the magnitude disregarding the sign input.
- ***-ballContactPos***: Returns all events with a Ball Contact Pos - X of at least the amount input. Will return based on the magnitude disregarding the sign input.
- ***-frame***: Returns events with a contact on the specified frame. Accepts multiple space seperated inputs.
- ***-contactType***: Returns events with the specifed contact type. Accepted inputs: sour, nice, perfect
# Flags
### Event Result Flags (Only use one)
- ***-bunt***
- ***-sacFly***
- ***-strikeout***
- ***-groundBallDP***
- ***-errorChem***
- ***-errorInput***
- ***-walk***
- ***-walkHBP***
- ***-walkBB***
- ***-hit***
- ***-single***
- ***-double***
- ***-triple***
- ***-hr***
- **-steal**
- ***-caught***
- ***-caughtLineDrive***
- ***-out***
### Other Flags
- ***-starPitch***
- ***-bobble***
- ***-fiveStarDinger***
- ***-slidingCatch***
- ***-wallJump***
- ***-manualSelect***
- ***-walkoff***

# Example
`EventLookup.py --batter birdo --pitcher walu --inning 4 5`

# TODO
- Improve output flags
- Refactor event result flags to be an arguement
- Add additional parameters
- Add autocomplete for parameters
- Implement in RioBot?
