from setuptools import setup, find_packages

version = "0.1.1"

setup(
    name='warped',
    version=version,
    packages=find_packages(),
    url='https://git.k-fortytwo.de/christofsteel/warp',
    download_url = 'https://git.k-fortytwo.de/christofsteel/warped/archive/%s.tar.gz' % version,
    license='MIT',
    author='Christoph Stahl',
    author_email='christoph.stahl@uni-dortmund.de',
    description='A webbased wrapper for the argument parser in Python',
    entry_points={
        'console_scripts': [
            "warped = warped.hook:main"
        ]
    },
    include_package_data = True,
    zip_safe=False,
    install_requires = ['Flask']
)
