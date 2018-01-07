import re

from invoke.collection import Collection
from invoke.tasks import task


@task
def clean(ctx):
    """Cleans temporary artifacts of project."""
    ignores = re.match('#\sno-clean:\s(.*)', open('.gitignore').readline()).group(1).split(' ')
    ctx.run('git clean -f -X -d {}'.format(' '.join(['-e \!' + re.escape(ign) for ign in ignores])))


@task
def develop(ctx):
    """Start development mode."""
    ctx.run("pip install -e .")


@task
def undevelop(ctx):
    """Stop development mode."""
    ctx.run("python setup.py develop --uninstall")


@task
def test(ctx):
    """Run unit tests."""
    ctx.run("pytest")


@task
def package(ctx):
    """Packages module."""
    ctx.run("python setup.py bdist_wheel")


@task
def release(ctx, version):
    """Releases a new version of the library."""
    ctx.run('git tag -a {}'.format(version))
    clean(ctx)
    upload(ctx)
    ctx.run('git push')
    ctx.run('git push --tags')


@task
def register(ctx):
    """Registers package to PyPI."""
    ctx.run('python setup.py register')


@task
def upload(ctx):
    """Uploads packages to PyPI."""
    ctx.run('python setup.py bdist_wheel upload')


ns = Collection(clean, develop, undevelop, test, package, release, register, upload)
