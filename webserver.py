#!/usr/bin/env python

import sys, os
import BaseHTTPServer
from StringIO import StringIO
from SimpleHTTPServer import SimpleHTTPRequestHandler

# https://stackoverflow.com/questions/5896079/python-head-tail-and-backward-read-by-lines-of-a-text-file
class File(file):
    """ An helper class for file reading  """

    def __init__(self, *args, **kwargs):
        super(File, self).__init__(*args, **kwargs)
        self.BLOCKSIZE = 4096

    def head(self, lines_2find=1):
        self.seek(0)                            #Rewind file
        return [super(File, self).next() for x in xrange(lines_2find)]

    def tail(self, lines_2find=1):
        self.seek(0, 2)                         #Go to end of file
        bytes_in_file = self.tell()
        lines_found, total_bytes_scanned = 0, 0
        while (lines_2find + 1 > lines_found and
               bytes_in_file > total_bytes_scanned):
            byte_block = min(
                self.BLOCKSIZE,
                bytes_in_file - total_bytes_scanned)
            self.seek( -(byte_block + total_bytes_scanned), 2)
            total_bytes_scanned += byte_block
            lines_found += self.read(self.BLOCKSIZE).count('\n')
        self.seek(-total_bytes_scanned, 2)
        line_list = list(self.readlines())
        return line_list[-lines_2find:]

    def backward(self):
        self.seek(0, 2)                         #Go to end of file
        blocksize = self.BLOCKSIZE
        last_row = ''
        while self.tell() != 0:
            try:
                self.seek(-blocksize, 1)
            except IOError:
                blocksize = self.tell()
                self.seek(-blocksize, 1)
            block = self.read(blocksize)
            self.seek(-blocksize, 1)
            rows = block.split('\n')
            rows[-1] = rows[-1] + last_row
            while rows:
                last_row = rows.pop(-1)
                if rows and last_row:
                    yield last_row
        yield last_row

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.translate_path(self.path).endswith('/'):
            f = File('/var/log/LOCAL7.log')
            local7 = f.tail(10)
            f.close()

            f = File('/var/log/LOCAL6.log')
            local6 = f.tail(10)
            f.close()

            image_files = os.listdir('.')
            image_files = [f for f in image_files if f.endswith('.jpg') and os.path.isfile(f)]
            image_files.sort(reverse=True)

            body = '<html><table style="position: absolute; top: 0; bottom: 0; left: 0; right: 0;"><tr><td style="width: 25%" valign="top">\n<h1>Reboots</h1><pre>\n'
            body += ''.join(local7)
            body += '</pre>\n<h1>Camera</h1><pre>\n'
            body += ''.join(local6)
            body += '</pre>\n<h1>Last shots</h1>\n'
            for f in image_files[:9]:
                body += ''.join( [
                    '<a href="',
                    f,
                    '\">',
                    f,
                    '</a> ',
                    str(os.stat(f).st_size),
                    '<br>\n'
                    ] )
            body += '</td>\n<td style="width: 75%">'
            body += '<img src="' + image_files[0] + '" style="display:block; width:100%; height:auto;"></img>'
            body += '</td>\n</tr></table></html>'
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        # fallback
        return SimpleHTTPRequestHandler.do_GET(self)

os.chdir('/home/pi/timelapse/01/');

HandlerClass = MyHandler
ServerClass  = BaseHTTPServer.HTTPServer
Protocol     = 'HTTP/1.0'

if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8000
server_address = ('', port)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)

sa = httpd.socket.getsockname()
print 'Serving HTTP on', sa[0], 'port', sa[1], '...'
httpd.serve_forever()
