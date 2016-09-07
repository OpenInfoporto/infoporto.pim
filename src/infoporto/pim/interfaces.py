# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from five import grok
from plone.dexterity.content import Container

from infoporto.pim import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.supermodel import model
from plone.app.textfield import RichText
import datetime

from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from Products.CMFCore.utils import getToolByName
from zope.interface import directlyProvides

from z3c.relationfield.schema import RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.dexterity.browser.view import DefaultView


def possibleRecipients(context):
    acl_users = getToolByName(context, 'acl_users')
    groups = acl_users.getGroups()
    terms = []

    for g in groups:
        gid = g.getProperty('id')
        gname = g.getProperty('name')
        terms.append(SimpleVocabulary.createTerm(gid, str(gid), gname))

    return SimpleVocabulary(terms)

directlyProvides(possibleRecipients, IContextSourceBinder)

def getCurrentUser():
    from plone import api
    user = api.user.get_current().getUserName()
    return unicode(user)


class IInfoportoPimLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IMessage(model.Schema):

    subject = schema.TextLine(
        title=_(u"Subject"),
        required=True,
    )

    message_from = schema.TextLine(
        title=_(u"From"),
        required=True,
        defaultFactory=getCurrentUser,
    )


    message_to = schema.Choice(
        title=_(u"To"),
        source=possibleRecipients,
        required=True,
    )


    body = RichText(
        title=_(u"Body"),
        required=False,
    )

    unread = schema.Bool(
        title=_(u"Unread"),
        default=True
    )

    creation_date = schema.Datetime(
        title=_(u"Created at"),
        default=datetime.datetime.now()
    )


boxtypes = SimpleVocabulary(
    [SimpleTerm(value=u'messagesbox', title=_(u'Messages Box')),
     SimpleTerm(value=u'readingnotificationsbox', title=_(u'Reading notifications Box')),]
)


class IMailbox(model.Schema):

    name = schema.TextLine(
        title=_(u"Name"),
        required=True,
    )

    boxtype = schema.Choice(
        title=_(u"Type"),
        required=True,
        vocabulary=boxtypes,
    )


class Mailbox(Container):
    grok.implements(IMailbox)


class IReadingConfirmation(model.Schema):
    
    user = schema.TextLine(
        title=_("Utente"),
        required=True
    )

    message = RelationChoice(
        title=_(u"Messaggio"),
        source=ObjPathSourceBinder(object_provides=IMessage.__identifier__),
        required=True,
    )

