
import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='LordXen',
    version='0.0.0.1',
    url='https://github.com/LordBex/LordXen',
    license='',
    author='lordbex',
    author_email='lordibex@protonmail.com',
    description='Python XenForo Api lib',
    long_description=read('README.rst'),
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Environment :: Web Environment', 'Intended Audience :: Developers',
        'Operating System :: OS Independent', 'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ])