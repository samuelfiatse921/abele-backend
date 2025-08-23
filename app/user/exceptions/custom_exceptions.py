from fastapi import HTTPException


class UnexpectedFailure(HTTPException):
    """Raised when serve fails to handle request."""
    pass


class ClientRequestFailure(HTTPException):
    """Raised when client sends invalid request."""
    pass


class DatabaseException(Exception):
    """Raised when there's a database error"""
    pass


class NoPaymentRecordFound(Exception):
    """Raised when there's no record found"""
    pass


class NoRecordToUpdate(Exception):
    """Raised when there's no record found"""
    pass

