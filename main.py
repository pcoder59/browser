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
        self.showMaximized()

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        self.tabs.currentChanged.connect(self.currentChanged)

        self.tabs.setTabsClosable(True)

        self.tabs.tabCloseRequested.connect(self.closeTab)

        self.setCentralWidget(self.tabs)

        #navbar
        navbar = QToolBar()
        self.addToolBar(navbar)

        plusButton = PicButton(QPixmap("plus.png"))
        plusButton.clicked.connect(self.tabOpen)
        navbar.addWidget(plusButton)

        navbar.addSeparator()

        backButton = PicButton(QPixmap("backArrow.png"))
        backButton.clicked.connect(lambda: self.tabs.currentWidget().back())
        navbar.addWidget(backButton)

        navbar.addSeparator()

        forwardButton = PicButton(QPixmap("forwardArrow.png"))
        forwardButton.clicked.connect(lambda: self.tabs.currentWidget().forward())
        navbar.addWidget(forwardButton)

        navbar.addSeparator()

        reloadButton = PicButton(QPixmap("refreashArrow.png"))
        reloadButton.clicked.connect(lambda: self.tabs.currentWidget().reload())
        navbar.addWidget(reloadButton)

        navbar.addSeparator()

        self.urlBar = QLineEdit()
        self.urlBar.returnPressed.connect(self.navigate)
        navbar.addWidget(self.urlBar)

        navbar.addSeparator()

        #self.browser.urlChanged.connect(self.update)

        self.addTab()

    def closeTab(self, i):
        self.tabs.removeTab(i)

    def currentChanged(self, i):
        if i != -1:
            qurl = self.tabs.currentWidget().url()
            self.update(qurl, self.tabs.currentWidget())
            self.updateTitle(self.tabs.currentWidget())
        else:
            self.setWindowTitle("Browser")

    def updateTitle(self, browser):
        if browser != self.tabs.currentWidget():
            return
  
        title = self.tabs.currentWidget().page().title()
  
        self.setWindowTitle("% s - Browser" % title)

    def addTab(self, qurl = None, label="Blank"):
        if qurl is None:
            qurl = QUrl("https://www.duckduckgo.com")
        
        browser = QWebEngineView()

        browser.setUrl(qurl)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser = browser: self.update(qurl, browser))

        browser.loadFinished.connect(lambda _, i = i, browser = browser: self.tabs.setTabText(i, browser.page().title()))

    def tabOpen(self, i):
        print("yes")
        print(i)
        if(i == False):
            self.addTab()

    def navigate(self):
        flag = False
        url = self.urlBar.text()
        for domain in domains:
            test = ("."+domain).lower()
            if(url.endswith(test)):
                self.tabs.currentWidget().setUrl(QUrl("http://"+url))
                flag = True
        if flag == False:
            self.tabs.currentWidget().setUrl(QUrl("https://duckduckgo.com/?q="+url))

    def update(self, q, browser = None):
        if browser != self.tabs.currentWidget():
            return

        self.urlBar.setText(q.toString())

        self.urlBar.setCursorPosition(0)

app = QApplication(sys.argv)
QApplication.setApplicationName("Browser")
window = MainWindow()
app.exec()