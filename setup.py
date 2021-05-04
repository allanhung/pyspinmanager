try:
    import setuptools
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION='0.1.0'

setup(
    name='pyspinmanager',
    packages=setuptools.find_packages(),
    package_data={'pyspinmanager': ['spin_templates/*.j2']},
    install_requires=['docopt', 'jinja2', 'jq', 'tqdm', 'pyyaml', 'numpy'],
    version=VERSION,
    description='maintain spinnaker application and pipeline',
    author='Allan',
    author_email='hung.allan@gmail.com',
    url='https://github.com/hungallan/pyspinmanager',
    download_url='https://github.com/hungallan/pyspinmanager/tarball/' + VERSION,
    keywords=['utility', 'miscellaneous', 'library'],
    classifiers=[],
    entry_points={                                                                                                                                                                                                                                                             
        'console_scripts': [                                                                                                                                                                                                                                                   
            'pyspinmanager = pyspinmanager.pyspinmanager:main',                                                                                                                                                                                                                          
        ]
    }
)
