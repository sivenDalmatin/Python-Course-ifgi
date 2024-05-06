#import required classes
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWebKitWidgets import QWebView

#create instance of QWebView
qwc = QWebView()
#configure correct Url to access
qwc.load(QUrl("https://de.wikipedia.org/wiki/[%Name%]"))
#open new window in QGIS with the URL
qwc.show()