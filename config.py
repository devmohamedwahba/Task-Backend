# SQLALCHEMY_DATABASE_URI = "postgres://postgres:body12345@127.0.0.1/smart"
# SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost/smart"
SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"

SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = [
    "access",
    "refresh",
]
