import sys
import argparse
from clanrewarddistribution import ClanRewardsDistributor


def main() -> int:
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('-d', '--data', default='.')
    argument_parser.add_argument('-r', '--rewards', default='.')
    args = vars(argument_parser.parse_args())

    print(args)

    ClanRewardsDistributor(args['data'], args['rewards']).distribute_clan_rewards()


if __name__ == '__main__':
    sys.exit(main())
