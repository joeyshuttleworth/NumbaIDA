from os import path

from skbuild import setup

this_directory = path.abspath(path.dirname(__file__))

long_description = "NumbaIDA is a Python package allowing you to quickly solve DAE problems in"\
    + "Numba JIT compiled functions using the LLNL SUNDIALS IDA solver."

setup(
    name="numbaida",
    packages=['numbaida'],
    version='0.0.1',
    license='MIT',
    author='Joseph Shuttleworth',
    author_email='joseph.shuttleworth@nottingham.ac.uk',
    description='Python wrapper of IDA (solving DAEs)' +
    ' which can be used with Numba.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>3.6',
    make_args=['-DSKBUILD=ON'],
    install_requires=['numpy', 'numba', 'scikit-build'],
    extras_require={
        'test': [
            'pytest-cov>=2.10',     # For coverage checking
            'pytest>=4.6',          # For unit tests
            'flake8>=3',            # For code style checking
            'matplotlib',
            'isort',
            'mock>=3.0.5',         # For mocking command line args etc.
            'codecov>=2.1.3',
            'matplotlib>=3.5.1',
        ]}
)
