from setuptools import setup

setup(
    name='nonediag',
    version=open("VERSION").read(),
    description='NoneBot2 error diagnosing tool.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='HivertMoZara',
    author_email='worldmozara@gmail.com',
    url='https://github.com/NCBM/nonediag',
    python_requires=">=3.7",
    packages=["nonediag"],
    install_requires=open('requirements.txt').read().splitlines(),
    entry_points={
        'console_scripts': [
            'nonediag = nonediag.__main__:_entry'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    license='MIT',
)
