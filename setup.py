import setuptools

setuptools.setup(
    name="clevermaps-python-sdk",
    version="0.0.1",
    author="Karel Psota",
    author_email="karel.psota@clevermaps.io",
    description="Python SDK client for the CleverMaps API",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests>=2.30.0',
        'pydantic>=2.0.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
