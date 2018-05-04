#!/usr/bin/env python
import argparse
import os

def cli():
    p = argparse.ArgumentParser()

    p.add_argument('-c', help='set config environment', dest='config')

    s = p.add_subparsers(dest='which')

    sp = s.add_parser('run', help='run dev server')
    sp.add_argument('-d', help='debug mode', dest='debug', action='store_true')
    sp.add_argument('-p', help='port', dest='port', default=8080)
    sp.add_argument('-r','--raise', help='raise errors', dest='raise_errors', action='store_true')

    sp = s.add_parser('db', help='db commands')
    sp.add_argument('--reset', help='reset db', dest='reset', action='store_true')
    sp.add_argument('--create', help='create db', dest='create', action='store_true')

    sp = s.add_parser('routes', help='list routes')

    sp = s.add_parser('nltk', help='nltk setup')
    sp.add_argument('-i', '--install', help='install nltk dependencies', dest='nltk_install', action='store_true')

    args = p.parse_args()

    # setup environment
    if args.config:
        assert os.path.exists(args.config), 'bad config fp "{}"'.format(args.config)
        os.environ['FLASK_CONFIG'] = os.path.abspath(args.config)
    else:
        if 'FLASK_CONFIG' not in os.environ:
            args.config = './local/server-config-dev.yaml'
            os.environ['FLASK_CONFIG'] = os.path.abspath(args.config)

    if args.which == 'db':
        if args.reset:
            import server
            server.reset_db()
        elif args.create:
            import server 
            server.create_db()

    elif args.which == 'run':
        import server
        app = server.create_app(debug=args.debug, raise_errors=args.raise_errors)
        app.run(port=int(args.port))

    elif args.which == 'routes':
        import server
        for route in server.get_rules():
            print(route)

    elif args.which == 'nltk':
        if args.nltk_install:
            import nltk
            nltk.download('stopwords')
            nltk.download('punkt')
            nltk.download('averaged_perceptron_tagger')
            nltk.download('wordnet')

if __name__ == '__main__':
    cli()
