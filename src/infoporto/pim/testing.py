# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import infoporto.pim


class InfoportoPimLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=infoporto.pim)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'infoporto.pim:default')


INFOPORTO_PIM_FIXTURE = InfoportoPimLayer()


INFOPORTO_PIM_INTEGRATION_TESTING = IntegrationTesting(
    bases=(INFOPORTO_PIM_FIXTURE,),
    name='InfoportoPimLayer:IntegrationTesting'
)


INFOPORTO_PIM_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(INFOPORTO_PIM_FIXTURE,),
    name='InfoportoPimLayer:FunctionalTesting'
)


INFOPORTO_PIM_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        INFOPORTO_PIM_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='InfoportoPimLayer:AcceptanceTesting'
)
