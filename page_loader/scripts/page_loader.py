#!/usr/bin/env python3
from page_loader import args
from page_loader.loader import download
import logging
import sys


logger = logging.getLogger(__name__)


def main():
    logger.info("program started")
    parsed_args = args.parse()
    try:
        result = download(parsed_args.url, parsed_args.output)
    except Exception as error:
        print(f'Unable to upload {parsed_args.url}')
        print(f'During execution the following error occurs: {error}')
        logger.exception(msg=f'Unable to download {args.url}')
        sys.exit(1)
    else:
        logger.info(f'Program finished, received path {result}')
        print(f'Page successfully downloaded into {result}')
        sys.exit(0)


if __name__ == '__main__':
    main()
