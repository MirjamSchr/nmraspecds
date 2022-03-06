import os
import setuptools


def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        content = file.read()
    return content


setuptools.setup(
    name='nmraspecds',
    version=read('VERSION').strip(),
    description='ASpecD derived Package for recipe driven data analysis of NMR spectra',
    long_description=read('README.rst'),
    long_description_content_type="text/x-rst",
    author='Mirjam Schröder',
    author_email='mirjam.schroeder@catalysis.de',
    url='https://www.nmraspecds.de',
    project_urls={
        "Documentation": 'https://docs.nmraspecds.de',
        "Source": 'https://github.com/majrim-spc/nmraspecds',
    },
    packages=setuptools.find_packages(exclude=('tests', 'docs')),
    license='BSD',
    keywords=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Development Status :: 4 - Beta",
    ],
    install_requires=[
    ],
    extras_require={
        'dev': ['prospector'],
        'docs': ['sphinx', 'sphinx-rtd-theme', 'sphinx_multiversion'],
    },
    python_requires='>=3.7',
)
