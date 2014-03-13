#!/usr/bin/env python
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import codecs
import logging
import pypuppetdb
import jinja2

log = logging.getLogger('puppetdb_stencil')

METAPARAMS = ('require', 'before', 'subscribe', 'notify', 'audit', 'loglevel',
        'noop', 'schedule', 'stage', 'alias', 'tag')

# Allow templates from anywhere on the filesystem
loader = jinja2.FileSystemLoader(['.', '/'])
environment = jinja2.Environment(trim_blocks=True, lstrip_blocks=True,
        loader=loader,
        extensions=['jinja2.ext.with_', 'jinja2.ext.loopcontrols'])

def render_resources(db, resource_type, template_names):
    resources = db.resources(resource_type)
    try:
        template = environment.select_template(templates)
    except jinja2.TemplatesNotFound:
        log.error('No template found for {0}'.format(resource_type))
    else:
        return template.render(resource_type=resource_type,
            resources=resources, metaparams=METAPARAMS)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='puppetdb_stencil')
    parser.add_argument('resource_types', metavar='RESOURCE_TYPE', nargs='+')
    parser.add_argument('--templates', '-t', metavar='TEMPLATE', nargs='*')
    parser.add_argument('--debug', '-d', action='store_true')
    parser.add_argument('--host', '-H', default='localhost')
    parser.add_argument('--port', '-p', default='8080')

    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.WARN)

    db = pypuppetdb.connect(host=args.host, port=args.port)

    for resource_type in args.resource_types:
        templates = ['{0}.jinja2'.format(resource_type)]
        if args.templates:
            templates += args.templates
        print(render_resources(db, resource_type, templates))
