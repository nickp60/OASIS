from setuptools import setup, find_packages
# from distutils.core import setup
setup(
    name="OASIS",
    author="David Robinson",
    author_email="dgrtwo@princeton.edu",
    description="Optimized Annotation System for Insertion Sequences",
    version="1.0",
    packages=find_packages(),
    package_data={"OASIS": ["data/*"]},
    entry_points={
        'console_scripts': [
            'OASIS=OASIS.OASIS_main:main',
        ],
    },
)
