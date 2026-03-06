from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="flashcardio",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Generate double-sided printable flashcard PDFs from CSV or ODS files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/Flashcardio",
    py_modules=["flashcardio"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Education",
        "Topic :: Printing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "flashcardio=flashcardio:main",
        ],
    },
    keywords="flashcards pdf education study printing csv ods",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/Flashcardio/issues",
        "Source": "https://github.com/yourusername/Flashcardio",
    },
)
