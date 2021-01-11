import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LargestValues-AZHAR-BASIT", # Replace with your own username
    version="0.0.1",
    author="Azhar Basit",
    author_email="azhar.basit@gmail.com",
    description="TRI-AD Coding Challenge",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/azh4r/triad-challenge",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)