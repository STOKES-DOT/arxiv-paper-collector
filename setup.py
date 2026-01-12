"""
ArXiv Paper Collector - Setup Script
Install with: pip install -e .
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

setup(
    name='arxiv-paper-collector',
    version='1.0.0',
    author='Jiaoyuan',
    author_email='your-email@example.com',
    description='Automated arXiv paper collection and PDF report generation',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/YOUR_USERNAME/arxiv-paper-collector',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.8',
    install_requires=[
        'arxiv>=1.4.0',
        'PyYAML>=6.0',
        'Jinja2>=3.1.0',
        'python-dateutil>=2.8.0',
        'colorlog>=6.7.0',
        'schedule>=1.2.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'arxiv-collector=main:main',
        ],
    },
    include_package_data=True,
    package_data={
        'arxiv_paper_collector': ['templates/*.tex', 'config.yaml'],
    },
    zip_safe=False,
    keywords='arxiv papers academic research automation latex pdf machine-learning',
)
