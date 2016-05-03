from setuptools import setup

setup(
    name="community-detection-with-weighted-nodes",
    version="0.1",
    author="Michael Ionkin",
    author_email="msionkin@gmail.com",
    description="Louvain algorithm for community detection in the graph with "
                "nodes that have its own weights",
    license="BSD",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 1 - Beta",
    ],

    packages=['louvain', 'graphIO', 'data'],
    install_requires=[
        "networkx", "matplotlib"
    ],
)