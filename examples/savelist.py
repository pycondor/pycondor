#!/usr/bin/env python

import argparse

if __name__ == "__main__":
    '''
    Example script that generates and saves a list to file
    '''

    parser = argparse.ArgumentParser(description='Generates and saves a list to file')
    parser.add_argument('--length', dest='length', type=int, default=10,
                        help='Length of list to be generated and saved')
    args = parser.parse_args()

    print('Saving range({})...'.format(args.length))
    with open('range_{}'.format(args.length), 'wb') as outputfile:
        for i in range(args.length):
          outputfile.write('{}\n'.format(i))
