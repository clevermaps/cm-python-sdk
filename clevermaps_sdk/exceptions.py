class CleverMapsSdkException(Exception):
    """Base custom exception"""
    pass


class AccessTokenException(CleverMapsSdkException):
    """Raised in case of invalid access token"""
    pass


class ExportException(CleverMapsSdkException):
    """Raised in case of failed export"""
    pass