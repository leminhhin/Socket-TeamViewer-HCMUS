import netifaces

def get_address():
    mac = netifaces.ifaddresses('en0')[netifaces.AF_LINK]
    addrs = mac.pop()['addrs']
    return addrs