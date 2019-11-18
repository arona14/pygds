import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pygds-sessionless',
    version='0.0.18',
    description="A python package to make it easy interacting with gds."
                "In this version the system won't hold any session",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/cosmopolitan-travel-serivce/pygds',
    license='MIT',
    author='Cosmo Tech Service',
    author_email='mbaye@ctsfares.com',
    packages=setuptools.find_packages(),
    install_requires=[
        'pandas',
        'jxmlease',
        'xmltodict',
        'lxml',
        'requests',
        'deprecation'
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
