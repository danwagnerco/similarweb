from distutils.core import setup

setup(
  name = "similarweb",
  packages = ["similarweb"],
  version = "0.1",
  description = "Python client for the SimilarWeb API",
  author = "Dan Wagner",
  author_email = "danwagnerco@gmail.com",
  url = "https://github.com/danwagnerco/similarweb",
  download_url = "https://github.com/danwagnerco/similarweb/tarball/0.1",
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

