import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="MHPKMS",                     # This is the name of the package
    version="1.0.0.2",                        # The initial release version
    author="MHP",                     # Full name of the author
    author_email='py.hacker.hieu@gmail.com',
    keywords=['MHP', "KMS", 'trial', 'python', 'python3'],
    url='https://github.com/MHP0920/MHPKMS',
    license="CC BY-ND 4.0",
    description="Send trial products take easy.",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Free To Use But Restricted",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    install_requires=['requests'],                     # Install other dependencies if any

)