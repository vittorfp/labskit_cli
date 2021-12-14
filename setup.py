"""
Setup module for the labskit package.  
"""
from pathlib import Path
from setuptools import setup, find_packages

package_files = [
    str(Path('data') / 'gryphon_config.json'),
    str(Path('data') / 'lib_category_tree.json')
]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name='labskit',
    version='0.0.1',
    license='MIT',
    description='OW analytics toolkit cli',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['gryph', 'gryphon', 'gryphon_commands'],
    packages=find_packages(),
    install_requires=[requirements],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points='''
        [console_scripts]
        gryphon=gryphon:main
        gryph=gryph:cli
        griffin=gryphon:did_you_mean_gryphon
    ''',
    include_package_data=True,
    package_data={'gryphon_commands': package_files}
)
