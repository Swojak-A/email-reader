class EmailReaderInvalidStatusException(Exception):
    def __init__(self, status):
        self.status = status
        self.message = f"Invalid status: {status}. IMAP status should be 'OK'."
        super().__init__(self.message)


class NoEmailsFoundException(Exception):
    def __init__(self):
        self.message = "No emails found."
        super().__init__(self.message)
