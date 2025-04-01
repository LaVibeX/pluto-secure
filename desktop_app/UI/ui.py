import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTabWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QTextEdit, QCheckBox
)

class VaultTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Site", "Username", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def add_entry(self, site, username):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(site))
        self.table.setItem(row, 1, QTableWidgetItem(username))
        self.table.setItem(row, 2, QTableWidgetItem("🔓 ✏️ 🗑️"))

class AddCredentialTab(QWidget):
    def __init__(self, vault_tab):
        super().__init__()
        self.vault_tab = vault_tab
        layout = QVBoxLayout()

        self.site_input = QLineEdit()
        self.site_input.setPlaceholderText("Site (e.g., gmail.com)")
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username")
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.Password)

        self.show_password_cb = QCheckBox("Show Password")
        self.show_password_cb.toggled.connect(self.toggle_password_visibility)

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Notes (optional)")

        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_credential)

        layout.addWidget(QLabel("Add New Credential"))
        layout.addWidget(self.site_input)
        layout.addWidget(self.user_input)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.show_password_cb)
        layout.addWidget(self.notes_input)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def toggle_password_visibility(self, checked):
        if checked:
            self.pass_input.setEchoMode(QLineEdit.Normal)
        else:
            self.pass_input.setEchoMode(QLineEdit.Password)

    def save_credential(self):
        site = self.site_input.text()
        user = self.user_input.text()
        password = self.pass_input.text()
        if site and user and password:
            self.vault_tab.add_entry(site, user)
            QMessageBox.information(self, "Saved", f"Credential for {site} saved.")
            self.site_input.clear()
            self.user_input.clear()
            self.pass_input.clear()
            self.notes_input.clear()
            self.show_password_cb.setChecked(False)
        else:
            QMessageBox.warning(self, "Missing Info", "Please fill in all fields.")

class PlutoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pluto Password Manager")
        self.setGeometry(200, 200, 600, 400)

        tabs = QTabWidget()
        self.vault_tab = VaultTab()
        self.add_tab = AddCredentialTab(self.vault_tab)

        tabs.addTab(self.vault_tab, "🔐 Vault")
        tabs.addTab(self.add_tab, "➕ Add Credential")

        self.setCentralWidget(tabs)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlutoApp()
    window.show()
    sys.exit(app.exec_())
