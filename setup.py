from setuptools import setup

setup(
    name='gnomopo',
    version="0.1.1",
    author='Mario Balibrera',
    author_email='mario.balibrera@gmail.com',
    license='GPL-2.0-or-later',
    description='GNOme MOuse POsitioner',
    long_description='exposes mouse position on vanilla (non-x) ubuntu',
    packages=[
        'gnomopo'
    ],
    zip_safe = False,
    install_requires = [
        "fyg >= 0.1.7.9"
    ],
    entry_points = '''
        [console_scripts]
        gnomopo = gnomopo:invoke
    ''',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
