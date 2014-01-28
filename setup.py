import io
import sys
from os.path import dirname, join
from setuptools import setup, find_packages, Extension
from pip.req import parse_requirements


def get_requirements(filename):
    return [str(r.req) for r in
            parse_requirements(join(dirname(__file__), filename))]


install_requirements = get_requirements("requirements.txt")
test_requirements= get_requirements("test-requirements.txt")


setup(
    name='lucky',
    version='0.1',
    description='An lean api for connecting to Leankit.',
    author_email='kevin@bigkevmcd.com',
    author='Kevin McDermott',
    classifiers=[],
    include_package_data=True,
    license='MIT',
    packages=['lucky'],
    install_requires=install_requirements,
    tests_require=test_requirements,
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'lucky = lucky.scripts:main'
        ]
    }
)
