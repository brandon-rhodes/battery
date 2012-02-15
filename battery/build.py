"""How to download and verify Python versions."""

import os
import subprocess
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
    return os.path.join('Build', 'Python-' + version)

def untar(version):
    if not os.path.exists('Build'):
        os.mkdir('Build')
    builddir = _builddir(version)
    if not os.path.exists(builddir):
        tar = tarfile.open(_tarpath(version))
        tar.extractall('Build')

def cmmi(version):
    builddir = _builddir(version)
    # patch
    with open(os.path.join(builddir, 'Objects', 'fileobject.c'), 'r+') as f:
        s = f.read()
        if '_getline' not in s:
            s = s.replace('getline', '_getline')
            f.seek(0)
            f.write(s)
    if version.startswith('2.0'):
        with open(os.path.join(builddir, 'Modules', 'readline.c'), 'r+') as f:
            s = f.read()
            if 'rl_read_init_file(const char *)' not in s:
                s = s.replace('rl_read_init_file(char *)',
                              'rl_read_init_file(const char *)')
                s = s.replace('rl_insert_text(char *)',
                              'rl_insert_text(const char *)')
                f.seek(0)
                f.truncate()
                f.write(s)
    if '2.1' <= version < '2.4':
        with open(os.path.join(builddir, 'Modules', 'readline.c'), 'r+') as f:
            s = f.read()
            if '\nstatic int history_length' in s:
                s = s.replace('\nstatic int history_length',
                              '\n/*static int history_length')
                f.seek(0)
                f.truncate()
                f.write(s)
    # go
    if not os.path.exists('usr'):
        os.mkdir('usr')
    args = ['/bin/bash', 'configure',
            '--prefix=' + os.path.join(os.getcwd(), 'usr'),
            '--with-threads']
    if version.startswith('2.3'):
        args.append('BASECFLAGS=-U_FORTIFY_SOURCE')
    if version >= '2.3':
        args.append('--enable-shared')

    config_out = os.path.join(builddir, 'config.out')
    with open(config_out, 'w') as f:
        subprocess.check_call(args, stdout=f, stderr=subprocess.STDOUT,
                              cwd=builddir)

    if version < '2.1':
        with open(os.path.join(builddir, 'Modules', 'Setup.in'), 'r+') as f:
            s = f.read()
            for module in ('*shared*', 'readline', '_locale', 'crypt',
                           'syslog', 'zlib'):
                s = s.replace('\n#' + module, '\n' + module)  # uncomment line
            f.seek(0)
            f.write(s)

    # On Ubuntu Natty and later, libraries live under directories with
    # names like "/usr/lib/i386-linux-gnu".

    if version >= '2.5' and os.path.exists('/usr/bin/dpkg-architecture'):
        arch = subprocess.check_output([
                'dpkg-architecture', '-qDEB_BUILD_MULTIARCH']).strip()
        if os.path.isdir('/usr/lib/' + arch):
            with open(os.path.join(builddir, 'setup.py'), 'r+') as f:
                s = f.read()
                s = s.replace('lib64', 'lib/' + arch)
                f.seek(0)
                f.write(s)

    env = dict(os.environ)
    env['LD_LIBRARY_PATH'] = os.path.join(os.getcwd(), 'usr', 'lib')

    subprocess.check_call(['make'], cwd=builddir, env=env)
    subprocess.check_call(['make', 'install'], cwd=builddir, env=env)

    mainpython = os.path.join('usr', 'bin', 'python')
    if os.path.exists(mainpython):
        os.unlink(mainpython)
