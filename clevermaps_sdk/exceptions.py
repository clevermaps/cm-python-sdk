class CleverMapsException(Exception):
    """Base custom exception"""
    pass


class AccessTokenException(CleverMapsException):
    """Raised in case of invalid access token"""
    pass


class ExportException(CleverMapsException):
    """Raised in case of failed export"""
    pass