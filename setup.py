from setuptools import setup, find_packages

setup(
    name="pygame-template",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pygame>=2.6.1",
    ],
    python_requires=">=3.13",
    author="Ray Thurman",
    author_email="raymondthurman5@gmail.com",
    description="A production-ready PyGame template",
    keywords="pygame, template, game",
    url="https://github.com/raythurman2386/pygame-template",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Games/Entertainment",
    ],
)
