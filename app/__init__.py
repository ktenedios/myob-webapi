from app.app import get_new_server_instance

# Function that is only called by ../run.py and by Heroku for running a server instance.
# This function ensures that dependencies stored in the inversion of control container
# by the unit tests are not affected.
def start_server(running_unit_tests=True):
    if not running_unit_tests:
        server = get_new_server_instance()
        server.start()
