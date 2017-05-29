from setuptools import setup, find_packages

setup(
    name='warped',
    version='0.1.0',
    packages=find_packages(),
    url='https://git.k-fortytwo.de/christofsteel/warp',
    download_url = 'https://git.k-fortytwo.de/christofsteel/warped/archive/0.1.0.tar.gz',
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
