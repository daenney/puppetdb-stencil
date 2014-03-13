################
puppetdb_stencil
################

When passed one or more resource types those resources are rendered through templates. The templates are loaded based on a template matching the exact resource type name with a .jinja2 extension or an optionally passed template.

.. code-block:: bash

   $ python puppetdb_stencil.py mytype

A more complex example that renders multiple types through a shared template:

.. code-block:: bash

   $ python puppetdb_stencil.py nagios_host nagios_hostgroup -t examples/nagios_.jinja2

Template selection
------------------

The jinja2 loader is used to first search in the current directory and then the absolute path. This is done for every template specified. A template name is generated for the current resource type name.

.. code-block:: bash

   $ python puppetdb_stencil.py nagios_host -t examples/nagios_.jinja2

This looks in these places:

* ``nagios_host.jinja2``
* ``/nagios_host.jinja2``
* ``examples/nagios_.jinja2``
* ``/examples/nagios_.jinja2``

Installation
------------

This project requires pypuppetdb and Jinja2 to function. On Python 2.6 it additionally requires argparse.

.. code-block:: bash

   $ pip install -r requirements.txt
