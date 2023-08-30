from setuptools import find_packages, setup

setup(
    name="xjst",
    version="0.1.3",
    packages=find_packages(include=["xjst", "xjst.*"]),
    description="XML & JSON serialization tools at BSUIR 2023 spring semester.""",
    author="Me",
    license="MIT",
    entry_points={
        'console_scripts': ['xjst=xjst.lib:main']
    }
)
