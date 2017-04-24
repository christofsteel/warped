from setuptools import setup, find_packages

setup(
    name='warp',
    version='0.0.1',
    packages=['warp'],
    url='https://git.k-fortytwo.de/christofsteel/warp',
    license='MIT',
    author='Christoph Stahl',
    author_email='christoph.stahl@uni-dortmund.de',
    description='A webbased wrapper for the argument parser in Python',
    entry_points={
        'console_scripts': [
            "warp = warp.hook:main"
        ]
    },
    include_package_data = True,
    install_requires = ['Flask']
)
