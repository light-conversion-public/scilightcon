# -*- coding: utf-8 -*-
'''
Created on Wed Feb  5 16:19:16 2020

@author: butkus
'''
import setuptools
import codecs
import os.path

with open('README.md', 'r') as fh:
    long_description = fh.read()
    
with open('requirements.txt', 'r') as fr:
    install_requires = [line.strip() for line in fr.readlines()]


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

setuptools.setup(
    name='scilightcon', # Replace with your own username
    version=get_version("scilightcon/__init__.py"),
    author='Vytautas Butkus',
    author_email='vytautas.butkus@lightcon.com',
    description='A lightcon scipack',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires = install_requires,
    packages=['scilightcon'],
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 1 - Planning',
    ],
    project_urls = {
            'Examples': 'https://bitbucket.org/harpiasoftware/light-conversion-apis/src/master/examples/'},
    python_requires='>=3.7',
)

