#!/usr/bin/env python

import argparse
import os
import stat

parser = argparse.ArgumentParser()
parser.add_argument('--module', required=True, help='The module containing the program implementation')
parser.add_argument('--outdir', required=True, help='The directory to generate the script in')
parser.add_argument('--execname', required=True, help='The name of the executable script to generate')
args = parser.parse_args()

if not os.path.exists(args.outdir):
    os.makedirs(args.outdir)
if not os.path.isdir(args.outdir):
    print 'Cannot create output directory', args.outdir
    exit(1)

template = """\
#!/usr/bin/env python
# Automatically generated file: do not modify!

from ElementsKernel.Program import Program

p = Program('%(MODULE_NAME)s')
exit(p.runProgram())
""" % { 'MODULE_NAME' : args.module }

filename = args.outdir + os.sep + args.execname

with open(filename, 'w') as f:
    f.write(template)
os.chmod(filename, os.stat(filename).st_mode | stat.S_IEXEC)