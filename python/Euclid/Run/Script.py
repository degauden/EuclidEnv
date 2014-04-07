###############################################################################
# (c) Copyright 2013 CERN                                                     #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
__author__ = 'Marco Clemencic <marco.clemencic@cern.ch>'

import os
import re
import logging

import EnvConfig

from Euclid.Run.Lookup import getEnvXmlPath, findProject
from Euclid.Run.Version import isValidVersion, expandVersionAlias

auto_override_projects = [('Compat', 'latest')]


def projectExtraPath(projroot):
    '''
    Return any extra search path required by the project at 'projroot'.
    '''
    extra_path = []
    # drop the 'InstallArea' part of the path
    while 'InstallArea' in projroot:
        projroot = os.path.dirname(projroot)

    def extractList(filename, varname):
        if os.path.exists(filename):
            data = {}
            exec open(filename).read() in data #IGNORE:W0122
            # Get the list and convert it to strings
            return filter(str, data.get(varname, []))
        else:
            return []

    # check for a requested nightly slot
    nightly = os.path.join(projroot, 'nightly.cmake')
    if os.path.exists(nightly):
        exp = re.compile('^\s*set\s*\(\s*nightly_(slot|day)\s+(\S*)\s*\)', re.I)
        vals = dict([l.groups() for l in filter(None, map(exp.match, open(nightly)))])
        try:
            slot = vals['slot']
            day = vals['day']
            nd = os.path.join(os.environ.get('LHCBNIGHTLY', ''), slot, day)
            extra_path.append(nd)
            from Euclid.Run.Options import getNightlyExtraPath
            extra_path.extend(getNightlyExtraPath(nd, slot, day))
        except KeyError:
            logging.warning('invalid content of %s: ignored', nightly)

    # check for the Python digested search path
    spFile = os.path.join(projroot, 'searchPath.py')
    extra_path.extend(extractList(spFile, 'path'))

    return extra_path

class ERun(EnvConfig.Script):
    __usage__ = "Usage: %prog [OPTION]... [NAME=VALUE]... PROJECT VERSION [COMMAND [ARG]...]"

    def _prepare_parser(self):
        from Euclid.Run.Options import addSearchPath, addPlatform
        from optparse import OptionValueError

        super(ERun, self)._prepare_parser()
        parser = self.parser

        addPlatform(parser)
        addSearchPath(parser)

        def extract_project_version(opt_str, rargs):
            if not rargs:
                raise OptionValueError("%s must be followed by the project name and optionally by the version" % opt_str)
            p_name = rargs.pop(0)
            if rargs and isValidVersion(p_name, rargs[0]):
                v = rargs.pop(0)
            else:
                v = 'latest'
            return p_name, v

        def runtime_project_option(_option, opt_str, _value, parser):
            pv = extract_project_version(opt_str, parser.rargs)
            parser.values.runtime_projects.append(pv)

        parser.add_option("--runtime-project", action="callback",
                          metavar = "PROJECT [VERSION]", type="string",
                          callback=runtime_project_option,
                          nargs = 0,
                          help="Add a project to the runtime environment")

        def overriding_project_option(_option, opt_str, _value, parser):
            pv = extract_project_version(opt_str, parser.rargs)
            parser.values.overriding_projects.append(pv)

        parser.add_option("--overriding-project", action="callback",
                          metavar = "PROJECT [VERSION]", type="string",
                          callback=overriding_project_option,
                          nargs = 0,
                          help="Add a project to override packages")

        parser.add_option("--no-auto-override", action="store_false",
                          dest = "auto_override",
                          help = "Do not automatically prepend the projects %s" % auto_override_projects)

        parser.add_option("--use-grid", action="store_true",
                          help = "Enable auto selection of LHCbGrid project")

        # Note: the profile is not used in the script class, but in the wrapper
        #       it is added to the parser to appear in the help and for checking
        parser.add_option("--profile", action="store_true",
                          help="Print some profile informations about the execution.")

        parser.set_defaults(use = [],
                            runtime_projects = [],
                            overriding_projects = [],
                            auto_override = True,
                            use_grid = False)

    def _parse_args(self, args=None):
        super(ERun, self)._parse_args(args)
        if len(self.cmd) < 1:
            self.parser.error("missing project name")
        self.project = self.cmd.pop(0)
        if self.cmd and isValidVersion(self.project, self.cmd[0]):
            self.version = self.cmd.pop(0)
        else:
            self.version = 'latest'

    def _makeEnv(self):
        # FIXME: when we drop Python 2.4, this should become 'from . import path'
        from Euclid.Run import path
        # prepend dev dirs to the search path
        if self.opts.dev_dirs:
            path[:] = map(str, self.opts.dev_dirs) + path

        if self.opts.user_area and not self.opts.no_user_area:
            path.insert(0, self.opts.user_area)

        # prepare the list of projects to use
        projects = []
        if self.opts.use_grid:
            self.opts.overriding_projects.extend(('LHCbGrid', 'latest'))
        if self.opts.auto_override:
            explicit = set([p[0] for p in self.opts.overriding_projects])
            projects.extend([p for p in auto_override_projects if p[0] not in explicit])
        projects.extend(self.opts.overriding_projects)
        projects.append((self.project, self.version))
        projects.extend(self.opts.runtime_projects)

        # Check if the main project needs a special search path
        self.log.debug('check if we need extra search path')
        extra_path = projectExtraPath(findProject(self.project, self.version, self.opts.platform))
        if extra_path:
            self.log.debug('the project requires an extra search path')
            # we add the extra search path between the command line entries and the default
            idx = len(self.opts.dev_dirs)
            if self.opts.user_area:
                idx += 1
                path[:] = path[:idx] + extra_path + path[idx:]
            self.log.debug('final search path: %r', path)

        # set the environment XML search path
        env_path = []
        for p, v in projects:
            v = expandVersionAlias(p, v)
            env_path.extend(getEnvXmlPath(p, v, self.opts.platform))
        # FIXME: EnvConfig has got problems with unicode in the search path
        env_path = map(str, env_path) # ensure that we do not have unicode strings
        EnvConfig.path.extend(env_path)

        # extend the prompt variable (bash, sh)
        if self.cmd and os.path.basename(self.cmd[0]) in ('bash', 'sh'):
            prompt = os.environ.get('PS1', r'\W \$ ')
            self.opts.actions.append(('set', ('PS1', r'[{0} {1}] {2}'.format(self.project, self.version, prompt))))


        # instruct the script to load the projects environment XML
        for p, _ in projects:
            self.opts.actions.insert(0, ('loadXML', (p + 'Environment.xml',)))

        super(ERun, self)._makeEnv()


    def main(self):
        super(ERun, self).main()
