"""How to download and verify Python versions."""

import os
import tarfile
import urllib2
from contextlib import closing

def _tarname(version):
    if version < '1.6':
        return 'py{}.tgz'.format(version.replace('.', ''))
    elif version < '2':
        return 'Python-{}.tar.gz'.format(version)
    else:
        return 'Python-{}.tgz'.format(version)

def _tarpath(version):
    return os.path.join('Download', _tarname(version))

def _url(version):
    if version < '1.6':
        base = 'http://www.python.org/ftp/python/src/'
    elif version < '2':
        base = 'http://www.python.org/download/releases/{}/'.format(version)
    else:
        base = 'http://www.python.org/ftp/python/{}/'.format(version)
    return base + _tarname(version)

def force_download(version):
    if not os.path.exists('Download'):
        os.mkdir('Download')
    print(_url(version))
    with closing(urllib2.urlopen(_url(version))) as response:
        contents = response.read()
    with open(_tarpath(version), 'w') as destination:
        destination.write(contents)

def download(version):
    if os.path.exists(_tarpath(version)):
        if os.stat(_tarpath(version)).st_size:
            return
    print('Downloading Python {}'.format(version))
    force_download(version)

def _builddir(version):
    return os.path.join('Build', version)

def untar(version):
    if not os.path.exists('Build'):
        os.mkdir('Build')
    tar = tarfile.open(_tarpath(version))
    tar.extractall('Build')
