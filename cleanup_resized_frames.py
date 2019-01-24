#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import os, argparse, traceback

from FrameSelector import FrameSelector

def is_valid_directory(parser, arg):
    arg = os.path.abspath(arg)
    if not os.path.exists(arg):
        parser.error("%s does not exist!" % arg)
    elif not os.path.isdir(arg):
        parser.error("%s is not a directory!" % arg)
    else:
        return arg

def is_existing_file(parser, arg):
    arg = os.path.abspath(arg)
    if not os.path.exists(arg):
        parser.error("%s does not exist!" % arg)
    else:
        return arg

class argparse_logger(argparse.ArgumentParser):
    def error(self, message):
        logging.error(message)
        argparse.ArgumentParser.error(self, message)
        
def log_uncaught_exceptions(ex_cls, ex, tb):
    logging.critical(''.join(traceback.format_tb(tb)))
    logging.critical('{0}: {1}'.format(ex_cls, ex))

if __name__ == '__main__':
    import logging, sys, re, subprocess

    logging.basicConfig (level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')

    sys.excepthook = log_uncaught_exceptions

    parser = argparse_logger(description='Make a directory of symlinks to feed ffmpeg')
    parser.add_argument('--resize-directory', required=True, help='resize directory', type = lambda x : is_valid_directory(parser, x))
    parser.add_argument('--filter-file', required=True, help='filter file', type = lambda x : is_existing_file(parser, x))

    parser.add_argument('--verbose', action='count', help='crank up logging')

    args = parser.parse_args()

    if args.verbose > 0:
        logging.getLogger().setLevel(logging.DEBUG)

    frame_filter = FrameSelector(args.filter_file)

    for infile in sorted(os.listdir(args.resize_directory)):
        m = re.match(r'^(\d+)_(\d{8})-(\d{2})(\d{2})\d{2}\.(jpg|png)$', infile)
        if not m:
            logging.info ('skipping %s, does not look like an image file', infile)
            continue
        else:
            i = int(m.group(1))
            d = m.group(2)
            h = m.group(3)
            m = m.group(4)
            mmt = frame_filter.find(i)
            if mmt is None:
                inpath = os.path.join(args.resize_directory, infile)
                logging.info ('%s did not match any files', inpath)
                os.remove(inpath)
