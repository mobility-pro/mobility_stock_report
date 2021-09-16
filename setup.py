from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in mobility/__init__.py
from mobility import __version__ as version

setup(
	name="mobility",
	version=version,
	description="Custom App for Mobilty",
	author="Frappe",
	author_email="developers@frappe.io",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
