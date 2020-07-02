from setuptools import setup

setup(
    name='torchmoji',
    version='1.0',
    packages=['torchmoji'],
    description='torchMoji',
    include_package_data=True,
    install_requires=[
        'emoji~=0.4.5',
        'numpy~=1.14.6',
        'scipy~=1.1.0',
        'scikit-learn~=0.19.2',
        'text-unidecode~=1.0',
    ],
)
