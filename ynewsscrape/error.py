class FetchHtmlError(Exception):
    def __init__(self, err_message=""):
        self.err_message = err_message

    def __str__(self) -> str:
        return f"Failed to fetch html. error={self.err_message}"


class HtmlParseError(Exception):
    def __str__(self) -> str:
        return "Failed to parse html. \
                The DOM structure of the page may have changed, please check."
