class CatFileException(Exception):
    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)


class WrongFileTypeError(CatFileException):
    def __init__(self, expected_type: str) -> None:
        super().__init__(f"Expected file of type {expected_type}")


class InvalidFileTypeError(CatFileException):
    def __init__(self, provided_type: str) -> None:
        super().__init__(f"{provided_type} is not a valid file type code")


class DuplicateFileTypeCodeError(CatFileException):
    def __init__(self, provided_class: object, provided_code: str) -> None:
        super().__init__(f"The code - {provided_code} - for the class - {provided_class} - is already in use.")


class NoFileTypeFoundError(CatFileException):
    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__("No file type was found for the provided input", *args, **kwargs)
