import argparse
import os


def parse():
    parser = argparse.ArgumentParser()

    # position arguments
    parser.add_argument('url')

    # option arguments
    parser.add_argument('-o', '--output',
                        default=os.getcwd())
    args = parser.parse_args()
    return args
