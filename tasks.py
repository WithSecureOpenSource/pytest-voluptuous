import re

from invoke.collection import Collection
from invoke.tasks import task


@task
def clean(ctx):
    """Cleans temporary artifacts of project."""
    ignores = re.match(r'^#\sno-clean:\s(.*)$', open('.gitignore').readline()).group(1).split(' ')
    ctx.run('git clean -f -X -d {}'.format(' '.join(['-e \!' + re.escape(ign) for ign in ignores])))


@task
def develop(ctx):
    """Start development mode."""
    ctx.run('pip install -e .')


@task
def undevelop(ctx):
    """Stop development mode."""
    ctx.run('python setup.py develop --uninstall')


@task
def analyze(ctx):
    """Run static analysis."""
    ctx.run('pylint pytest_voluptuous')


@task
def test(ctx):
    """Run unit tests."""
    ctx.run('pytest --cov pytest_voluptuous --cov-report term-missing')


@task
def package(ctx):
    """Packages module."""
    ctx.run('python setup.py bdist_wheel')


@task
def tox(ctx):
    """Run tox."""
    ctx.run('tox')


@task
def release(ctx, version):
    """Releases a new version of the library."""
    ctx.run('git tag -a {0} -m "Release {0}"'.format(version))
    ctx.run('git push')
    ctx.run('git push --tags')
    clean(ctx)
    package(ctx)
    upload(ctx)


@task
def upload(ctx):
    """Uploads packages to PyPI."""
    ctx.run('twine upload dist/pytest_voluptuous-*.whl')


ns = Collection(clean, develop, undevelop, analyze, test, tox, package, release, upload)
