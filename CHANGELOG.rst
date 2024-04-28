..
    Steps to update Changelog:
    0. Create a release on Github using semantic versioning
    1. Create a new Changelog entry above the previous with the standard headers and the date of release
    2. Copy/paste (until automated) each section from release notes to rst file
    3. Correct hyperlink syntax

datopy 0.0.1 (April 28, 2024)
=============================

..
    datopy is up and running

Summary
-------

Datopy is a package for simplifying the early stages of the data analysis workflow (getting data, modeling data, validating data, etc). It is first and foremost a personal use package; however, I prioritize extensibility and clear documentation, and I hope that other developers will find the package useful.

While I make no guarantees in the way of performance or functionality, datopy is now in more-or-less working order (parts of it, at least). Feel free to explore, sample, and extend.

This release includes some routines for data modeling (see `datopy.modeling`), ETL (Extract, Transform, Load; `datopy.etl`), and data inspection (`datopy.inspection`, `datopy.stylesheet`). Still to come: the `datopy.models` subpackage, which will include data models, validation, and processing routines for dealing with media metadata (`datopy.models.media`), animal data (`datopy.models.eco`), and global development indicators (`datopy.models.global`).

Here's a snapshot of what this release includes:

Exciting Features 🙌
--------------------

- Core data modeling/validation functionality and various workflow-related utilities

Stability and Performance ⚡️
---------------------------

- Extensive type checking and doctesting
- Continual performance and coverage testing via tox and Github actions
- Tested in Python 3.10 and Python 3.11 environments

Key Patches
-----------

- Improved type checking and examples https://github.com/bainmatt/datopy/pull/5
- Improved doctesting https://github.com/bainmatt/datopy/pull/6
- Improved environment management https://github.com/bainmatt/datopy/pull/7
- Better orchestration and unittesting suite https://github.com/bainmatt/datopy/pull/9
- Data validation schemes for retrieval and processing https://github.com/bainmatt/datopy/pull/14
- Generic Pydantic media model https://github.com/bainmatt/datopy/pull/28

..
    - Improved type checking and examples `(#5) <https://github.com/bainmatt/datopy/pull/5>`_
    - Improved doctesting `(#6) <https://github.com/bainmatt/datopy/pull/6>`_
    - Improved environment management `(#7) <https://github.com/bainmatt/datopy/pull/7>`_
    - Better orchestration and unittesting suite `(#9) <https://github.com/bainmatt/datopy/pull/9>`_
    - Data validation schemes for retrieval and processing `(#14) <https://github.com/bainmatt/datopy/pull/14>`_
    - Generic Pydantic media model `(#28) <https://github.com/bainmatt/datopy/pull/28>`_

Full Changelog: https://github.com/bainmatt/datopy/commits/v0.0.1