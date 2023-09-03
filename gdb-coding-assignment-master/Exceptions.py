"""
Custom informative exceptions
"""


class ExtractTokenException(Exception):
    def __init_(self):
        self.message = "Access token not found in the API response"
        super().__init__(self.message)


class HttpResponseException(Exception):
    def __init_(self, status_code, text):
        self.message = f"Bad Http response : Error code {status_code}\n Description: {text}"
        super().__init__(self.message)


class InvalidCategoryException(Exception):
    def __init_(self, category):
        self.category = category
        self.message = f"Category {self.category} doesn't exist"
        super().__init__(self.message)
