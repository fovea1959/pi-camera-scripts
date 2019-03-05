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
    parser.add_argument('--input-directory', required=True, help='input directory', type = lambda x : is_valid_directory(parser, x))
    parser.add_argument('--symlink-directory', help='symlink directory', type = lambda x : is_valid_directory(parser, x))
    parser.add_argument('--resize-directory', help='resize directory', type = lambda x : is_valid_directory(parser, x))
    parser.add_argument('--filter-file', required=True, help='filter file', type = lambda x : is_existing_file(parser, x))
    parser.add_argument('--script', required=True, help='file to put shell script into')
    parser.add_argument('--timestamp', action='store_true', help='Add a timestamp to the output frames')
    parser.add_argument('--start', help='First date to convert')
    parser.add_argument('--end', help='Last date to convert')

    parser.add_argument('--verbose', action='count', help='crank up logging')

    args = parser.parse_args()

    if args.verbose > 0:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.input_directory == args.resize_directory:
        logging.critical ('--input-directory and --resize-directory cannot be the same')
        sys.exit(1)

    if args.symlink_directory:
        if args.input_directory == args.symlink_directory:
            logging.critical ('--input-directory and --symlink-directory cannot be the same')
            sys.exit(1)

        current_contents_of_symlink_directory = os.listdir(args.symlink_directory)
        if len(current_contents_of_symlink_directory) > 0:
            logging.critical ('--symlink-directory %s is not empty', args.symlink_directory)
            sys.exit(1)

    frame_filter = FrameSelector(args.filter_file)

    sf = None
    if args.script:
        sf = open (args.script, 'w')

    last_date = None
    for infile in sorted(os.listdir(args.input_directory)):
        m = re.match(r'^(\d+)_(\d{8})-(\d{2})(\d{2})\d{2}\.jpg$', infile)
        if not m:
            logging.info ('skipping %s, does not look like an image file', infile)
            continue
        else:
            i = int(m.group(1))
            d = m.group(2)
            if args.start and d < args.start:
                continue
            if args.end and d > args.end:
                continue
            h = m.group(3)
            m = m.group(4)
            mmt = frame_filter.find(i)
            if mmt is not None:
                inpath = os.path.join(args.input_directory, infile)
                logging.debug ('%s matched %s', inpath, str(mmt))
                if args.symlink_directory:
                    os.symlink (inpath, os.path.join(args.symlink_directory, infile))
                if args.resize_directory:
                    if last_date is not None and d < last_date:
                        # clock regressed
                        d = last_date
                        ts = None
                    else:
                        last_date = d
                        ts = str(int(h)-4) + ":" + str(m)
                    outfilename = os.path.join(args.resize_directory, infile);
                    outfilename = os.path.splitext(outfilename)[0] + '.png'
                    if os.path.exists(outfilename):
                        logging.debug ('%s already exists, skipping conversion', outfilename)
                    else:
                        date_legend = '" ' + d[:4] + '.' + d[4:6] + '.' + d[6:] + ' "'
                        undercolor = '"#00000080"'
                        cmd = [
                            'convert', inpath, 
                            '-resize', '1280x720', 
                            #'-resize', '640x360', 
                            '-fill',  'white',   '-undercolor',  undercolor , 
                            '-pointsize', '72', 
                            '-gravity', 'South', '-annotate', '+0+5', date_legend, 
                            '-pointsize', '36', 
                            '-gravity', 'SouthWest', '-annotate', '+0+5', '{:05d}'.format(i), 
                        ]
                        if args.timestamp and ts is not None:
                            cmd.extend([ '-gravity', 'SouthEast', '-annotate', '+0+5', ts ])
                        cmd.append(outfilename)
                        sf.write(' '.join(cmd))
                        sf.write('\n')

            else:
                logging.debug ('%s no match', infile)
