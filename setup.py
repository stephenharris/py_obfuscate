from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='py_obfuscate',
    version='0.1.4',
    description='A module for obfuscating a mysqldump file',
    long_description=long_description,
    long_description_content_type='text/markdown', 
    url='https://github.com/stephenharris/py_obfuscate',
    author='Stephen Harris',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='obfuscate mysqldump mysql',
    packages=find_packages(),
    install_requires=['faker'],
    extras_require={},
    package_data={},
    entry_points={},
)