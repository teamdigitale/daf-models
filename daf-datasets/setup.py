from setuptools import setup, find_packages

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='daf-datasets',
    version='0.0.1',
    description='Official Datasets from the DAF Team',
    author='Daf Team',
    author_email='fabiofumarola@gmail.com',
    url='https://github.com/teamdigitale/daf-datasets',
    install_requires=[
        'numpy',
        'nltk',
        'request'
    ],
    classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
    packages=find_packages()
)
