from flask_talisman import Talisman

security = Talisman(
    content_security_policy={
        'default-src': "'self'",
        'img-src': "'self' data: https:",
        'script-src': "'self'",
        'style-src': "'self' 'unsafe-inline'",
    },
    force_https=True,
    strict_transport_security=True,
    session_cookie_secure=True,
    session_cookie_http_only=True
)