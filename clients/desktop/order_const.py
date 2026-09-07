
import base64
from PySide6.QtCore import QUrl
from PySide6.QtNetwork import QNetworkRequest

#local for test
credentials = "admin:impimp13"
strBaseUrl = "http://127.0.0.1:8000/orders-api/" 
# strBaseUrl = "https://orders.python1c.ru/orders-api/"

def getRequestAuth(strUrl: str = ""):
    url = QUrl(strBaseUrl+strUrl)
    request = QNetworkRequest(url) 
    request.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, "application/json")     
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    request.setRawHeader(b"Authorization", f"Basic {encoded_credentials}".encode('utf-8'))
    return request
     