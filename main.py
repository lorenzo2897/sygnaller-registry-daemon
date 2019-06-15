#!/usr/bin/env python2

import BaseHTTPServer
import ssl
import urlparse
import json
import registry
import fcntl
import sys

r = registry.Registry()


class RegistryAPIServer(BaseHTTPServer.BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def _error(self, err):
        return {
            'error': err
        }

    def do_GET(self):
        url_string = urlparse.urlparse(self.path)
        params = urlparse.parse_qs(url_string.query)

        if 'action' not in params:
            resp = self._error('Missing action parameter')
        else:
            if 'register_device' in params['action']:
                resp = self.register_device(params)

            elif 'query_device' in params['action']:
                resp = self.query_device(params)

            elif 'list_devices' in params['action']:
                resp = self.list_devices()

            else:
                resp = self._error('Action not supported')

        self._set_headers()
        self.wfile.write(json.dumps(resp))

    def register_device(self, params):
        try:
            mac = params['mac'][0]
            ip = params['ip'][0]
            r.register(mac, ip)
            return {}
        except:
            return self._error('Invalid parameters')

    def query_device(self, params):
        try:
            mac = params['mac'][0]
            entry = r.query(mac)
            if entry is not None:
                return entry.toJSON()
            else:
                return self._error('Device not found')
        except:
            return self._error('Invalid parameters')

    def list_devices(self):
        try:
            return [entry.toJSON() for entry in r.db.itervalues()]
        except:
            return self._error('Invalid parameters')


def start_server(certificatePath=None, port=8000):
    server_address = ('', port)
    httpd = BaseHTTPServer.HTTPServer(server_address, RegistryAPIServer)
    if certificatePath is not None:
        httpd.socket = ssl.wrap_socket(httpd.socket, certfile=certificatePath, server_side=True)
    print 'Starting httpd on port %d...' % port
    httpd.serve_forever()


def main():
    start_server()  # (certificatePath='./server.pem', port=50123)


if __name__ == '__main__':
    main()
