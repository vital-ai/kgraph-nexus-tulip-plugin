import sys
import os

# this didn't work

current_dir = os.path.dirname(os.path.abspath(__file__))

packages_dir = os.path.join(current_dir, 'packages')

if packages_dir not in sys.path:
    sys.path.append(packages_dir)
