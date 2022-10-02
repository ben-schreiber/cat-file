import versioneer
from setuptools import find_packages
from setuptools import setup


setup(
    name="cat-file",
    url="https://github.com/schreiberben/cat-file.git",
    description="A CLI tool to visualize data files",
    author="Ben Schreiber",
    install_requires=["pandas", "tabulate", "pyarrow", "xlrd", "openpyxl"],
    entry_points={"console_scripts": ["cat-file = cat_file.main:main"]},
    packages=find_packages(),
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    python_requires=">=3.8.0",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
