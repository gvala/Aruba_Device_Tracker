cat > aruba_device_tracker/legacy_ssl.py << 'EOF'
"""Legacy SSL renegotiation support for older Aruba IAP firmware."""
import ssl
import requests
import urllib3


class CustomHttpAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context)


def get_legacy_session():
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.check_hostname = False
    ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
    ctx.set_ciphers('DEFAULT@SECLEVEL=0')
    session = requests.session()
    session.mount('https://', CustomHttpAdapter(ctx))
    return session
EOF
