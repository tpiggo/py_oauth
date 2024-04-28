from unittest import TestCase

from oauth2_security.nodes import Authority, Role, And, Or
from oauth2_security.token_info import TokenInfo


class TestNodes(TestCase):
    def test_authority(self):
        self.assertTrue(Authority("abc").evaluate(TokenInfo(["abc"], [])))

    def test_wrong_authority(self):
        self.assertFalse(Authority("abc").evaluate(TokenInfo(["def"], [])))

    def test_no_authority(self):
        self.assertFalse(Authority("abc").evaluate(TokenInfo([], ["something"])))

    def test_role(self):
        self.assertTrue(Role("abc").evaluate(TokenInfo([], ["abc"])))

    def test_no_role(self):
        self.assertFalse(Authority("abc").evaluate(TokenInfo(["something"], [])))

    def test_wrong_role(self):
        self.assertFalse(Authority("abc").evaluate(TokenInfo(["def"], [])))

    def test_and(self):
        self.assertTrue(And([Authority("abc"), Authority("def")]).evaluate(TokenInfo(["abc", "def"], [])))

    def test_failed_and(self):
        self.assertFalse(And([Authority("abc"), Authority("def")]).evaluate(TokenInfo(["abc", "dcf"], [])))

    def test_or(self):
        self.assertTrue(Or([Authority("abc"), Authority("def")]).evaluate(TokenInfo(["abc", "dcf"], [])))

    def test_failed_or(self):
        self.assertFalse(Or([Authority("abc"), Authority("def")]).evaluate(TokenInfo(["Dabc", "dcf"], [])))
