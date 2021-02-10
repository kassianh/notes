import sys

import PyQt5.QtGui as qtgui
import PyQt5.QtWidgets as qtwdgt
import PyQt5.QtCore as qtcore
import PyQt5.QtSql as qtsql


class MainWindow(qtwdgt.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.colour = None

        self.setWindowTitle("Notes")
        self.setWindowIcon(qtgui.QIcon('notebook.png')) 

        # Initialize
        self.input_field = qtwdgt.QTextEdit()
        self.label = qtwdgt.QLabel("0/140")
        widget = qtwdgt.QWidget()        
        mapper = qtwdgt.QDataWidgetMapper(self)

        # Setup model
        self.model = qtsql.QSqlTableModel()
        self.model.setTable("notes")
        self.model.select()
        self.model.setEditStrategy(qtsql.QSqlTableModel.OnManualSubmit)
        self.model.setHeaderData(0, qtcore.Qt.Horizontal, "id")
        self.model.setHeaderData(1, qtcore.Qt.Horizontal, "text")
        self.model.setHeaderData(2, qtcore.Qt.Horizontal, "colour")
        self.model.setHeaderData(3, qtcore.Qt.Horizontal, "family")
        self.model.setHeaderData(4, qtcore.Qt.Horizontal, "style")
        self.model.setHeaderData(5, qtcore.Qt.Horizontal, "weight")
        self.model.setHeaderData(6, qtcore.Qt.Horizontal, "point_size")
        self.model.setHeaderData(7, qtcore.Qt.Horizontal, "strikeout")
        self.model.setHeaderData(8, qtcore.Qt.Horizontal, "underline")

        # Retrieve note from model
        if self.model.record(0).value("id") is not None:
            self.colour = self.model.record(0).value("colour")
            family = self.model.record(0).value("family")
            style = int(self.model.record(0).value("style"))
            weight = int(self.model.record(0).value("weight"))
            point_size = int(self.model.record(0).value("point_size"))
            strikeout = int(self.model.record(0).value("strikeout"))
            underline = int(self.model.record(0).value("underline"))

            self.input_field.setStyleSheet("color: %s" % self.colour)

            font = qtgui.QFont()

            font.setFamily(family)
            font.setStyle(style)
            font.setWeight(weight)
            font.setPointSize(point_size)
            font.setStrikeOut(strikeout)
            font.setUnderline(underline)

            self.input_field.setFont(font)

        # Map model to input_field
        mapper.setModel(self.model)
        mapper.addMapping(self.input_field, 1)
        mapper.toFirst()

        layout = qtwdgt.QVBoxLayout()

        self.input_field.setWordWrapMode(qtgui.QTextOption.WordWrap)

        # Update character count label with 
        self.input_field.textChanged.connect(lambda: self.on_change_character_label(len(self.input_field.toPlainText())))

        self.label.setAlignment(qtcore.Qt.AlignRight)
        self.label.setStyleSheet("color: gray")

        layout.addWidget(self.input_field)
        layout.addWidget(self.label)

        # Font anomaly - will not change initially without saving
        self.on_save()

        # Set character count label
        self.on_change_character_label(len(self.input_field.toPlainText()))

        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.setup_menu()

    # Create menu
    def setup_menu(self):
        new_action = qtwdgt.QAction("&New", self)
        new_action.setStatusTip("Create new note.")
        new_action.triggered.connect(self.on_new)
        new_action.setShortcut(qtgui.QKeySequence("Ctrl+N"))

        save_action = qtwdgt.QAction("&Save", self)
        save_action.setStatusTip("Save this note.")
        save_action.triggered.connect(self.on_save)
        save_action.setShortcut(qtgui.QKeySequence("Ctrl+S"))

        exit_action = qtwdgt.QAction("&Exit", self)
        exit_action.setStatusTip("Exit this application.")
        exit_action.triggered.connect(self.on_exit)
        exit_action.setShortcut(qtgui.QKeySequence("Ctrl+W"))

        undo_action = qtwdgt.QAction("&Undo", self)
        undo_action.setStatusTip("Undo your last word.")
        undo_action.triggered.connect(self.input_field.undo)
        undo_action.setShortcut(qtgui.QKeySequence("Ctrl+Z"))

        redo_action = qtwdgt.QAction("&Redo", self)
        redo_action.setStatusTip("Redo your last word.")
        redo_action.triggered.connect(self.input_field.redo)
        redo_action.setShortcut(qtgui.QKeySequence("Ctrl+Y"))

        cut_action = qtwdgt.QAction("Cu&t", self)
        cut_action.setStatusTip("Cut selection.")
        cut_action.triggered.connect(self.input_field.cut)
        cut_action.setShortcut(qtgui.QKeySequence("Ctrl+X"))

        copy_action = qtwdgt.QAction("&Copy", self)
        copy_action.setStatusTip("Copy selection.")
        copy_action.triggered.connect(self.input_field.copy)
        copy_action.setShortcut(qtgui.QKeySequence("Ctrl+C"))

        paste_action = qtwdgt.QAction("&Paste", self)
        paste_action.setStatusTip("Paste last copied.")
        paste_action.triggered.connect(self.input_field.paste)
        paste_action.setShortcut(qtgui.QKeySequence("Ctrl+P"))

        select_all_action = qtwdgt.QAction("&Select All", self)
        select_all_action.setStatusTip("Select all in text field.")
        select_all_action.triggered.connect(self.input_field.selectAll)
        select_all_action.setShortcut(qtgui.QKeySequence("Ctrl+A"))

        colour_action = qtwdgt.QAction("&Change Colour", self)
        colour_action.setStatusTip("Change colour of text in field.")
        colour_action.triggered.connect(self.on_colour_change)
        colour_action.setShortcut(qtgui.QKeySequence("Ctrl+O"))

        font_action = qtwdgt.QAction("Change &Font", self)
        font_action.setStatusTip("Change font of text in field.")
        font_action.triggered.connect(self.on_font_change)
        font_action.setShortcut(qtgui.QKeySequence("Ctrl+F"))

        self.setStatusBar(qtwdgt.QStatusBar(self))

        menu = self.menuBar()

        file_menu = menu.addMenu("&File")
        file_menu.addAction(save_action)
        file_menu.addAction(new_action)
        file_menu.addAction(exit_action)

        edit_menu = menu.addMenu("&Edit")
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        edit_menu.addSeparator()
        edit_menu.addAction(select_all_action)

        format_menu = menu.addMenu("F&ormat")
        format_menu.addAction(colour_action)
        format_menu.addAction(font_action)
    
    # Responsible for updating label with character count
    def on_change_character_label(self, length):
        if length > 140:
            self.input_field.textCursor().deletePreviousChar()
            length = 140

        self.label.setText(str(length) + "/140")

    # Colour picker
    def on_colour_change(self):
        previous_colour = self.colour
        self.colour = qtwdgt.QColorDialog.getColor()
        
        # Check if pressed cancel
        if self.colour.isValid():
            self.input_field.setStyleSheet("color: %s" % self.colour.name()) 

        # Reset to previous colour
        else:
            self.colour = previous_colour

    # Font changer
    def on_font_change(self):
        font, ok = qtwdgt.QFontDialog.getFont() 

        if ok:
            self.input_field.setFont(font)

    # Save text, colour, and font
    def on_save(self):
        record = self.model.record(0)

        # Check if no last record
        if record.value("id") is None:
            self.model.insertRows(0, 1)

        text = self.input_field.toPlainText()

        # Set colour to black as default
        if self.colour is None:
            if record.value("colour") is None:
                self.colour = "#000000"

        # Retrieve values and assign to record
        record.setValue("text", text)
        record.setValue("colour", self.colour)
        record.setValue("family", self.input_field.currentFont().family())
        record.setValue("style", self.input_field.currentFont().style())
        record.setValue("weight", self.input_field.currentFont().weight())
        record.setValue("point_size", self.input_field.currentFont().pointSize())
        record.setValue("strikeout", self.input_field.currentFont().strikeOut())
        record.setValue("underline", self.input_field.currentFont().underline())        

        # Submit
        self.model.setRecord(0, record)
        self.model.submitAll()

    # Create new note - overwrite old
    def on_new(self):
        warning_dialog = WarningDialog("New", "The old note will be overwritten, is that ok?", self)
        if warning_dialog.exec():
            self.input_field.clear()

            self.colour = "#000000"
            self.input_field.setStyleSheet("color: %s" % self.colour) 

            font = qtgui.QFont()
            self.input_field.setFont(font)

            self.on_save()

    # Exit program
    def on_exit(self):
        warning_dialog = WarningDialog("Exit", "Do you want to exit?", self)
        if warning_dialog.exec():
            self.on_save()
            db.close()
            sys.exit(0)

# Custom dialog creating new note and exiting program
class WarningDialog(qtwdgt.QDialog):

    def __init__(self, window_title, message, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle(window_title)

        # Ok | Cancel buttons
        button = qtwdgt.QDialogButtonBox.Ok | qtwdgt.QDialogButtonBox.Cancel

        self.button_box = qtwdgt.QDialogButtonBox(button)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout = qtwdgt.QVBoxLayout()

        self.message = qtwdgt.QLabel(message)

        self.layout.addWidget(self.message)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)


if __name__ == '__main__':
    
    # Add database
    db = qtsql.QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('notes.db')

    app = qtwdgt.QApplication(sys.argv)

    # Open database
    if not db.open():
        QMessageBox.critical(
            None,
            "Notes - Error!",
            "Database Error: %s" % db.lastError().databaseText(),
        )

        sys.exit(1)

    # Create table - will only run first time
    createTableQuery = qtsql.QSqlQuery()
    createTableQuery.exec(
        """
        CREATE TABLE notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            text VARCHAR(140) NOT NULL,
            colour VARCHAR(7) NOT NULL,
            family VARCHAR(50) NOT NULL,
            style INT NOT NULL,
            weight INT NOT NULL,
            point_size INT NOT NULL,
            strikeout INT,
            underline INT
        )
        """
    )

    window = MainWindow()
    window.show()
    app.exec()