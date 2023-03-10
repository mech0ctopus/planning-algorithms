from setuptools import setup, find_packages

setup(
    name="planning",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
    extras_require={
        "dev": ["pytest", "pytest-cov"]
    },
    author="Craig Miller",
    author_email="craigdanielmiller@gmail.com",
    description="Experimental implementations of Planning Algorithms by Steven LaValle.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mech0ctopus/planning-algorithms",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
