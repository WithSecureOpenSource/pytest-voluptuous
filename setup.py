from setuptools import setup, find_packages


setup(
    name='pytest-voluptuous',
    use_scm_version=True,
    description='Pytest plugin for asserting data against voluptuous schema.',
    long_description=open('README.rst').read() + '\n' + open('CHANGELOG.rst').read(),
    license='ASL 2.0',
    author='F-Secure Corporation',
    author_email='opensource@f-secure.com',
    url='https://github.com/f-secure/pytest-voluptuous',
    packages=find_packages(),
    install_requires=open('requirements.txt').readlines(),
    classifiers=[
        'Intended Audience :: Developers',
        'Framework :: Pytest',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'pytest11': [
            'pytest_voluptuous = pytest_voluptuous.plugin',
        ],
    },
)
