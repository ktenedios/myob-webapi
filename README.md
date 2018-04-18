# NPL Victoria 2018 Football Results API

This is a Python Flask application that gets results of the NPL Victoria 2018 football (soccer) competition.

The application is hosted in Heroku and can be accessed from <https://ktenedios-football-results-api.herokuapp.com/>.

The following RESTful endpoints that return JSON data are exposed:

* `/` - Root endpoint that lists the endpoints exposed by the application.
* `/season` - Get the full season results.
* `/round/<round_number>` - Get the results for a given round (e.g. `/round/2`)
* `/healthCheck` - Get the results of a system health check. In the context of this application, the health check verifies that it gets a HTTP 200 response from <http://websites.sportstg.com/comp_info.cgi?a=ROUND&round=-1&client=0-10178-0-478257-0&pool=1>.
* `/environmentDump` - Get a dump of the environment where the application is running from, including application information.

## CI/CD pipeline

A build job has been set up in [CircleCI](https://circleci.com/gh/ktenedios/myob-webapi) that is automatically triggered upon pushing commits to origin.

The build job will run a collection of unit tests that are located in the `tests` folder, and will also measure code coverage. The results of the unit tests and the code coverage analysis are published as artifacts to the build job.

Once the tests have succeeded, the application is then deployed automatically to Heroku.

The build steps are contained in the file `.circleci/config.yml`, and it relies on `.circleci/setup-heroku.sh` for deploying a successful build to Heroku.

## Setting up CircleCI and Heroku for automated deployments

The prerequisites for CircleCI deploying to Heroku are:

1. Generating an SSH key pair (private and public keys) using `ssh-keygen`.
2. Obtaining the fingerprint of the SSH key from step 1 using `ssh-keygen -lf path/to/key`, which will be inserted into the file `.circleci/config.yml`.
3. Registering the public SSH key under your Heroku account settings.
4. Obtaining the HTTPS URL (e.g. <https://git.heroku.com/ktenedios-football-results-api.git>), which will be inserted into the file `.circleci/setup-heroku.sh`.

Once the prerequisites have been satisfied, refer to the following link for configuring Heroku:
<https://circleci.com/docs/2.0/project-walkthrough/#deploying-to-heroku>