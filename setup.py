from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in test_zeinab/__init__.py
from test_zeinab import __version__ as version

setup(
	name="test_zeinab",
	version=version,
	description="Calculate Average Power Consumption",
	author="Zeinab Mohammed",
	author_email="devzeinab@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
