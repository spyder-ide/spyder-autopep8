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

from spyderlib.qt.QtGui import (
    QWidget, QTextCursor, QVBoxLayout, QGroupBox, QScrollArea, QLabel,
    QCheckBox)

# Local imports
from spyderlib.baseconfig import get_translation
_ = get_translation("p_autopep8", dirname="spyderplugins")
from spyderlib.utils.qthelpers import get_icon, create_action
from spyderlib.py3compat import to_text_string

from spyderlib.plugins import SpyderPluginMixin, PluginConfigPage


class AutoPEP8ConfigPage(PluginConfigPage):
    """Widget with configuration options for line profiler
    """
    GROUPS = {
        "1": "Indentation",
        "2": "Whitespace",
        "3": "Blank line",
        "4": "Import",
        "5": "Line length",
        "6": "Deprecation",
        "7": "Statement",
        "9": "Runtime"}
    CODES = {
        # See http://pep8.readthedocs.org/en/latest/intro.html#error-codes
        "E101": "indentation contains mixed spaces and tabs",
        "E111": "indentation is not a multiple of four",
        "E112": "expected an indented block",
        "E113": "unexpected indentation",
        "E121": "continuation line indentation is not a multiple of four",
        "E122": "continuation line missing indentation or outdented",
        "E123": "closing bracket does not match indentation of opening"
            " bracket’s line",
        "E124": "closing bracket does not match visual indentation",
        "E125": "continuation line does not distinguish itself from next"
            " logical line",
        "E126": "continuation line over-indented for hanging indent",
        "E127": "continuation line over-indented for visual indent",
        "E128": "continuation line under-indented for visual indent",
        "E133": "closing bracket is missing indentation",
        "E201": "whitespace after ‘(‘",
        "E202": "whitespace before ‘)’",
        "E203": "whitespace before ‘:’",
        "E211": "whitespace before ‘(‘",
        "E221": "multiple spaces before operator",
        "E222": "multiple spaces after operator",
        "E223": "tab before operator",
        "E224": "tab after operator",
        "E225": "missing whitespace around operator",
        "E226": "missing whitespace around arithmetic operator",
        "E227": "missing whitespace around bitwise or shift operator",
        "E228": "missing whitespace around modulo operator",
        "E231": "missing whitespace after ‘,’",
        "E241": "multiple spaces after ‘,’",
        "E242": "tab after ‘,’",
        "E251": "unexpected spaces around keyword / parameter equals",
        "E261": "at least two spaces before inline comment",
        "E262": "inline comment should start with ‘# ‘",
        "E271": "multiple spaces after keyword",
        "E272": "multiple spaces before keyword",
        "E273": "tab after keyword",
        "E274": "tab before keyword",
        "E301": "expected 1 blank line, found 0",
        "E302": "expected 2 blank lines, found 0",
        "E303": "too many blank lines (3)",
        "E304": "blank lines found after function decorator",
        "E401": "multiple imports on one line",
        "E501": "line too long (82 > 79 characters)",
        "E502": "the backslash is redundant between brackets",
        "E701": "multiple statements on one line (colon)",
        "E702": "multiple statements on one line (semicolon)",
        "E703": "statement ends with a semicolon",
        "E711": "comparison to None should be ‘if cond is None:’",
        "E712": "comparison to True should be ‘if cond is True:’ or"
            " ‘if cond:’",
        "E721": "do not compare types, use ‘isinstance()’",
        "E901": "SyntaxError or IndentationError",
        "E902": "IOError",
        "W191": "indentation contains tabs",
        "W291": "trailing whitespace",
        "W292": "no newline at end of file",
        "W293": "blank line contains whitespace",
        "W391": "blank line at end of file",
        "W601": ".has_key() is deprecated, use ‘in’",
        "W602": "deprecated form of raising exception",
        "W603": "‘<>’ is deprecated, use ‘!=’",
        "W604": "backticks are deprecated, use ‘repr()’)"}


    def setup_page(self):
        # General options
        options_group = QGroupBox(_("Options"))
        passes_spin = self.create_spinbox(
            _("Additional pep8 passes: "), _("(-1 is infinite)"), 'passes',
            default=-1, min_=-1, max_=1000000, step=10)
        aggressive_spin = self.create_spinbox(
            _("Level of aggressivity: "), None, 'aggressive',
            default=0, min_=0, max_=2, step=1)

        # Enable/disable error codes
        fix_layout = QVBoxLayout()
        indent = QCheckBox(" ").sizeHint().width()
        last_group = ""
        FIX_LIST.sort(key=lambda item: item[0][1])
        for code, description in FIX_LIST:
            if code[1] != last_group:
                last_group = code[1]
                group = QGroupBox(_(self.GROUPS.get(code[1], "")))
                fix_layout.addWidget(group)
                group_layout = QVBoxLayout(group)
            if code not in DEFAULT_IGNORE:
                option = self.create_checkbox(code, code, default=True)
            else:
                option = self.create_checkbox(
                    "{code} ({warning})".format(
                        code=code, warning=_("UNSAFE")),
                    code, default=False)
            group_layout.addWidget(option)
            if code in self.CODES:
                label = QLabel("{autopep8} ({pep8}).".format(
                    autopep8=description.rstrip("."), pep8=self.CODES[code]))
            else:
                label = QLabel(_(description))
            label.setWordWrap(True)
            label.setIndent(indent)
            font = label.font()
            font.setPointSizeF(font.pointSize() * 0.9)
            label.setFont(font)
            group_layout.addWidget(label)

        # General layout
        options_layout = QVBoxLayout()
        options_layout.addWidget(passes_spin)
        options_layout.addWidget(aggressive_spin)
        options_group.setLayout(options_layout)

        widget_scroll = QWidget()
        widget_scroll.setLayout(fix_layout)
        fix_scroll = QScrollArea()
        fix_scroll.setWidget(widget_scroll)
        fix_scroll.setWidgetResizable(True)
        fig_out_layout = QVBoxLayout()
        fig_out_layout.addWidget(fix_scroll, 1)
        fix_group = QGroupBox(_("Errors/warnings to fix"))
        fix_group.setLayout(fig_out_layout)

        vlayout = QVBoxLayout()
        vlayout.addWidget(options_group)
        vlayout.addWidget(fix_group, 1)
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
        ignore = []
        for code, description in FIX_LIST:
            if not self.get_option(code):
                ignore.append(code)

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
                ignore.append("W391")

        # replace(): See qt doc for QTextCursor.selectedText()
        text_before = to_text_string(
            cursor.selectedText().replace("\u2029", "\n"))

        # Run autopep8
        options = ["", "--ignore", ",".join(ignore),
                   "--pep8-passes", str(self.get_option("passes")),
                   "--max-line-length",
                   str(self.window().editor.get_option("edge_line_column"))]
        for aggressive in range(self.get_option("aggressive")):
            options.append("--aggressive")
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
