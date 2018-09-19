#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import os, argparse, traceback

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
    import argparse, logging, os, sys, re

    logging.basicConfig (level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')

    sys.excepthook = log_uncaught_exceptions

    parser = argparse_logger(description='Make a directory of symlinks to feed ffmpeg')
    parser.add_argument('--input-directory', required=True, help='input directory', type = lambda x : is_valid_directory(parser, x))
    parser.add_argument('--output-directory', required=True, help='output directory', type = lambda x : is_valid_directory(parser, x))
    parser.add_argument('--filter-file', required=True, help='filter file', type = lambda x : is_existing_file(parser, x))

    parser.add_argument('--verbose', action='count', help='crank up logging')

    args = parser.parse_args()

    if args.verbose > 0:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.input_directory == args.output_directory:
        logging.critical ('--input-directory and --output-directory cannot be the same')
        sys.exit(1)

    current_contents_of_output_directory = os.listdir(args.output_directory)
    if len(current_contents_of_output_directory) > 0:
        logging.critical ('--output-directory %s is not empty', args.output_directory)
        sys.exit(1)

    match_tuples = []
    with open(args.filter_file, 'r') as ff:
        for line in ff:
            line = re.sub (r'#.*$', '', line.strip())
            line = re.sub('\s', '', line)
            if line != '':
                m = re.search (r'[^0123456789-]', line)
                if m:
                    logging.warn ('bad character "%s" in filter file line "%s"', m.group(0), line)
                    continue
                m = re.match (r'^(\d+)(-?)(\d*)$', line)
                if not m:
                    logging.critical ('trouble picking the numbers out of "%s"', line)
                    sys.exit(1)
                else:
                    print line
                    m1 = m2 = int(m.group(1))
                    if m.group(2) != '':
                        if m.group(3) == '':
                            m2 = None
                        else:
                            m2 = int(m.group(3))
                    match_tuples.append((m1, m2))

    for infile in sorted(os.listdir(args.input_directory)):
        m = re.match(r'^(\d+)_', infile)
        if not m:
            logging.info ('skipping %s, no digits at front', infile)
            continue
        else:
            i = int(m.group(1))
            mmt = None
            for mt in match_tuples:
                logging.debug ('checking %s against %s %s', i, str(mt), infile)
                if mt[1] is None:
                    logging.debug ('checking %d >= %d', i, mt[0])
                    if i >= mt[0]:
                        mmt = mt
                        break
                else:
                    logging.debug ('checking %d >= %d & <= %d', i, mt[0], mt[1])
                    if i >= mt[0] and i <= mt[1]:
                        mmt = mt
                        break
            if mmt is not None:
                logging.info ('%s matched %s', infile, str(mmt))
                os.symlink (os.path.join(args.input_directory, infile), os.path.join(args.output_directory, infile))
            else:
                logging.info ('%s no match', infile)


