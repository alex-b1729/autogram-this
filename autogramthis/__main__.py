import argparse
from .autogram import Autogram


parser = argparse.ArgumentParser(
    prog='autogramthis',
    description='Searches for an autogram from an optional starting string.',
)
parser.add_argument(
    'prefix',
    type=str,
    nargs='?',
    default='',
    help='The text to begin the autogram sentence',
)
parser.add_argument(
    '-s',
    '--suffix',
    type=str,
    default='',
    help='The text to end the autogram sentence',
)
parser.add_argument(
    '-p',
    '--pangram',
    action='store_true',
    help='Search for a pangram - i.e. where every letter occurs at least once',
)
parser.add_argument(
    '--make-singular',
    action='store_true',
    help="Exclude the 's from letters with count greater than one",
)
parser.add_argument(
    '--no-and',
    action='store_true',
    help="Exclude the word 'and' from before the last character's count",
)

args = vars(parser.parse_args())

ag = Autogram(args['prefix'], args['suffix'])
ag.make_plural = not args['make_singular']
ag.include_final_and = not args['no_and']
ag.is_pangram = args['pangram']
ag.search()
