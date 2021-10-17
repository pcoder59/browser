import sys
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtWebEngineWidgets import * 
from PyQt6.QtGui import *
with open("domains.txt") as f:
    domains = f.readlines()
    domains = [x.strip() for x in domains]

class PicButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)
    def sizeHint(self):
        return self.pixmap.size()

class MainWindow(QMainWindow):
    #initialize main window
    def __init__(self):
        super(MainWindow, self).__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("about:blank"))
        self.setCentralWidget(self.browser)
        self.showMaximized()

        #navbar
        navbar = QToolBar()
        self.addToolBar(navbar)

        backButton = PicButton(QPixmap("backArrow.png"))
        backButton.clicked.connect(self.browser.back)
        navbar.addWidget(backButton)

        forwardButton = PicButton(QPixmap("forwardArrow.png"))
        forwardButton.clicked.connect(self.browser.forward)
        navbar.addWidget(forwardButton)

        reloadButton = PicButton(QPixmap("refreashArrow.png"))
        reloadButton.clicked.connect(self.browser.reload)
        navbar.addWidget(reloadButton)

        self.urlBar = QLineEdit()
        self.urlBar.returnPressed.connect(self.navigate)
        navbar.addWidget(self.urlBar)

        self.browser.urlChanged.connect(self.update)

    def navigate(self):
        flag = False
        url = self.urlBar.text()
        for domain in domains:
            test = ("."+domain).lower()
            if(url.endswith(test)):
                self.browser.setUrl(QUrl("http://"+url))
                flag = True
        if flag == False:
            self.browser.setUrl(QUrl("https://duckduckgo.com/?q="+url))

    def update(self, q):
        self.urlBar.setText(q.toString())

app = QApplication(sys.argv)
QApplication.setApplicationName("Browser")
window = MainWindow()
app.exec()