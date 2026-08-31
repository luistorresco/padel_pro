"""Domain layer - Pure business logic, no framework imports."""


class DomainException(Exception):
    """Base domain exception."""
    pass


class EntityNotFound(DomainException):
    """Entity not found."""
    pass


class ValidationError(DomainException):
    """Validation error."""
    pass
