from praw.models import Comment, Submission
import mock
import pytest

from ... import IntegrationTest


class TestSubmission(IntegrationTest):
    def test_comments(self):
        with self.recorder.use_cassette(
                'TestSubmission.test_comments'):
            submission = Submission(self.reddit, '2gmzqe')
            assert len(submission.comments) == 1
            assert isinstance(submission.comments[0], Comment)
            assert isinstance(submission.comments[0].replies[0], Comment)

    @mock.patch('time.sleep', return_value=None)
    def test_delete(self, _):
        self.reddit.read_only = False
        with self.recorder.use_cassette(
                'TestSubmission.test_delete'):
            submission = Submission(self.reddit, '4b1tfm')
            submission.delete()
            assert submission.author is None
            assert submission.selftext == '[deleted]'

    @mock.patch('time.sleep', return_value=None)
    def test_edit(self, _):
        self.reddit.read_only = False
        with self.recorder.use_cassette(
                'TestSubmission.test_edit'):
            submission = Submission(self.reddit, '4b1tfm')
            submission.edit('New text')
            assert submission.selftext == 'New text'

    def test_duplicates(self):
        with self.recorder.use_cassette(
                'TestSubmission.test_duplicates'):
            submission = Submission(self.reddit, 'avj2v')
            assert len(list(submission.duplicates())) > 0

    def test_invalid_attribute(self):
        with self.recorder.use_cassette(
                'TestSubmission.test_invalid_attribute'):
            submission = Submission(self.reddit, '2gmzqe')
            with pytest.raises(AttributeError) as excinfo:
                submission.invalid_attribute
        assert excinfo.value.args[0] == ("'Submission' object has no attribute"
                                         " 'invalid_attribute'")

    def test_reply(self):
        self.reddit.read_only = False
        with self.recorder.use_cassette(
                'TestSubmission.test_reply'):
            submission = Submission(self.reddit, '4b1tfm')
            comment = submission.reply('Test reply')
            assert comment.author == pytest.placeholders.username
            assert comment.body == 'Test reply'
            assert comment.parent_id == submission.fullname
