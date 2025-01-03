import json
import os
import argparse
from functools import partial

from project_rio_lib.stat_file_parser import StatObj, EventObj
from event_search_class import EventSearch
import CharacterInputHandling as CHI

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
                game_stats = StatObj(jsonObj)
                events_search = EventSearch(game_stats)

                event_flags = {
                    'bunt': events_search.buntResultEvents,
                    'sacFly':  events_search.sacFlyResultEvents,
                    'strikeout': events_search.strikeoutResultEvents,
                    'groundBallDP': events_search.groundBallDoublePlayResultEvents,
                    'errorChem': events_search.chemErrorResultEvents,
                    'errorInput': events_search.inputErrorResultEvents,
                    'walk': events_search.walkResultEvents,
                    'walkHBP': partial(events_search.walkResultEvents, include_bb=False),
                    'walkBB': partial(events_search.walkResultEvents, include_hbp=False),
                    'hit': events_search.hitResultEvents,
                    'single': partial(events_search.hitResultEvents, numberOfBases=1),
                    'double': partial(events_search.hitResultEvents, numberOfBases=2),
                    'triple': partial(events_search.hitResultEvents, numberOfBases=3),
                    'hr': partial(events_search.hitResultEvents, numberOfBases=4),
                    'steal': events_search.stealEvents,
                    'starPitch': events_search.starPitchEvents,
                    'bobble': events_search.bobbleEvents,
                    'fiveStarDinger': events_search.fiveStarDingerEvents,
                    'slidingCatch': events_search.slidingCatchEvents,
                    'wallJump': events_search.wallJumpEvents,
                    'manualSelect': events_search.manualCharacterSelectionEvents,
                    'walkoff': events_search.walkoffEvents,
                    'caught': events_search.caughtResultEvents,
                    'caughtLineDrive': events_search.caughtLineDriveResultsEvents,
                    'out': events_search.outResultEvents
                    }
                event_parameters = {
                    'firstFielderPos': events_search.positionFieldingEvents,
                    'batter': events_search.characterAtBatEvents,
                    'pitcher': events_search.characterPitchingEvents,
                    'fielder': events_search.characterFieldingEvents,
                    'inning': events_search.inningEvents,
                    'halfInning': events_search.halfInningEvents,
                    'runnersOnBase': events_search.runnerOnBaseEvents,
                    'outsInInning': events_search.outsInInningEvents,
                    'balls': events_search.ballEvents,
                    'strikes': events_search.strikeEvents,
                    'chemOnBase': events_search.chemOnBaseEvents,
                    'rbi': events_search.rbiEvents,
                    'battingPlayer': events_search.playerBattingEvents,
                    'pitchingPlayer': events_search.playerPitchingEvents,
                    'swingType': events_search.swingTypeEvents,
                    'ballStrikezonePos': events_search.ballPositionStrikezoneEvents,
                    'ballContactPos': events_search.ballContactPositionEvents,
                    'frame': events_search.contactFrameEvents,
                    'contactType': events_search.contactTypeEvents
                    }
                
                matchingEvents = set(range(game_stats.final_event()+1))
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
                    event_obj = EventObj(game_stats, event)
                    print(f'{game_stats.player(0)} at {game_stats.player(1)} {game_stats.statJson["Video Published"]}\n'
                            f'Batter: {event_obj.batter()}\n'
                            f'{convert(event_obj.half_inning())} {event_obj.inning()}, {event_obj.outs()} Out(s), {event_obj.balls()} Ball(s), {event_obj.strikes()} Strike(s)\n'
                            f'{event_summary}\n')
                    
if __name__ == "__main__":
    main()