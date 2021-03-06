
from sys import stdout
from os import pathsep, listdir, environ, fdopen
from os.path import exists, isdir, realpath
from optparse import OptionParser, OptionValueError
from tempfile import mkstemp
from zipfile import is_zipfile


def stripPath(path):
    collected = []
    for p in path.split(pathsep):
        rp = realpath(p)
        # We keep the entry if it is a directory not empty or a zipfile
        try:
            if exists(rp) and ((isdir(rp) and listdir(rp))
                               or is_zipfile(rp)) and p not in collected:
                collected.append(p)
        except OSError:
            pass
    return pathsep.join(collected)


def cleanVariable(varname, shell, out):
    if varname in environ:
        pth = stripPath(environ[varname])
        if shell == "csh" or shell.find("csh") != -1:
            out.write("setenv %s %s\n" % (varname, pth))
        elif shell == "sh" or shell.find("sh") != -1:
            out.write("export %s=%s\n" % (varname, pth))
        elif shell == "bat":
            out.write("set %s=%s\n" % (varname, pth))


def _check_output_options_cb(option, opt_str, value, parser):
    if opt_str == "--mktemp":
        if parser.values.output != stdout:
            raise OptionValueError(
                "--mktemp cannot be used at the same time as --output")
        else:
            parser.values.mktemp = True
            fd, outname = mkstemp()
            parser.values.output = fdopen(fd, "w")
            print(outname)
    elif opt_str == "--output" or opt_str == "-o":
        if parser.values.mktemp:
            raise OptionValueError(
                "--mktemp cannot be used at the same time as --output")
        else:
            parser.values.output = open(value, "w")


if __name__ == '__main__':

    script_parser = OptionParser()

    script_parser.add_option("-e", "--env",
                             action="append",
                             dest="envlist",
                             metavar="PATHVAR",
                             help="add environment variable to be processed")
    script_parser.add_option("--shell", action="store", dest="shell", type="choice", metavar="SHELL",
                             choices=['csh', 'sh', 'bat'],
                             help="select the type of shell to use")

    script_parser.set_defaults(output=stdout)
    script_parser.add_option("-o", "--output", action="callback", metavar="FILE",
                             type="string", callback=_check_output_options_cb,
                             help="(internal) output the command to set up the environment ot the given file instead of stdout")
    script_parser.add_option("--mktemp", action="callback",
                             dest="mktemp",
                             callback=_check_output_options_cb,
                             help="(internal) send the output to a temporary file and print on stdout the file name (like mktemp)")

    options, args = script_parser.parse_args()

    if not options.shell and "SHELL" in environ:
        options.shell = environ["SHELL"]

    if options.envlist:
        for v in options.envlist:
            cleanVariable(v, options.shell, options.output)

    for a in args:
        print(stripPath(a))
