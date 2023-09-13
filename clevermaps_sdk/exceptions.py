class CleverMapsSdkException(Exception):
    """Base custom exception"""
    pass


class AccessTokenException(CleverMapsSdkException):
    """Raised in case of invalid access token"""
    pass


class ExportException(CleverMapsSdkException):
    """Raised in case of failed export"""
    pass

class InvalidDwhQueryException(CleverMapsSdkException):
    """Raised in case of invalid Datawarehouse Query"""
    pass

class InvalidProjectException(CleverMapsSdkException):
    """Raised in case of invalid project"""
    pass

class DataUploadException(CleverMapsSdkException):
    """Raised in case of failed data upload"""
    pass

class DataDumpException(CleverMapsSdkException):
    """Raised in case of failed data dump"""
    pass