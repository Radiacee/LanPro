from setuptools import setup, find_packages

setup(
    name='LanPro',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A fun programming language with unique syntax and features.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/LanPro',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        # Add your project dependencies here
    ],
)