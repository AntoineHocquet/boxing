# Packaging and entry point setup
from setuptools import setup, find_packages

setup(
    name='boxing',
    version='0.1.0',
    author='Antoine Hocquet',
    author_email='antoine.hocquet86@gmail.com',
    description='Adversarial training framework with neural networks fighting in a 2D box',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AntoineHocquet/boxing',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'numpy',
        'matplotlib',
        'pillow',
        'torch>=2.0',
    ],
    entry_points={
        'console_scripts': [
            'boxing=boxing.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.8',
)
