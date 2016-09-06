spyder.autopep8
===============

Description
-----------

This is a plugin to run the `autopep8 <https://pypi.python.org/pypi/autopep8>`_ python linter from within the python IDE `spyder <https://github.com/spyder-ide/spyder>`_.


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
