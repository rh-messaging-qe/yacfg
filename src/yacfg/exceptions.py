class YacfgException(Exception):
    """Base exception for Yet Another Configuration Generator (YACFG)."""


class TemplateError(YacfgException):
    """Exception raised for template-related errors in YACFG."""


class ProfileError(YacfgException):
    """Exception raised for profile-related errors in YACFG."""


class GenerationError(YacfgException):
    """Exception raised for generation-related errors in YACFG."""


class ConfigurationError(YacfgException):
    """Exception raised for configuration-related errors in YACFG."""


class ParsingError(YacfgException):
    """Exception raised for parsing-related errors in YACFG."""


class AuthorizationError(YacfgException):
    """Exception raised for authorization-related errors in YACFG."""


# Custom exception with additional details
class InvalidInputError(YacfgException):
    """Exception raised for invalid input in YACFG.

    Attributes:
        input_value -- input value that caused the error
        message -- explanation of the error
    """

    def __init__(self, input_value: str, message: str = "Invalid input"):
        self.input_value: str = input_value
        self.message: str = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.message}: {self.input_value}"
