
class XenApiException(Exception):
    def __init__(self, error_key, message=None, **data):
        self.error_key = error_key
        self.message = message or "Error on Request"
        self.append_data = data

    def __str__(self):
        return f'[XenForo][{self.error_key}][{self.message}] {self.message}'


class XenApiKeyIncorrect(XenApiException):
    pass


class XenPageNotFound(XenApiException):
    pass


class XenThreadNotExists(Exception):
    def __init__(self, thread_id, **data):
        self.thread_id = thread_id
        self.append_data = data

    def __str__(self):
        return f"[XenForo] Thread with id '{self.thread_id}' not exists"


def xen_raise_error(error_key, message=None, **data):
    match error_key:
        case 'api_key_not_found':
            raise XenApiKeyIncorrect(error_key, message=message, **data)
        case 'requested_page_not_found':
            raise XenApiKeyIncorrect(error_key, message=message, **data)
        case _:
            raise XenApiException(error_key, message=message, **data)
