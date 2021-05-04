#!/usr/bin/env python

"""pyspinmanager

maintain spinnaker application and pipeline

Usage:
  pyspinmanager <module> <func> [<args>...]

Options:
  -h --help            Show this screen.
"""

from docopt import docopt
import sys
import pyspinmanager.spin_scripts
from pyspinmanager.spin_scripts import *

def main():
    """
    run module

    example:
    pyrpmsepc java <git_url> <version>
    """
    args = docopt(__doc__, options_first=True)
    module = args['<module>']
    func = args['<func>']
    argv = [module, func]+args['<args>']
    module_script = getattr(pyspinmanager.spin_scripts, module)
    module_args = docopt(module_script.__doc__, argv=argv)
    return getattr(module_script, func)(module_args)

if __name__ == '__main__':
    main()
