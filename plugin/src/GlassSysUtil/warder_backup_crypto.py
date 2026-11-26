"""Optional authenticated encryption for user-owned local backups."""
import base64
import binascii
import hashlib
import os

FORMAT='warder-private-v1'
AAD=b'Warder Evolution private backup v1'
MAX_PLAINTEXT=2*1024*1024
MAX_ENVELOPE=3*1024*1024


def available():
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        return callable(AESGCM) and callable(getattr(hashlib,'scrypt',None))
    except (ImportError,OSError,AttributeError):return False


def key(password,salt):
    if not isinstance(password,str) or not 12<=len(password)<=128 or not password.isprintable():
        raise ValueError('Private backup password requirements')
    if not available():raise ValueError('Private backup encryption unavailable')
    return hashlib.scrypt(password.encode('utf-8'),salt=salt,n=32768,r=8,p=1,dklen=32,maxmem=64*1024*1024)


def encode(raw):
    return base64.b64encode(raw).decode('ascii')


def decode(value,maximum):
    if not isinstance(value,str) or len(value)>4*((maximum+2)//3):raise ValueError('Invalid encrypted backup')
    try:raw=base64.b64decode(value,validate=True)
    except (ValueError,binascii.Error):raise ValueError('Invalid encrypted backup') from None
    if len(raw)>maximum:raise ValueError('Invalid encrypted backup')
    return raw


def seal(raw,password):
    if not isinstance(raw,bytes) or len(raw)>MAX_PLAINTEXT:raise ValueError('Private backup too large')
    if not available():raise ValueError('Private backup encryption unavailable')
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    salt,nonce=os.urandom(16),os.urandom(12)
    cipher=AESGCM(key(password,salt)).encrypt(nonce,raw,AAD)
    return {'format':FORMAT,'salt':encode(salt),'nonce':encode(nonce),'ciphertext':encode(cipher)}


def unseal(document,password):
    if not isinstance(document,dict) or set(document)!= {'format','salt','nonce','ciphertext'} or document['format']!=FORMAT:
        raise ValueError('Invalid encrypted backup')
    if not available():raise ValueError('Private backup encryption unavailable')
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.exceptions import InvalidTag
    salt=decode(document['salt'],16)
    nonce=decode(document['nonce'],12)
    cipher=decode(document['ciphertext'],MAX_PLAINTEXT+16)
    if len(salt)!=16 or len(nonce)!=12 or len(cipher)<16:raise ValueError('Invalid encrypted backup')
    try:return AESGCM(key(password,salt)).decrypt(nonce,cipher,AAD)
    except InvalidTag:raise ValueError('Incorrect password or damaged backup') from None
