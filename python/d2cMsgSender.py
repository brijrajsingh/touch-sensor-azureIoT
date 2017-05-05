import base64
import hmac
import hashlib
import time
import requests
import urllib
import RPi.GPIO as GPIO
import time
from time import gmtime, strftime

GPIO.VERSION
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.IN)

class D2CMsgSender:

    API_VERSION = '2016-02-03'
    TOKEN_VALID_SECS = 10
    TOKEN_FORMAT = 'SharedAccessSignature sig=%s&se=%s&skn=%s&sr=%s'

    def __init__(self, connectionString=None):
        if connectionString != None:
            iotHost, keyName, keyValue = [sub[sub.index('=') + 1:] for sub in connectionString.split(";")]
            self.iotHost = iotHost
            self.keyName = keyName
            self.keyValue = keyValue

    def _buildExpiryOn(self):
        return '%d' % (time.time() + self.TOKEN_VALID_SECS)

    def _buildIoTHubSasToken(self, deviceId):
        resourceUri = '%s/devices/%s' % (self.iotHost, deviceId)
        targetUri = resourceUri.lower()
        expiryTime = self._buildExpiryOn()
        toSign = '%s\n%s' % (targetUri, expiryTime)
        key = base64.b64decode(self.keyValue.encode('utf-8'))
        signature = urllib.quote(
            base64.b64encode(
                hmac.HMAC(key, toSign.encode('utf-8'), hashlib.sha256).digest()
            )
        ).replace('/', '%2F')
        return self.TOKEN_FORMAT % (signature, expiryTime, self.keyName, targetUri)

    def sendD2CMsg(self, deviceId, message):
        sasToken = self._buildIoTHubSasToken(deviceId)
        url = 'https://%s/devices/%s/messages/events?api-version=%s' % (self.iotHost, deviceId, self.API_VERSION)
        r = requests.post(url, headers={'Authorization': sasToken}, data=message)
        return r.text, r.status_code

if __name__ == '__main__':
    while True:
        try:
            if(GPIO.input(3)==1):
                connectionString = 'Your connection string goes here'
                d2cMsgSender = D2CMsgSender(connectionString)
                deviceId = 'iotdevice1'
                message = '{"VoteCount":1,"TimeFlag":"' + strftime("%Y-%m-%dT%H:%M:%S.%sz", gmtime()) + '"}'
                print d2cMsgSender.sendD2CMsg(deviceId, message)
                time.sleep(.5)
        except IOError:
            GPIO.cleanup()
            print "Error"
