spyder-autopep8
===============

Project details
---------------
|gitter| |backers| |sponsors|

.. |gitter| image:: https://badges.gitter.im/spyder-ide/public.svg
   :target: https://gitter.im/spyder-ide/public
   :alt: Join the chat at https://gitter.im/spyder-ide/public
.. |backers| image:: https://opencollective.com/spyder/backers/badge.svg?color=blue
   :target: #backers
   :alt: OpenCollective Backers
.. |sponsors| image:: https://opencollective.com/spyder/sponsors/badge.svg?color=blue
   :target: #sponsors
   :alt: OpenCollective Sponsors

Description
-----------

This is a plugin to run the `autopep8 <https://pypi.python.org/pypi/autopep8>`_ python linter from within the python IDE `spyder <https://github.com/spyder-ide/spyder>`_.


Important Announcement: Spyder is unfunded!
-------------------------------------------

Since mid November/2017, `Anaconda, Inc`_ has
stopped funding Spyder development, after doing it for the past 18
months. Because of that, development will focus from now on maintaining
Spyder 3 at a much slower pace than before.

If you want to contribute to maintain Spyder, please consider donating at

https://opencollective.com/spyder

We appreciate all the help you can provide us and can't thank you enough for
supporting the work of Spyder devs and Spyder development.

If you want to know more about this, please read this
`page`_.


.. _Anaconda, Inc: https://www.anaconda.com/
.. _page: https://github.com/spyder-ide/spyder/wiki/Anaconda-stopped-funding-Spyder


Important
---------
**Spyder** plugin support will be released with version 3.0 (Still in Beta).

If you want to try out this plugin you need to use the latest development version of **Spyder** (**master** branch).


Requirements
------------
::

  spyder
  autopep8


Install instructions
--------------------

See https://github.com/spyder-ide/spyder/wiki/User-plugins, but in short:

::

  pip install spyder.autopep8


Usage
-----

Press Shift+F8 (default) to run autopep8 on the current file or go to ``Source > Run autopep8 code autoformatting``.

If some text is selected, autopep8 will run on this text only.

Informations about the execution will be displayed in the statusbar.

Screenshot
----------
Autopep8 preferences:

.. image:: img_src/screenshot_preferences.png

Contributing
------------

Everyone is welcome to contribute!

Backers
~~~~~~~

Support us with a monthly donation and help us continue our activities.

.. image:: https://opencollective.com/spyder/backers.svg
   :target: https://opencollective.com/spyder#support
   :alt: Backers

Sponsors
~~~~~~~~

Become a sponsor to get your logo on our README on Github.

.. image:: https://opencollective.com/spyder/sponsors.svg
   :target: https://opencollective.com/spyder#support
   :alt: Sponsors
