from setuptools import setup, find_packages


setup(
    name='pytest-voluptuous',
    use_scm_version=True,
    description='Pytest plugin for asserting data against voluptuous schema.',
    long_description=open('README.rst').read(),
    license='MIT',
    author='Tuukka Mustonen',
    author_email='tuukka.mustonen@gmail.com',
    url='https://github.com/tuukkamustonen/pytest-voluptuous',
    packages=find_packages(),
    install_requires=open('requirements.txt').readlines(),
    classifiers=[
        'Intended Audience :: Developers',
        'Framework :: Pytest',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    entry_points={
        'pytest11': [
            'pytest_voluptuous = pytest_voluptuous.plugin',
        ],
    },
)
