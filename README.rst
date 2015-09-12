spyder.autopep8
===============

Description
-----------

This is a plugin to run the `autopep8 <https://pypi.python.org/pypi/autopep8>`_ python linter from within `spyder <https://github.com/spyder-ide/spyder>`_ editor.


Requirements
------------
::

  spyder
  autopep8


Install instructions
--------------------
::

  pip install spyplugins.ui.autopep8


Usage
-----

Press Shift+F8 (default) to run autopep8 on the current file or go to ``Source > Run autopep8 code autoformatting``.

If some text is selected, autopep8 will run on this text only.

Informations about the execution will be displayed in the statusbar.
