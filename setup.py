from setuptools import find_namespace_packages, setup

setup(
    name="shamzam",
    version="0.1",
    packages=find_namespace_packages(include=['services.*']),    
    package_dir={
        'services.catalogue': 'services/catalogue',
        'services.recognition': 'services/recognition'
    },
    install_requires=[
        'Flask>=2.0.3',
        'requests>=2.26.0',
        'SQLAlchemy>=1.4.27'
    ]
)
