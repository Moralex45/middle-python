class DataAlreadyExistsError(Exception):
    """Raises when trying to create additional data on unique existent"""


class DataDoesNotExistError(Exception):
    """Raises when trying to remove data that does not exist"""
