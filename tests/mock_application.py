from flask import Flask

class MockApplication(Flask):
    _run_invoked = False

    def __init__(self, application_name):
        self._application_name = application_name

    def run(self):
        self._run_invoked = True

    def get_run_invoked(self):
        return self._run_invoked