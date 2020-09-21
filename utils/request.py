import logging
from urllib import parse


class Request:
    def __init__(self, unparsed_message: str):
        self.method = None
        self.url = None
        self.protocol = None
        self.is_valid = False

        lines = unparsed_message.splitlines()

        try:
            self.method, dirty_url, self.protocol = lines[0].split(' ')

            self.url = parse.unquote(dirty_url)
            if '?' in self.url:
                self.url = self.url[:self.url.find('?')]

            self.is_valid = True

        except Exception as e:
            logging.error(e)
            self.is_valid = False