import setuptools
exec(open('_version.py').read())

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="processOrg",
    version=__version__,
    author="Stuart Ianna",
    author_email="stuian@protonmail.com",
    description="Python class helper for handling multiple external subprocesses.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stuianna/processOrg",
    classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
    ],
    py_modules=['processorg'],
    python_requires='>=3.6',
    )
