import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name="admin_pretty_gfk",
    version="0.0.1",
    author="Andrii Tierzov",
    author_email="avtierzov@gmail.com",
    description="Custom Django admin mixin and widgets for handling generic foreign keys (GFKs) more intuitively.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DeDuHaNcHiK/admin-pretty-gfk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],

    packages=setuptools.find_packages(exclude=['tests*']),
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=[
        "Django>=4.2.18"
    ]
)
