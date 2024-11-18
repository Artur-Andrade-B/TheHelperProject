import os
from PySide6.QtCore import QStandardPaths

def open_documents_folder():
    path = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
    os.startfile(path)

def open_downloads_folder():
    path = QStandardPaths.writableLocation(QStandardPaths.DownloadLocation)
    os.startfile(path)

def open_desktop_folder():
    path = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
    os.startfile(path)
