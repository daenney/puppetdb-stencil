#!/usr/bin/env python
"""
puppetdb-stencil is a tool to render puppet resources using templates.
"""

from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging
import pypuppetdb
import jinja2

LOG = logging.getLogger('puppetdb_stencil')

METAPARAMS = ('require', 'before', 'subscribe', 'notify', 'audit', 'loglevel',
              'noop', 'schedule', 'stage', 'alias', 'tag')

# Allow templates from anywhere on the filesystem
LOADER = jinja2.FileSystemLoader(['.', '/'])
EXTENSIONS = ['jinja2.ext.with_', 'jinja2.ext.loopcontrols']
ENVIRONMENT = jinja2.Environment(trim_blocks=True, lstrip_blocks=True,
                                 loader=LOADER, extensions=EXTENSIONS)


def render_resources(database, resource_type, template_names):
    """
    Render resources of the given type. They are queried from the given
    database and rendered using the first template from template_names that can
    be loaded.
    """
    resources = database.resources(resource_type)
    try:
        template = ENVIRONMENT.select_template(template_names)
    except jinja2.TemplatesNotFound:
        LOG.error('No template found for {0}'.format(resource_type))
    else:
        return template.render(resource_type=resource_type,
                               resources=resources, metaparams=METAPARAMS)


def main():
    """
    Main function
    """
    parser = argparse.ArgumentParser(prog='puppetdb_stencil')
    parser.add_argument('resource_types', metavar='RESOURCE_TYPE', nargs='+')
    parser.add_argument('--templates', '-t', metavar='TEMPLATE', nargs='*')
    parser.add_argument('--debug', '-d', action='store_true')
    parser.add_argument('--host', '-H', default='localhost')
    parser.add_argument('--port', '-p', default='8080')

    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.WARN)

    database = pypuppetdb.connect(host=args.host, port=args.port)

    for resource_type in args.resource_types:
        templates = ['{0}.jinja2'.format(resource_type)]
        if args.templates:
            templates += args.templates
        print(render_resources(database, resource_type, templates))


if __name__ == '__main__':
    main()
