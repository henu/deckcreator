#!/usr/bin/env python3
import json
import os
import sys

from creator import Creator


def main(input_path, output_path):
    with open(input_path, 'r') as f:
        input_data = json.load(f)

    creator = Creator(input_data['style'])

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for card_name, card_data in input_data['cards'].items():
        creator.create_card(
            os.path.join(output_path, card_name + '.png'),
            card_data,
        )


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {} <INPUT JSON FILE> <OUTPUT DIRECTORY>'.format(sys.argv[0]))
        sys.exit(1)
    else:
        main(sys.argv[1], sys.argv[2])
