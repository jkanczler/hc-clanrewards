import sys
from clanrewarddistribution import ClanRewardsDistributor


def main() -> int:
    ClanRewardsDistributor().distribute_clan_rewards()


if __name__ == '__main__':
    sys.exit(main())
