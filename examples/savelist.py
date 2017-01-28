#!/usr/bin/env python3

import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generates and saves a list to file')
    parser.add_argument('--length', dest='legnth', type=int, default=10,
                        help='Length of list to be generated and saved')
    args = parser.parse_args()

    with open('range_{}'.format(args.length), 'wb') as outputfile:
        outputfile.writelines(range(args.length))
