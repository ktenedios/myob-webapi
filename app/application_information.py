import subprocess

class ApplicationInformation():
    def __init__(self):
        self._git_revision_short_hash = \
            self._get_git_property(['git', 'rev-parse', '--short', 'HEAD'])

        tags = self._get_git_property(['git', 'tag', '--list', '--contains', self._git_revision_short_hash])
        self._git_tags = tags.split('\n')

        authors = self._get_git_property(['git', 'log', '--format="%an <%ae>"', self._git_revision_short_hash])
        self._git_commit_author = authors.split('\n')[0].replace('"', '')

    def _get_git_property(self, git_params):
        output = subprocess.check_output(git_params)
        assert output is not None
        return output.strip().decode('utf-8')

    def get_information(self):
        return {
            'app': {
                'name': 'NPL Victoria 2018 Football Results API',
                'mostRecentCommit': self._git_revision_short_hash,
                'commitAuthor': self._git_commit_author,
                'tags': self._git_tags
            }
        }
