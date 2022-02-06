from os import path

from skbuild import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="NumbaIDA",
    packages=['NumbaIDA'],
    version='0.0.1',
    license='MIT',
    install_requires=['numpy','numba', 'scikit-build'],
    author='Joseph Shuttleworth',
    author_email='joseph.shuttleworth@nottingham.ac.uk',
    description='Python wrapper of IDA (solving DAEs)' +
    ' which can be used with Numba.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>3.6',
    cmake_args=['-DSKBUILD=ON']
    )
