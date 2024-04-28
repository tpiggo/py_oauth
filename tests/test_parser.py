from unittest import TestCase
from oauth2_security.auth import pre_authorize_expression, And
from oauth2_security.errors import InvalidTypeError, InvalidNameError
from oauth2_security.nodes import Authority, AnyRole


class TestAuth(TestCase):
    def test_check_valid(self):
        expression_tree = pre_authorize_expression("has_authority('abc')")
        self.assertIsInstance(expression_tree, Authority)
        self.assertEqual(expression_tree.value, 'abc')

    def test_build_any_role(self):
        expression_tree = pre_authorize_expression("has_any_role('abc', 'def')")
        self.assertIsInstance(expression_tree, AnyRole)
        self.assertEqual(expression_tree.values, ('abc', 'def'))

    def test_build_and(self):
        expression_tree = pre_authorize_expression("has_any_role('abc', 'def') and has_authority('abc')")
        self.assertIsInstance(expression_tree, And)
        self.assertIsInstance(expression_tree.items[0], AnyRole)
        # We have already checked the type
        self.assertEqual(expression_tree.items[0].values, ('abc', 'def'))
        self.assertIsInstance(expression_tree.items[1], Authority)
        self.assertEqual(expression_tree.items[1].value, 'abc')

    def test_build_invalid(self):
        def throwable():
            pre_authorize_expression("import dataclass; has_any_role('abc', 'def')")
        self.assertRaises(InvalidTypeError, throwable)

    def test_build_invalid_name(self):
        def throwable():
            pre_authorize_expression("has_any_role_typo('abc', 'def')")
        self.assertRaises(InvalidNameError, throwable)