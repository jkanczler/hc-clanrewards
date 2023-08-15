import sys
import argparse
from clanrewarddistribution import ClanRewardsDistributor


def main() -> int:
    argument_parser = argparse.ArgumentParser(
        prog='clanrewarddistributor',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''
Segít szétosztani a jutalmakat egy Hustle Castle klánnak.

Adat fájlok, amiket az alkalmazás mellé kell helyezni:
    - config.json:
        number_of_rewards: mennyi jutalmat oszt ki klántagonként
        item_price: mennyibe kerül egy tárgy (ennyi glory kerül levonásra tárgyanként)

        Például:
        {
            "number_of_rewards": 3,
            "item_price": 50000
        }

    - items.json: a jutalmak listája, hogy milyen tárgyból mennyi van

        Például:
        {
            "totem_lego": 3,
            "gem_dodge": 1
        }

    - clan_mates.json: a klántagok és kívánságaik:

        "name": A játékos neve
        "glory": A szerzett glory
        "demands": A kívánság lista
            "items": a tárgyak listája, amit kér
            "quantity": mennyit kér a tárgyakból

        Például:
        {
            "clan_mates": [
                {
                    "name": "Ayrisz",
                    "glory": 334065,
                    "demands": [
                        { "items": ["spirit_lego"], "quantity": 1 },
                        { "items": ["spirit_epic"], "quantity": 1 },
                        { "items": ["dia_100"], "quantity": 1 },            
                        { "items": ["clan_coin"], "quantity": 1 },
                        { "items": ["badge"], "quantity": 1 }
                    ]
                },
                {
                    "name": "KisCsako88",
                    "glory": 298889,
                    "demands": [
                        { "items": ["spirit_lego"], "quantity": 2 },
                        { "items": ["essence_eclipse"], "quantity": 1 },
                        { "items": ["dia_100", "dia_50"], "quantity": 2 },
                        { "items": ["spirit_epic"], "quantity": 1 },
                        { "items": ["essence_bastion"], "quantity": 1 },
                        { "items": ["fury_of_the_stars"], "quantity": 1 }
                    ]
                }
            ]
        }
''',
        epilog='Készítette: Josh Rusher (Magyar Végvárak)')

    argument_parser.add_argument('-d', '--data', default='.', help='A könyvtár helye, mely a szükséges adatokat tartalmazza.')
    argument_parser.add_argument('-r', '--rewards', default='.', help='A könyvtár helye, ahová az alkalmazás a szétosztás eredményét tartalmazó fájlt generálja.')
    argument_parser.add_argument('-v', '--version', action='version', version='%(prog)s v1.0')
    args = vars(argument_parser.parse_args())

    print(args)

    ClanRewardsDistributor(args['data'], args['rewards']).distribute_clan_rewards()


if __name__ == '__main__':
    sys.exit(main())
