from setuptools import find_packages, setup

setup(
    name='BuildForSDG_API',
    version='1.0.0',
    packages=find_packages(),
    zip_safe=False,
    include_package_date=True,
    install_requires=['Flask', 'flask_restplus', 'python-simplexml']
)
