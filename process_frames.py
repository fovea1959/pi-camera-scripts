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
    import logging, sys, re, subprocess

    logging.basicConfig (level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')

    sys.excepthook = log_uncaught_exceptions

    parser = argparse_logger(description='Make a directory of symlinks to feed ffmpeg')
    parser.add_argument('--input-directory', required=True, help='input directory', type = lambda x : is_valid_directory(parser, x))
    parser.add_argument('--symlink-directory', help='symlink directory', type = lambda x : is_valid_directory(parser, x))
    parser.add_argument('--resize-directory', help='resize directory', type = lambda x : is_valid_directory(parser, x))
    parser.add_argument('--filter-file', required=True, help='filter file', type = lambda x : is_existing_file(parser, x))
    parser.add_argument('--script', help='file to put shell script into')

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

    sf = None
    if args.script:
        sf = open (args.script, 'w')

    last_date = None
    for infile in sorted(os.listdir(args.input_directory)):
        m = re.match(r'^(\d+)_(\d{8})-.*\.jpg$', infile)
        if not m:
            logging.info ('skipping %s, does not look like an image file', infile)
            continue
        else:
            i = int(m.group(1))
            d = m.group(2)
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
                inpath = os.path.join(args.input_directory, infile)
                logging.info ('%s matched %s', inpath, str(mmt))
                if args.symlink_directory:
                    os.symlink (inpath, os.path.join(args.symlink_directory, infile))
                if args.resize_directory:
                    if last_date is not None and d < last_date:
                        # clock regressed
                        d = last_date
                    else:
                        last_date = d
                    outfilename = os.path.join(args.resize_directory, infile);
                    outfilename = os.path.splitext(outfilename)[0] + '.png'
                    if os.path.exists(outfilename):
                        logging.info ('%s already exists, skipping conversion', outfilename)
                    else:
                            legend = '  ' + d[:4] + '.' + d[4:6] + '.' + d[6:] + '  '
                            undercolor = '#00000080'
                            if sf:
                                legend = '"' + legend + '"'
                                undercolor = '"' + undercolor + '"'
                            cmd = [
                                'convert', inpath, 
                                '-resize', '1280x720', 
                                '-pointsize', '72', 
                                '-fill',  'white',   '-undercolor',  undercolor , '-gravity', 'South', '-annotate', '+0+5', legend, 
                                outfilename
                            ]
                            if sf:
                                sf.write(' '.join(cmd))
                                sf.write('\n');
                            else:
                                try:
                                    logging.info ('running %s', ' '.join(cmd))
                                    r = subprocess.check_call (cmd, stderr=subprocess.STDOUT)
                                except subprocess.CalledProcessError as exc:
                                    logging.critical ("imagemagick failed: %d %s", exc.returncode, exc.output)
                                    raise

            else:
                logging.info ('%s no match', infile)
