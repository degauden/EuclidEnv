

import os
import sys


from Euclid.Path import multiPathGetFirst

try:
    import EnvConfig  # @UnresolvedImport @UnusedImport
except:
    if os.environ.get("CMAKE_PREFIX_PATH", None):
        env_conf_subdir = os.sep.join(["EnvConfig", "__init__.py"])
        env_conf_init = multiPathGetFirst(
            os.environ["CMAKE_PREFIX_PATH"], env_conf_subdir)
        if env_conf_init:
            env_conf = os.path.dirname(env_conf_init)
            env_py = os.path.dirname(env_conf)
            sys.path.insert(0, env_py)
            import EnvConfig  # @UnusedImport @UnresolvedImport @Reimport
        else:
            env_conf_subdir = os.sep.join(
                ["scripts", "EnvConfig", "__init__.py"])
            env_conf_init = multiPathGetFirst(
                os.environ["CMAKE_PREFIX_PATH"], env_conf_subdir)
            if env_conf_init:
                env_conf = os.path.dirname(env_conf_init)
                env_py = os.path.dirname(env_conf)
                sys.path.insert(0, env_py)
                import EnvConfig  # @UnresolvedImport @Reimport

    # use another fallback if CMAKE_PREFIX_PATH is not defined.

from Euclid.Run.Lookup import getEnvXmlPath, findProject
from Euclid.Run.Version import isValidVersion, expandVersionAlias

# auto_override_projects = [('Compat', 'latest')]
auto_override_projects = []


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
                raise OptionValueError(
                    "%s must be followed by the project name and optionally by the version" % opt_str)
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
                          metavar="PROJECT [VERSION]", type="string",
                          callback=runtime_project_option,
                          nargs=0,
                          help="Add a project to the runtime environment")

        def overriding_project_option(_option, opt_str, _value, parser):
            pv = extract_project_version(opt_str, parser.rargs)
            parser.values.overriding_projects.append(pv)

        parser.add_option("--overriding-project", action="callback",
                          metavar="PROJECT [VERSION]", type="string",
                          callback=overriding_project_option,
                          nargs=0,
                          help="Add a project to override packages")

        parser.add_option("--no-auto-override", action="store_false",
                          dest="auto_override",
                          help="Do not automatically prepend the projects %s" % auto_override_projects)

        # Note: the profile is not used in the script class, but in the wrapper
        # it is added to the parser to appear in the help and for checking
        parser.add_option("--profile", action="store_true",
                          help="Print some profile informations about the execution.")

        parser.set_defaults(use=[],
                            runtime_projects=[],
                            overriding_projects=[],
                            auto_override=True)

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
        # FIXME: when we drop Python 2.4, this should become 'from . import
        # path'
        from Euclid.Run import path
        # prepend dev dirs to the search path
        if self.opts.dev_dirs:
            path[:] = map(str, self.opts.dev_dirs) + path

        if self.opts.user_area and not self.opts.no_user_area:
            path.insert(0, self.opts.user_area)

        # prepare the list of projects to use
        projects = []
        if self.opts.auto_override:
            explicit = set([p[0] for p in self.opts.overriding_projects])
            projects.extend(
                [p for p in auto_override_projects if p[0] not in explicit])
        projects.extend(self.opts.overriding_projects)
        projects.append((self.project, self.version))
        projects.extend(self.opts.runtime_projects)

        # set the environment XML search path
        env_path = []
        for p, v in projects:
            v = expandVersionAlias(p, v)
            env_path.extend(
                getEnvXmlPath(p, v, self.opts.platform))
        # FIXME: EnvConfig has got problems with unicode in the search path
        # ensure that we do not have unicode strings
        env_path = map(str, env_path)
        EnvConfig.path.extend(env_path)

        # extend the prompt variable (bash, sh)
        if self.cmd and os.path.basename(self.cmd[0]) in ('bash', 'sh'):
            prompt = os.environ.get('PS1', r'\W \$ ')
            self.opts.actions.append(
                ('set', ('PS1', r'[{0} {1}] {2}'.format(self.project, self.version, prompt))))

        # instruct the script to load the projects environment XML
        for p, _ in projects:
            self.opts.actions.insert(0, ('loadXML', (p + 'Environment.xml',)))

        super(ERun, self)._makeEnv()

    def main(self):
        super(ERun, self).main()
