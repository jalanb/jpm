"""Set up the jpm project"""


from setuptools import setup


import jpm


setup(
    name='jpm',
    version=jpm.__version__,
    url='https://github.com/jalanb/jpm',
    license='MIT License',
    author="jalanb",
    author_email='jpm@al-got-rhythm.net',
    description='Just Play Music',
    platforms='any',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Development Status :: 1 - Planning',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Topic :: Multimedia :: Sound/Audio :: Players',
    ],
    scripts=['bin/jpm'],
    install_requires=['python-mpd2'],
    test_suite='nose.collector',
    tests_require=['nose'],
    extras_require={
        'docs': ['Sphinx'],
        'development': ['pudb'],
        'testing': ['nose'],
    }
)
