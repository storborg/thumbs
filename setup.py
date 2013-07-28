from setuptools import setup


setup(name="thumbs",
      version='0.1',
      description="Build thumbnails and HTML page.",
      long_description='',
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
      ],
      keywords='photos pics thumbnails images html',
      author='Scott Torborg',
      author_email='scott@cartlogic.com',
      url='http://github.com/storborg/thumbs',
      install_requires=[
      ],
      license='MIT',
      packages=['thumbs'],
      entry_points=dict(console_scripts=['thumbs=thumbs:main']),
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
