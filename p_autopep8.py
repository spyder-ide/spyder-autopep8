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

        FIX_LIST = [(code.strip(), description.strip())
                    for code, description in autopep8.supported_fixes()]
        DEFAULT_IGNORE = ["E711", "E712", "W6"]
    except AttributeError:
        has_autopep8_fix_string = False
except ImportError:
    is_autopep8_installed = False

from spyderlib.qt.QtGui import QWidget, QTextCursor, QVBoxLayout, QGroupBox

# Local imports
from spyderlib.baseconfig import get_translation
_ = get_translation("p_autopep8", dirname="spyderplugins")
from spyderlib.utils.qthelpers import get_icon, create_action
from spyderlib.py3compat import to_text_string

from spyderlib.plugins import SpyderPluginMixin, PluginConfigPage


class AutoPEP8ConfigPage(PluginConfigPage):
    """Widget with configuration options for line profiler
    """
    def setup_page(self):
        fix_group = QGroupBox(_("Errors/warnings to fix"))
        fix_layout = QVBoxLayout()

        for code, description in FIX_LIST:
            if code not in DEFAULT_IGNORE:
                option = self.create_checkbox(
                    "{code} - {description}".format(
                        code=code, description=_(description)),
                    code, default=True)
            else:
                option = self.create_checkbox(
                    "{code} - ({warning}) {description}".format(
                        code=code, description=_(description),
                        warning=_("UNSAFE")),
                    code, default=False)
            fix_layout.addWidget(option)
        fix_group.setLayout(fix_layout)

        vlayout = QVBoxLayout()
        vlayout.addWidget(fix_group)
        vlayout.addStretch(1)
        self.setLayout(vlayout)


class AutoPEP8(QWidget, SpyderPluginMixin):  # pylint: disable=R0904
    """Python source code automatic formatting based on autopep8.

    QObject is needed to register the action.
    """
    CONF_SECTION = "autopep8"
    CONFIGWIDGET_CLASS = AutoPEP8ConfigPage

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        SpyderPluginMixin.__init__(self, parent)

    #------ SpyderPluginMixin API --------------------------------------------
    def get_plugin_title(self):
        """Return widget title"""
        return _("Autopep8")

    def get_plugin_icon(self):
        """Return widget icon"""
        return get_icon('profiler.png')

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

        # Retrieve active fixes
        fixes = [item[0] for item in FIX_LIST if self.get_option(item[0])]

        # Retrieve text of current opened file
        editorstack = self.main.editor.get_current_editorstack()
        index = editorstack.get_stack_index()
        finfo = editorstack.data[index]
        editor = finfo.editor
        cursor = editor.textCursor()
        cursor.beginEditBlock()  # Start cancel block
        options = [""]
        if not cursor.hasSelection():
            position_start = 0
            cursor.select(QTextCursor.Document)  # Select all
        else:
            # Select whole lines
            position_end = cursor.selectionEnd()
            cursor.setPosition(cursor.selectionStart())
            cursor.movePosition(QTextCursor.StartOfLine)
            position_start = cursor.position()
            cursor.setPosition(position_end, QTextCursor.KeepAnchor)
            cursor.movePosition(QTextCursor.StartOfLine,
                                QTextCursor.KeepAnchor)
            position_lastline_start = cursor.position()
            if not position_end == position_lastline_start:
                cursor.movePosition(QTextCursor.EndOfLine,
                                    QTextCursor.KeepAnchor)
                # Select EOL if not on a new line
                if not position_lastline_start == cursor.position():
                    cursor.movePosition(QTextCursor.Right,
                                        QTextCursor.KeepAnchor)

            # Disable checks of newlines at end of file
            if not cursor.atEnd():
                fixes = [fix for fix in fixes if not fix == "W391"]

        # replace(): See qt doc for QTextCursor.selectedText()
        text_before = to_text_string(
            cursor.selectedText().replace("\u2029", "\n"))

        # Run autopep8
        options = ["", "--select", ",".join(fixes)]
        options = autopep8.parse_args(options)[0]
        text_after = autopep8.fix_string(text_before, options)

        # Apply new text if needed
        if text_before != text_after:
            cursor.insertText(text_after)  # Change text

        cursor.endEditBlock()  # End cancel block

        # Select changed text
        position_end = cursor.position()
        cursor.setPosition(position_start, QTextCursor.MoveAnchor)
        cursor.setPosition(position_end, QTextCursor.KeepAnchor)
        editor.setTextCursor(cursor)

        self.main.statusBar().showMessage(
            _("Autopep8 finished !"))


#==============================================================================
# The following statements are required to register this 3rd party plugin:
#==============================================================================
PLUGIN_CLASS = AutoPEP8  # pylint: disable=C0103
