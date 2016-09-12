from invoke.collection import Collection
from invoke.tasks import task


@task
def clean(ctx):
    """Cleans temporary artifacts of project."""
    ctx.run('git clean -f -X -d -e \!*.egg-info -e \!.idea -e \!*.pyc')


@task
def develop(ctx):
    """Start development mode."""
    ctx.run('pip install -r requirements.txt')
    ctx.run("python setup.py develop")


@task
def undevelop(ctx):
    """Stop development mode."""
    ctx.run("python setup.py develop --uninstall")


@task
def package(ctx):
    """Packages module."""
    ctx.run("python setup.py bdist_wheel")


@task
def register(ctx):
    """Registers package to PyPI."""
    ctx.run('python setup.py register')


@task
def release(ctx):
    """Uploads packages to PyPI."""
    ctx.run('python setup.py bdist_wheel upload')


ns = Collection(clean, develop, undevelop, package, register, release)
