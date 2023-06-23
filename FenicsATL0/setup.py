from setuptools import setup

setup(
    name='FenicsATL',
    version='1.0.2',
    packages=['FenicsATL'],
    install_requires=[
        'paramiko',
        'mysql-connector-python',
        'numpy',
        'pandas',
        'bokeh',
        'matplotlib'
    ],
    author='SI SAID Wassim',
    author_email='wassim.sisaid@gmail.com',
    description='FenicsATL data analysis library',
    url='https://github.com/your/repo',
    entry_points={
        'console_scripts': [
            'fenicsatl = FenicsATL:commands'
        ]
    }
)
