#!/usr/bin/env python
import argparse
import os
import server

def cli():
    p = argparse.ArgumentParser()

    p.add_argument('-d', help='debug mode', dest='debug', action='store_true')
    p.add_argument('-c', help='set config environment', dest='config')
    p.add_argument('-p', help='port', dest='port', default=8080)
    p.add_argument('--raise', help='raise errors', dest='raise_errors', action='store_true')
    p.add_argument('--reset', help='reset db', dest='reset', action='store_true')

    args = p.parse_args()

    # setup environment
    if args.config:
        assert os.path.exists(args.config), 'bad config fp "{}"'.format(args.config)
    else:
        args.config = './local/server-config-dev.yaml'

    os.environ['FLASK_CONFIG'] = os.path.abspath(args.config)

    if args.reset:
        server.reset_db()
    else:
        app = server.create_app(debug=args.debug, raise_errors=args.raise_errors)
        app.run(port=int(args.port))

if __name__ == '__main__':
    cli()
