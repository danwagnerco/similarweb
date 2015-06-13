from setuptools import setup

__version__ = None
with open("similarweb/version.py") as f:
  exec(f.read())

setup(
  name = "similarweb",
  packages = ["similarweb"],
  version = __version__,
  description = "Python client for the SimilarWeb API",
  author = "Dan Wagner",
  author_email = "danwagnerco@gmail.com",
  url = "https://github.com/danwagnerco/similarweb",
  install_requires = [
      "requests>=2.7.0"
      ],
  classifiers = [
      "Development Status :: 3 - Alpha",
      "Environment :: Console",
      "Intended Audience :: Developers",
      "Operating System :: OS Independent",
      "Programming Language :: Python"
      ],
  keywords = "similarweb"
)

