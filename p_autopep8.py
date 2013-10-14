# -*- coding: utf-8 -*-
u"""
:author: Joseph Martinot-Lagarde

Created on Sat Jan 19 14:57:57 2013
"""
from __future__ import (
    print_function, unicode_literals, absolute_import, division)

try:
    import autopep8
    is_autopep8_installed = True

    # Check version
    try:
        autopep8.fix_string
        has_autopep8_fix_string = True
    except AttributeError:
        has_autopep8_fix_string = False
except ImportError:
    is_autopep8_installed = False

from spyderlib.qt.QtGui import QWidget, QTextCursor

# Local imports
from spyderlib.baseconfig import get_translation
_ = get_translation("p_autopep8", dirname="spyderplugins")
from spyderlib.utils.qthelpers import create_action
from spyderlib.py3compat import to_text_string

from spyderlib.plugins import SpyderPluginMixin


class AutoPEP8(QWidget, SpyderPluginMixin):  # pylint: disable=R0904
    """Python source code automatic formatting based on autopep8.

    QObject is needed to register the action.
    """
    CONF_SECTION = "Autopep8"

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        SpyderPluginMixin.__init__(self, parent)

    #------ SpyderPluginMixin API --------------------------------------------
    def on_first_registration(self):
        """Action to be performed on first plugin registration"""
        pass

    def register_plugin(self):
        """Register plugin in Spyder's main window"""
        autopep8_act = create_action(
            self, _("Run autopep8 code autoformatting"),
            triggered=self.run_autopep8)
        autopep8_act.setEnabled(is_autopep8_installed
                                and has_autopep8_fix_string)
        self.register_shortcut(autopep8_act, context="Editor",
                               name="Run autoformatting", default="Shift+F8")

        self.main.source_menu_actions += [None, autopep8_act]
        self.main.editor.pythonfile_dependent_actions += [autopep8_act]

    def refresh_plugin(self):
        """Refresh autopep8 widget"""
        pass

    def apply_plugin_settings(self, options):
        """Apply configuration file's plugin settings"""
        pass

    #------ Public API --------------------------------------------------------
    def run_autopep8(self):
        """Format code with autopep8"""
        if not is_autopep8_installed:
            self.main.statusBar().showMessage(
                _("Unable to run: the 'autopep8' python module is not"
                  " installed."))
            return
        if not has_autopep8_fix_string:
            self.main.statusBar().showMessage(
                _("Unable to run: the the minimum version of 'autopep8' python"
                  " module is 0.8.6, please upgrade."))
            return

        # Retrieve text of current opened file
        editorstack = self.main.editor.get_current_editorstack()
        index = editorstack.get_stack_index()
        finfo = editorstack.data[index]
        editor = finfo.editor
        text_before = to_text_string(editor.toPlainText())

        # Run autopep8
        text_after = autopep8.fix_string(text_before)

        # Apply new text if needed
        if text_before != text_after:
            cursor = editor.textCursor()
            cursor.beginEditBlock()  # Start cancel block
            cursor.select(QTextCursor.Document)  # Select all
            cursor.insertText(text_after)  # Change text
            cursor.endEditBlock()  # End cancel block

        self.main.statusBar().showMessage(
            _("Autopep8 finished !"))


#==============================================================================
# The following statements are required to register this 3rd party plugin:
#==============================================================================
PLUGIN_CLASS = AutoPEP8  # pylint: disable=C0103
