from app.app import get_new_application_instance

# Function that is only called by ../run.py and by Heroku for running a server instance.
# This function ensures that dependencies stored in the inversion of control container
# by the unit tests (the mock objects) are not affected.
def get_application():
    return get_new_application_instance()
