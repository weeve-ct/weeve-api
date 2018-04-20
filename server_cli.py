#!/usr/bin/env python
import argparse
import os
import server

def cli():
    p = argparse.ArgumentParser()
    p.add_argument('-c', help='set config environment', dest='config')

    s = p.add_subparsers(dest='which')

    sp = s.add_parser('run', help='run dev server')
    sp.add_argument('-d', help='debug mode', dest='debug', action='store_true')
    sp.add_argument('-p', help='port', dest='port', default=8080)
    sp.add_argument('-r','--raise', help='raise errors', dest='raise_errors', action='store_true')

    sp = s.add_parser('reset', help='reset db')
    sp.add_argument('--reset', help='reset db', dest='reset', action='store_true')

    sp = s.add_parser('routes', help='reset db')

    args = p.parse_args()

    # setup environment
    if args.config:
        assert os.path.exists(args.config), 'bad config fp "{}"'.format(args.config)
    else:
        args.config = './local/server-config-dev.yaml'

    os.environ['FLASK_CONFIG'] = os.path.abspath(args.config)

    if args.which == 'reset':
        server.reset_db()

    elif args.which == 'run':
        app = server.create_app(debug=args.debug, raise_errors=args.raise_errors)
        app.run(port=int(args.port))

    elif args.which == 'routes':
        for route in server.get_rules():
            print(route)

if __name__ == '__main__':
    cli()
