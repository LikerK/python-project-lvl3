import argparse


def parse():
    parser = argparse.ArgumentParser()

    # position arguments
    parser.add_argument('url')

    # option arguments
    parser.add_argument('-o', '--output',
                        default='')
    args = parser.parse_args()
    return args
