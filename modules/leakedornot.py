import hashlib
import requests

class PwnedPassphraseException(Exception):
    pass

def check_pwned(passphrase):
    #Check passphrase against the haveibeenpwned.com API.
    #If the passphrase is found in the API, raise an exception.
    #Otherwise, return False.
    
    h = hashlib.sha1(passphrase.encode()).hexdigest().upper()
    prefix, suffix = h[:5], h[5:]
    url = f'https://api.pwnedpasswords.com/range/{prefix}'
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f'Error fetching {url}: {response.status_code}')
    for line in response.text.splitlines():
        suffix_, count = line.split(':')
        if suffix_ == suffix:
            raise PwnedPassphraseException(count)
    return False

