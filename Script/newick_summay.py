#!/usr/bin/env python

import sys
from ete3 import Tree

usage = \
"""

    USAGE: newick_summary.pl < input tree > output stat
"""

t = Tree(sys.stdin.read())
print len(t.get_leaf_names())

exit()
