
import os
import logging

# FIXME: when we drop Python 2.4, this should become 'from . import path'
from Euclid.Run import path, Error

log = logging.getLogger(__name__)

class NotFoundError(Error):
    '''
    Generic error for configuration elements that are not found.
    '''

class MissingManifestError(NotFoundError):
    '''
    The manifest.xml for a project was not found.
    '''

class MissingProjectError(NotFoundError):
    '''
    The manifest.xml for a project was not found.
    '''
    def __init__(self, *args):
        super(MissingProjectError, self).__init__(*args)
        self.name, self.version, self.platform, self.path = args
    def __str__(self):
        return 'cannot find project {0} {1} for {2} in {3}'.format(*self.args)

def findProject(name, version, platform):
    '''
    Find a Gaudi-based project in the directories specified in the 'path'
    variable.

    @param name: name of the project (case sensitive for local projects)
    @param version: version of the project
    @param platform: binary platform id

    @return path to the project binary directory
    '''
    log.debug('findProject(%r, %r, %r)', name, version, platform)
    # standard project suffixes
    suffixes = [os.path.join(name, version),
                '{0}_{1}'.format(name, version),
                os.path.join(name.upper(), '{0}_{1}'.format(name.upper(), version))]
    # special case: with the default 'latest' version we allow the plain name
    if version == 'latest':
        suffixes.insert(0, name)

    bindir = os.path.join('InstallArea', platform)
    for d in [os.path.join(b, s, bindir)
              for b in path
              for s in suffixes]:
        log.debug('check %s', d)
        if os.path.exists(d):
            log.debug('OK')
            return d
    else:
        raise MissingProjectError(name, version, platform, path)

def parseManifest(manifest):
    '''
    Extract the list of required projects from a manifest.xml
    file.

    @param manifest: path to the manifest file
    @return: tuple with ([projects...],) as (name, version) pairs
    '''
    from xml.dom.minidom import parse
    m = parse(manifest)
    def _iter(parent, child):
        '''
        Iterate over the tags in <parent><child/><child/></parent>.
        '''
        for pl in m.getElementsByTagName(parent):
            for c in pl.getElementsByTagName(child):
                yield c
    # extract the list of used (project, version) from the manifest
    used_projects = [(p.attributes['name'].value, p.attributes['version'].value)
                     for p in _iter('used_projects', 'project')]
    return (used_projects,)

def getEnvXmlPath(project, version, platform):
    '''
    Return the list of directories to be added to the Env XML search path for
    a given project.
    '''
    pdir = findProject(project, version, platform)
    search_path = [pdir]
    # manifests to parse
    manifests = [os.path.join(pdir, 'manifest.xml')]
    while manifests:
        manifest = manifests.pop(0)
        if not os.path.exists(manifest):
            raise MissingManifestError(manifest)
        projects,_ = parseManifest(manifest)
        # add the project directories ...
        pdirs = [findProject(p, v, platform) for p, v in projects]
        search_path.extend(pdirs)
        # ... and their manifests to the list of manifests to parse
        manifests.extend([os.path.join(pdir, 'manifest.xml') for pdir in pdirs])
    def _unique(iterable):
        returned = set()
        for i in iterable:
            if i not in returned:
                returned.add(i)
                yield i
    return list(_unique(search_path))

