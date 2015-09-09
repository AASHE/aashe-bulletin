from contextlib import contextmanager as _contextmanager
import time
import os

from fabric.api import cd, env, local, prefix, put, run, sudo
from fabric.contrib.files import exists
from fabric.colors import red, green
from fabric.context_managers import shell_env


env.current_symlink_name = 'current'
env.previous_symlink_name = 'previous'
env.virtualenv_name = 'env'
env.remote_vars = {}


@_contextmanager
def virtualenv():
    '''
    Custom fabric contextmanager that lets you run fabric
    commands (via sudo(), run(), etc.) with a virtualenv
    activated. Uses the `activate` fabric env attribute
    as the virtualenv activation command.

    Usage:
        with(virtualenv()):
            run("python manage.py syncdb")
    '''
    with cd(env.remote_path):
        with shell_env(**env.remote_vars):
            with prefix(env.activate):
                yield


def common_env():
    '''
    Set env attributes common to development, test,
    and production environments.
    '''
    env.user = 'releaser'
    env.remote_path = '/var/www/bulletin'
    env.django_settings = 'aashe_bulletin.settings'
    env.activate = 'source %s/%s/bin/activate' % (env.remote_path,
                                                  env.virtualenv_name)
    env.requirements_txts = ['requirements.txt']
    env.uwsgi_service_name = 'bulletin'
    env.remote_vars = {
        'BULLETIN_DATABASE_URL': os.environ.get('BULLETIN_DATABASE_URL',
                                                '')
    }
    env.branch = 'master'


def development():
    common_env()
    env.hosts = ['bulletin-dev.aashe.org']
    # env.branch = 'advanced-search'


def test():
    common_env()
    env.hosts = ['beta.aashe.org']


def production():
    common_env()
    env.hosts = ['bulletin.aashe.org']


def deploy():
    '''
    Generic deploy function to deploy a release to the configured
    server. Servers are configured via other functions (like dev).

    For example, to deploy to the dev server, use the fabric command:

    $ fab dev deploy
    '''
    export()
    # manage('syncdb')
    # manage('migrate')
    requirements()
    if not validate():
        print(red(
            "[ ERROR: Deployment failed to pass validate() "
            "on remote. Exiting. ]"))
    else:
        print(green(
            "[ PASS: Deployment passed validate() on remote. "
            "Continuing... ]"))
    config()
    restart()


def export():
    '''
    Create an archive from the current Git master branch and upload it.
    '''
    release = time.strftime('%Y%m%d%H%M%S')

    export_path = release

    tarfile = '%s.tar.gz' % release
    local('git archive --format=tar {branch} | gzip > {tarfile}'.format(
        branch=env.branch, tarfile=tarfile))

    put(tarfile, env.remote_path)
    local("rm %s" % tarfile)

    with cd(env.remote_path):
        # extract tarfile to export path
        run('mkdir %s' % export_path)
        run('tar xvzf {tarfile} --directory {export_path}'.format(
            tarfile=tarfile, export_path=export_path))
        run('rm -rf %s' % tarfile)

    env.release_path = '%s/%s' % (env.remote_path, export_path)


def requirements():
    '''
    Refresh or create the remote virtualenv site-packages using
    the project's requirements.txt files.
    '''
    with virtualenv():
        print("Updating virtualenv via requirements...")
        if not hasattr(env, 'release_path'):
            env.release_path = '%s/current' % env.remote_path
        for requirements_txt in env.requirements_txts:
            run('pip install -r %s/%s' % (env.release_path,
                                          requirements_txt))


def validate():
    '''
    Validate the installation.
    '''
    with virtualenv():
        with cd(env.release_path):
            result = run('python manage.py validate --settings=%s' %
                         env.django_settings)
            print 'validate() result was %s' % result
    return result.succeeded


def update_symlinks():
    with cd(env.remote_path):
        if exists('%s' % env.previous_symlink_name):
            previous_path = run('readlink %s' % env.previous_symlink_name)
            run('rm %s' % env.previous_symlink_name)
            run('rm -rf %s' % previous_path)
        if exists('%s' % env.current_symlink_name):
            # get the real directory pointed to by current
            current_path = run('readlink %s' % env.current_symlink_name)
            # make current the new previous
            run('ln -s %s %s' % (current_path, env.previous_symlink_name))
            run('rm %s' % env.current_symlink_name)
        # update "current" symbolic link to new code path
        run('ln -s %s %s' % (env.release_path, env.current_symlink_name))


def config(collectstatic=True):
    '''
    Configure the exported and uploaded code archive.
    '''
    update_symlinks()
    if collectstatic:
        with virtualenv():
            with cd(env.release_path):
                run('python manage.py collectstatic --settings=%s --noinput' %
                    env.django_settings)


def restart():
    '''
    Reboot uwsgi server.
    '''
    sudo("/sbin/status {service} | grep 'start/running' "
         "&& /sbin/stop {service}".format(service=env.uwsgi_service_name))
    sudo("/sbin/start %s" % env.uwsgi_service_name)


def manage(args):
    '''
    Run "manage.py {args}".
    '''
    with virtualenv():
        with cd("%s/current" % env.remote_path):
            run('python manage.py ' + args +
                ' --noinput --settings=' + env.django_settings)
