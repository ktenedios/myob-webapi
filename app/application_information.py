from github import Github, GithubException

from app.inversion_of_control import IsInstanceOf, RequiredFeature


class ApplicationInformation():
    _github_token = RequiredFeature('GithubToken', IsInstanceOf(str))
    _repo_name = RequiredFeature('RepoName', IsInstanceOf(str))

    def __init__(self):
        if (self._github_token == ''):
            self._git_revision = None
            self._git_tag = None
        else:
            g = Github(self._github_token)

            for repo in g.get_user().get_repos():
                if repo.name == self._repo_name:
                    most_recent_commit = repo.get_commits()[0]
                    self._git_revision = most_recent_commit.sha

                    try:
                        self._git_tag = repo.get_git_tag(self._git_revision)
                    except GithubException:
                        self._git_tag = None

                    break

    def get_information(self):
        return {
            'app': {
                'name': 'NPL Victoria 2018 Football Results API',
                'mostRecentCommit': self._git_revision,
                'tag': self._git_tag
            }
        }
