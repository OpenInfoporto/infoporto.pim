# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from infoporto.pim.testing import INFOPORTO_PIM_INTEGRATION_TESTING  # noqa
from plone import api

import unittest2 as unittest


class TestSetup(unittest.TestCase):
    """Test that infoporto.pim is properly installed."""

    layer = INFOPORTO_PIM_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if infoporto.pim is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('infoporto.pim'))

    def test_browserlayer(self):
        """Test that IInfoportoPimLayer is registered."""
        from infoporto.pim.interfaces import IInfoportoPimLayer
        from plone.browserlayer import utils
        self.assertIn(IInfoportoPimLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = INFOPORTO_PIM_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['infoporto.pim'])

    def test_product_uninstalled(self):
        """Test if infoporto.pim is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled('infoporto.pim'))
