#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import logging, re

class FrameSelector(object):

    def __init__ (self, infile):
        self.match_tuples = []
        with open(infile, 'r') as ff:
            for line in ff:
                line = re.sub (r'#.*$', '', line.strip())
                line = line.strip()
                if line != '':
                    m = re.match (r'^\s*(\d+)\s*(-?)\s*(\d*)\s*(.*)\s*$', line)
                    if not m:
                        logging.warn ('unable to parse file %s line "%s"', infile, line)
                        continue
                    m1 = m2 = int(m.group(1))
                    if m.group(2) != '':
                        if m.group(3) == '':
                            m2 = None
                        else:
                            m2 = int(m.group(3))
                    m3 = m.group(4)
                    self.match_tuples.append((m1, m2, m3))
        self.match_tuples.reverse()

    def find (self, i):
        mmt = None
        for mt in self.match_tuples:
            logging.debug ('checking %s against %s', i, str(mt))
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
        return mmt
