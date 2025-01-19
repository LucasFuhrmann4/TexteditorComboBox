from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QHBoxLayout, QComboBox


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super(CentralWidget, self).__init__(parent)

        bar_layout = QHBoxLayout()

        self.comboBox = QComboBox()
        self.comboBox.addItem('')
        self.comboBox.addItem('Bold')
        self.comboBox.addItem('Italic')
        self.comboBox.addItem('Underline')
        self.comboBox.currentTextChanged.connect(self.handle_format_change)

        bar_layout.addWidget(self.comboBox)

        self.__text_edit = QTextEdit()

        layout = QVBoxLayout()
        layout.addLayout(bar_layout)
        layout.addWidget(self.__text_edit)

        self.setLayout(layout)

    @pyqtSlot(str)
    def set_text(self, text):
        self.__text_edit.setText(text)

    def get_text(self):
        return self.__text_edit.toPlainText()

    @pyqtSlot(QFont)
    def set_font(self, font):
        self.__text_edit.setFont(font)

    @pyqtSlot(str)
    def handle_format_change(self, format_option):
        cursor = self.__text_edit.textCursor()
        format = cursor.charFormat()

        if format_option == 'Bold':
            is_bold = format.fontWeight() == QFont.Weight.Bold
            format.setFontWeight(QFont.Weight.Normal if is_bold else QFont.Weight.Bold)
        elif format_option == 'Italic':
            is_italic = format.fontItalic()
            format.setFontItalic(not is_italic)
        elif format_option == 'Underline':
            is_underline = format.fontUnderline()
            format.setFontUnderline(not is_underline)

        # Apply the format and reset the ComboBox selection
        cursor.setCharFormat(format)
        self.__text_edit.setTextCursor(cursor)

        # Reset the comboBox to the default (empty) selection
        self.comboBox.blockSignals(True)  # Prevent triggering `currentTextChanged` again
        self.comboBox.setCurrentIndex(0)
        self.comboBox.blockSignals(False)
