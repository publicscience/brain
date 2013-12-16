import unittest
from unittest.mock import patch

class RequiresMocks(unittest.TestCase):
    def create_patch(self, name, **kwargs):
        """
        Helper for patching/mocking methods.

        Args:
            | name (str)       -- the 'module.package.method' to mock.
        """
        patcher = patch(name, autospec=True, **kwargs)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing
