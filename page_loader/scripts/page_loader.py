#!/usr/bin/env python3
from page_loader.parser import parse
from page_loader.loader import downloads


def main():
    result = parse()
    page_loader = downloads(result.url, result.output)
    print(page_loader)


if __name__ == '__main__':
    main()
