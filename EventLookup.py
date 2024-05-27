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
    parser.add_argument('--steal', action='store_true')
    parser.add_argument('--starPitch', action='store_true')
    parser.add_argument('--bobble', action='store_true')
    parser.add_argument('--fiveStarDinger', action='store_true')
    parser.add_argument('--slidingCatch', action='store_true')
    parser.add_argument('--wallJump', action='store_true')
    parser.add_argument('--manualSelect', action='store_true')
    parser.add_argument('--walkoff', action='store_true')
    parser.add_argument('--caught', action='store_true')
    parser.add_argument('--caughtLineDrive', action='store_true')
    parser.add_argument('--out', action='store_true')

    parser.add_argument('--firstFielderPos')

    parser.add_argument('--batter')
    parser.add_argument('--pitcher')
    parser.add_argument('--fielder')

    parser.add_argument('--battingPlayer')
    parser.add_argument('--pitchingPlayer')
    
    parser.add_argument('--inning', type=int, nargs='+')
    parser.add_argument('--chemOnBase', type=int, nargs='+')
    parser.add_argument('--halfInning')
    parser.add_argument('--outsInInning')
    parser.add_argument('--balls', type=int, nargs='+')
    parser.add_argument('--strikes', type=int, nargs='+')
    parser.add_argument('--rbi', type=int, nargs='+')
    parser.add_argument('--swingType')
    parser.add_argument('--ballStrikezonePos', type=float)
    parser.add_argument('--ballContactPos', type=float)
    parser.add_argument('--frame', type=int, nargs='+')
    parser.add_argument('--contactType', nargs='+')

    parser.add_argument('--runnersOnBase', type=int, nargs='+')


    args = parser.parse_args()

    for filename in os.listdir(directory):
        stat_file = os.path.join(directory, filename)
        # checking if it is a file
        if (os.path.isfile(stat_file)) & (filename != ".DS_Store") & ('decoded' in filename):
            with open(stat_file, "r") as stats:
                jsonObj = json.load(stats)
                myStats = RioStatLib.StatObj(jsonObj)

                event_flags = {
                    'bunt': myStats.buntResultEvents,
                    'sacFly':  myStats.sacFlyResultEvents,
                    'strikeout': myStats.strikeoutResultEvents,
                    'groundBallDP': myStats.groundBallDoublePlayResultEvents,
                    'errorChem': myStats.chemErrorResultEvents,
                    'errorInput': myStats.inputErrorResultEvents,
                    'walk': myStats.walkResultEvents,
                    'walkHBP': partial(myStats.walkResultEvents, include_bb=False),
                    'walkBB': partial(myStats.walkResultEvents, include_hbp=False),
                    'hit': myStats.hitResultEvents,
                    'single': partial(myStats.hitResultEvents, numberOfBases=1),
                    'double': partial(myStats.hitResultEvents, numberOfBases=2),
                    'triple': partial(myStats.hitResultEvents, numberOfBases=3),
                    'hr': partial(myStats.hitResultEvents, numberOfBases=4),
                    'steal': myStats.stealEvents,
                    'starPitch': myStats.starPitchEvents,
                    'bobble': myStats.bobbleEvents,
                    'fiveStarDinger': myStats.fiveStarDingerEvents,
                    'slidingCatch': myStats.slidingCatchEvents,
                    'wallJump': myStats.wallJumpEvents,
                    'manualSelect': myStats.manualCharacterSelectionEvents,
                    'walkoff': myStats.walkoffEvents,
                    'caught': myStats.caughtResultEvents,
                    'caughtLineDrive': myStats.caughtLineDriveResultsEvents,
                    'out': myStats.outResultEvents
                    }
                event_parameters = {
                    'firstFielderPos': myStats.positionFieldingEvents,
                    'batter': myStats.characterAtBatEvents,
                    'pitcher': myStats.characterPitchingEvents,
                    'fielder': myStats.characterFieldingEvents,
                    'inning': myStats.inningEvents,
                    'halfInning': myStats.halfInningEvents,
                    'runnersOnBase': myStats.runnerOnBaseEvents,
                    'outsInInning': myStats.outsInInningEvents,
                    'balls': myStats.ballEvents,
                    'strikes': myStats.strikeEvents,
                    'chemOnBase': myStats.chemOnBaseEvents,
                    'rbi': myStats.rbiEvents,
                    'battingPlayer': myStats.playerBattingEvents,
                    'pitchingPlayer': myStats.playerPitchingEvents,
                    'swingType': myStats.swingTypeEvents,
                    'ballStrikezonePos': myStats.ballPositionStrikezoneEvents,
                    'ballContactPos': myStats.ballContactPositionEvents,
                    'frame': myStats.contactFrameEvents,
                    'contactType': myStats.contactTypeEvents
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
                    if arg in ['firstFielderPos', 'inning', 'halfInning', 'runnersOnBase', 'balls', 'strikes', 'chemOnBase', 'rbi', 'battingPlayer', 'pitchingPlayer', 'swingType', 'ballStrikezonePos', 'ballContactPos', 'frame', 'contactType']:
                        event_summary.append(f'{arg}: {input}')
                        flaggedEvents = event_parameters[arg](input)
                        matchingEvents = matchingEvents.intersection(flaggedEvents)


                convert = lambda x: 'Top' if x == 0 else 'Bot'
                for event in matchingEvents:
                    print(f'{myStats.player(0)} at {myStats.player(1)} {myStats.statJson["Video Published"]}\n'
                            f'Batter: {myStats.batterOfEvent(event)}\n'
                            f'{convert(myStats.halfInningOfEvent(event))} {myStats.inningOfEvent(event)}   {myStats.outsOfEvent(event)} Out(s)   {myStats.ballsOfEvent(event)}-{myStats.strikesOfEvent(event)}\n'
                            f'{event_summary}\n')
if __name__ == "__main__":
    main() 