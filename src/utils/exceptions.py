from fastapi import status

class ApiException(Exception):
    """Base class for API exceptions, 400 by default"""
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code

class ValidationError(ApiException):
    """Error 400: Invalid data provided by user"""
    def __init__(self, message: str):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST)
        
class UnauthorizedError(ApiException):
    """Error 401: Unauthorized"""
    def __init__(self, message: str):
        super().__init__(message=message, status_code=status.HTTP_401_UNAUTHORIZED)
        
class ForbiddenError(ApiException):
    """Error 403: Forbidden"""
    def __init__(self, message: str):
        super().__init__(message=message, status_code=status.HTTP_403_FORBIDDEN)
        
class NotFoundError(ApiException):
    """Error 404: Entity not found"""
    def __init__(self, message: str):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)
