from hashlib import sha1
import hmac
import binascii
import secrets

def getUrl(request):
    devId = secrets.DEVID
    key = secrets.DEVKEY
    request = request + ('&' if ('?' in request) else '?')
    raw = request + 'devid={0}'.format(devId)
    hashed = hmac.new(key, raw.encode(), sha1)
    signature = hashed.hexdigest()
    return 'http://tst.timetableapi.ptv.vic.gov.au' + raw + '&signature={0}'.format(signature)

print(getUrl('/v2/healthcheck'))