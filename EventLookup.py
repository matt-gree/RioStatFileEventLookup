import RioStatLib
import json
import os
import argparse
import CharacterInputHandling as CHI
from functools import partial

event_parameters = ['Bunt',
                'Sac Fly',
                'Strikeout',
                'Ground Ball Double Play',
                'Error - Chem',
                'Error - Input',
                'Walk (Any)'
                'Walk HBP',
                'Walk BB',
                'Hit',
                'Single',
                'Double',
                'Triple',
                'HR',
                'RBI',
                'Steal',
                'Star Hits',
                'First Pitch of AB',
                'Full Count Pitch',
                'Star Pitch',
                'Bobble',
                'Five Star Dinger',
                'Sliding Catch',
                'Wall Jump',
                'First Fielder Position',
                'Manual Character Selection',
                'Batting Character', 
                'Pitching Character', 
                'Fielding Character']

def main():
    with open('config.json') as config:
        directory = json.load(config)['statDirectory']

    parser = argparse.ArgumentParser(prog='MSB Event Lookup',
                                    description='This program takes \
                                        user inputs and returns information \
                                        when events neeting the inputs occured')

    parser.add_argument('--bunt', action='store_true')
    parser.add_argument('--sacFly', action='store_true')
    parser.add_argument('--strikeout', action='store_true')
    parser.add_argument('--groudBallDP', action='store_true')
    parser.add_argument('--errorChem', action='store_true')
    parser.add_argument('--errorInput', action='store_true')
    parser.add_argument('--walk', action='store_true')
    parser.add_argument('--walkHBP', action='store_true')
    parser.add_argument('--walkBB', action='store_true')
    parser.add_argument('--hit', action='store_true')
    parser.add_argument('--single', action='store_true')
    parser.add_argument('--double', action='store_true')
    parser.add_argument('--triple', action='store_true')
    parser.add_argument('--hr', action='store_true')
    parser.add_argument('--rbi', action='store_true')
    parser.add_argument('--steal', action='store_true')
    parser.add_argument('--starHits', action='store_true')
    parser.add_argument('--startOfAB', action='store_true')
    parser.add_argument('--fullCountPitch', action='store_true')
    parser.add_argument('--starPitch', action='store_true')
    parser.add_argument('--bobble', action='store_true')
    parser.add_argument('--fiveStarDinger', action='store_true')
    parser.add_argument('--slidingCatch', action='store_true')
    parser.add_argument('--wallJump', action='store_true')
    parser.add_argument('--manualSelect', action='store_true')

    parser.add_argument('--batter')
    parser.add_argument('--pitcher')
    parser.add_argument('--fielder')
    
    parser.add_argument('--firstFielderPos')

    args = parser.parse_args()

    for filename in os.listdir(directory):
        stat_file = os.path.join(directory, filename)
        # checking if it is a file
        if (os.path.isfile(stat_file)) & (filename != ".DS_Store") & ('decoded' in filename):
            with open(stat_file, "r") as stats:
                jsonObj = json.load(stats)
                myStats = RioStatLib.StatObj(jsonObj)

                event_flags = {'bunt': myStats.successfulBuntEvents,
                    'sacFly':  myStats.sacFlyEvents,
                    'strikeout': myStats.strikeoutEvents,
                    'groundBallDP': myStats.groundBallDoublePlayEvents,
                    'errorChem': myStats.chemErrorEvents,
                    'errorInput': myStats.inputErrorEvents,
                    'walk': myStats.walkEvents,
                    'walkHBP': partial(myStats.walkEvents, include_bb=False),
                    'walkBB': partial(myStats.walkEvents, include_hbp=False),
                    'hit': myStats.hitEvents,
                    'single': partial(myStats.hitEvents, numberOfBases=1),
                    'double': partial(myStats.hitEvents, numberOfBases=2),
                    'triple': partial(myStats.hitEvents, numberOfBases=3),
                    'hr': partial(myStats.hitEvents, numberOfBases=4),
                    'rbi': myStats.rbiEvents,
                    'steal': myStats.stealEvents,
                    'starHits': myStats.starHitEvents,
                    'startOfAB': myStats.startOfAtBatEvents,
                    'fullCountPitch': myStats.fullCountPitchEvents,
                    'starPitch': myStats.starPitchEvents,
                    'bobble': myStats.bobbleEvents,
                    'fiveStarDinger': myStats.fiveStarDingerEvents,
                    'slidingCatch': myStats.slidingCatchEvents,
                    'wallJump': myStats.wallJumpEvents,
                    'manualSelect': myStats.manualCharacterSelectionEvents
                    }
                event_parameters = {
                    'firstFielderPos': myStats.positionFieldingEvents,
                    'batter': myStats.characterAtBatEvents,
                    'pitcher': myStats.characterPitchingEvents,
                    'fielder': myStats.characterFieldingEvents
                    }
                
                matchingEvents = set(range(myStats.eventFinal()+1))
                event_summary = []
                for arg, input in args.__dict__.items():
                    if input is (False or None):
                        continue
                    if input is True:
                        event_summary.append(arg)
                        flaggedEvents = event_flags[arg]()
                        matchingEvents = matchingEvents.intersection(flaggedEvents)
                    if arg in ['batter', 'pitcher', 'fielder']:
                        character = CHI.userInputToCharacter(input)
                        event_summary.append(f'{arg}: {character}')
                        flaggedEvents = event_parameters[arg](character)
                        matchingEvents = matchingEvents.intersection(flaggedEvents)
                    if arg == 'firstFielderPos':
                        event_summary.append(f'{arg}: {input}')
                        flaggedEvents = event_parameters[arg](input)
                        matchingEvents = matchingEvents.intersection(flaggedEvents)


                convert = lambda x: 'Top' if x == 0 else 'Bot'
                for event in matchingEvents:
                    print(f'{myStats.player(0)} at {myStats.player(1)} {myStats.startDate()}\n'
                            f'{convert(myStats.halfInningOfEvent(event))} {myStats.inningOfEvent(event)}   {myStats.outsOfEvent(event)} Out(s)   {myStats.ballsOfEvent(event)}-{myStats.strikesOfEvent(event)}\n'
                            f'{event_summary}\n')
if __name__ == "__main__":
    main() 