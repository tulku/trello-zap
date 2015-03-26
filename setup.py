from distutils.core import setup

setup(name='trello-zap',
      version='0.1',
      packages=['trello_zap'],
      scripts=['scripts/TrelloZap'],
      # metadata for upload to PyPI
      author="Lucas Chiesa",
      author_email="lucas@lessindustries.com",
      description="Super lightweight Production management using trello",
      license="Apache 2.0",
      keywords="pm, trello"
      )
