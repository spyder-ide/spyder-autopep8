# -*- coding: utf-8 -*-
"""
:author: Joseph Martinot-Lagarde

Created on Sat Jan 19 14:57:57 2013
"""

# Standard library imports
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

# Third party imports
ERR_MSG = ''
try:
    import autopep8

    try:
        FIX_LIST = [(code.strip(), description.strip())
                    for code, description in autopep8.supported_fixes()]
        DEFAULT_IGNORE = ["E711", "E712", "W6"]
    except AttributeError:
        ERR_MSG = "Please install autopep8 >= 1.0, and pep8 >= 1.4.2."
except ImportError:
    ERR_MSG = "Please install autopep8 >= 1.0, and pep8 >= 1.4.2."

from qtpy.QtWidgets import (QWidget, QVBoxLayout, QGroupBox,
                            QScrollArea, QLabel, QCheckBox)
from qtpy.QtGui import QTextCursor

from spyder.config.base import get_translation
from spyder.config.gui import fixed_shortcut
from spyder.plugins import SpyderPluginMixin, PluginConfigPage
from spyder.utils.qthelpers import get_icon, create_action
from spyder.utils import icon_manager as ima

try:
    from spyder.py3compat import to_text_string
except ImportError:
    # Python 2
    to_text_string = unicode


_ = get_translation("autopep8", dirname="spyder_autopep8")


class AutoPEP8ConfigPage(PluginConfigPage):
    """
    Widget with configuration options for line profiler.
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
        "W6": "apply, except, exec, execfile, exitfunc, has_key, idioms,"
        " import, methodattrs, ne, numliterals, operator, paren, reduce,"
        " renames, repr, standarderror, sys_exc, throw, tuple_params,"
        " types, xreadlines",
        "W601": ".has_key() is deprecated, use ‘in’",
        "W602": "deprecated form of raising exception",
        "W603": "‘<>’ is deprecated, use ‘!=’",
        "W604": "backticks are deprecated, use ‘repr()’)"}

    def setup_page(self):
        if ERR_MSG:
            label = QLabel(_("Could not load plugin:\n{0}".format(ERR_MSG)))
            layout = QVBoxLayout()
            layout.addWidget(label)
            self.setLayout(layout)
            return

        # Layout parameter
        indent = QCheckBox().sizeHint().width()

        # General options
        options_group = QGroupBox(_("Options"))
        # Hack : the spinbox widget will be added to self.spinboxes
        spinboxes_before = set(self.spinboxes)
        passes_spin = self.create_spinbox(
            _("Number of pep8 passes: "), "", 'passes',
            default=0, min_=0, max_=1000000, step=1)
        spinbox = set(self.spinboxes) - spinboxes_before
        spinbox = spinbox.pop()
        spinbox.setSpecialValueText(_("Infinite"))
        aggressive1_checkbox = self.create_checkbox(
            "Aggressivity level 1", "aggressive1", default=False)
        aggressive1_label = QLabel(_(
            "Allow possibly unsafe fixes (E711 and W6), shorten lines"
            " and remove trailing whitespace more aggressively (in"
            " docstrings and multiline strings)."))
        aggressive1_label.setWordWrap(True)
        aggressive1_label.setIndent(indent)
        font_description = aggressive1_label.font()
        font_description.setPointSizeF(font_description.pointSize() * 0.9)
        aggressive1_label.setFont(font_description)
        aggressive2_checkbox = self.create_checkbox(
            "Aggressivity level 2", "aggressive2", default=False)
        aggressive2_label = QLabel(_(
            "Allow more possibly unsafe fixes (E712) and shorten lines."))
        aggressive2_label.setWordWrap(True)
        aggressive2_label.setIndent(indent)
        aggressive2_label.setFont(font_description)

        aggressive1_checkbox.toggled.connect(
            aggressive2_checkbox.setEnabled)
        aggressive1_checkbox.toggled.connect(
            aggressive2_label.setEnabled)
        aggressive2_checkbox.setEnabled(aggressive1_checkbox.isChecked())
        aggressive2_label.setEnabled(aggressive1_checkbox.isChecked())

        # Enable/disable error codes
        fix_layout = QVBoxLayout()
        last_group = ""
        FIX_LIST.sort(key=lambda item: item[0][1])
        for code, description in FIX_LIST:
            # Create a new group if necessary
            if code[1] != last_group:
                last_group = code[1]
                group = QGroupBox(_(self.GROUPS.get(code[1], "")))
                fix_layout.addWidget(group)
                group_layout = QVBoxLayout(group)

            # Checkbox for the option
            text = code
            default = True
            if code in DEFAULT_IGNORE:
                text += _(" (UNSAFE)")
                default = False
            option = self.create_checkbox(text, code, default=default)

            # Label for description
            if code in self.CODES:
                label = QLabel("{autopep8} ({pep8}).".format(
                    autopep8=_(description).rstrip("."),
                    pep8=self.CODES[code]))
            else:
                label = QLabel(_(description))
            label.setWordWrap(True)
            label.setIndent(indent)
            label.setFont(font_description)

            # Add widgets to layout
            option_layout = QVBoxLayout()
            option_layout.setSpacing(0)
            option_layout.addWidget(option)
            option_layout.addWidget(label)
            group_layout.addLayout(option_layout)

            # Special cases
            if code in ("E711", "W6"):
                aggressive1_checkbox.toggled.connect(option.setEnabled)
                aggressive1_checkbox.toggled.connect(label.setEnabled)
                option.setEnabled(aggressive1_checkbox.isChecked())
                label.setEnabled(aggressive1_checkbox.isChecked())
            if code == "E712":
                def e712_enabled():
                    enabled = (aggressive1_checkbox.isChecked()
                               and aggressive2_checkbox.isChecked())
                    option.setEnabled(enabled)
                    label.setEnabled(enabled)
                aggressive1_checkbox.toggled.connect(e712_enabled)
                aggressive2_checkbox.toggled.connect(e712_enabled)
                e712_enabled()

        # General layout
        aggressive2_layout = QVBoxLayout()
        margins = aggressive2_layout.contentsMargins()
        margins.setLeft(indent)
        aggressive2_layout.setContentsMargins(margins)
        aggressive2_layout.addWidget(aggressive2_checkbox)
        aggressive2_layout.addWidget(aggressive2_label)

        options_layout = QVBoxLayout()
        options_layout.addWidget(passes_spin)
        options_layout.addWidget(aggressive1_checkbox)
        options_layout.addWidget(aggressive1_label)
        options_layout.addLayout(aggressive2_layout)
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


class DummyDock(object):

    def close(self):
        pass


class AutoPEP8(SpyderPluginMixin):  # pylint: disable=R0904
    """Python source code automatic formatting based on autopep8.

    QObject is needed to register the action.
    """
    CONF_SECTION = "spyder.autopep8"
    CONFIGWIDGET_CLASS = AutoPEP8ConfigPage

    def __init__(self, main):
        super(AutoPEP8, self).__init__(main)
        self.dockwidget = DummyDock()

    # --- SpyderPlugin API ----------------------------------------------------
    def get_plugin_title(self):
        """Return widget title."""
        return _("Autopep8")

    def get_plugin_icon(self):
        """Return widget icon."""
        return ima.icon(self.CONF_SECTION)

    def register_plugin(self):
        """Register plugin in Spyder's main window."""
        autopep8_act = create_action(
            self.main, _("Run autopep8 code autoformatting"),
            icon=self.get_plugin_icon(),
            triggered=self.run_autopep8)
        fixed_shortcut("Shift+F8", self.main,
                       self.run_autopep8)
        self.main.source_menu_actions += [None, autopep8_act]
        self.main.editor.pythonfile_dependent_actions += [autopep8_act]

    def apply_plugin_settings(self, options):
        """Needs to be redefined."""
        pass

    def closing_plugin(self, cancelable=False):
        """Perform actions before parent main window is closed."""
        return True

    # --- Public API ---------------------------------------------------------
    def run_autopep8(self):
        """Format code with autopep8."""
        if ERR_MSG:
            self.main.statusBar().showMessage(
                _("Unable to run: {0}".format(ERR_MSG)))
            return

        # Retrieve active fixes
        ignore = []
        for code, description in FIX_LIST:
            if not self.get_option(code, True):
                ignore.append(code)

        # Retrieve text of current opened file
        editorstack = self.main.editor.get_current_editorstack()
        index = editorstack.get_stack_index()
        finfo = editorstack.data[index]
        editor = finfo.editor
        cursor = editor.textCursor()
        cursor.beginEditBlock()  # Start cancel block
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
        line_length = self.main.window().editor.get_option("edge_line_column")
        options = ["", "--ignore", ",".join(ignore),
                   "--pep8-passes", str(self.get_option("passes", 0) - 1),
                   "--max-line-length", str(line_length)]
        if self.get_option("aggressive1", False):
            options.append("--aggressive")
            if self.get_option("aggressive2", False):
                options.append("--aggressive")
        options = autopep8.parse_args(options)
        text_after = autopep8.fix_code(text_before, options)

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
