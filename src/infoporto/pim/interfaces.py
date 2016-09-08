# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from five import grok
from plone.dexterity.content import Container

from infoporto.pim import _
from zope import schema

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.supermodel import model
from plone.app.textfield import RichText
import datetime

from zope.schema.interfaces import IContextSourceBinder

from Products.CMFCore.utils import getToolByName
from zope.interface import directlyProvides

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone import api


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


def deliverMessage(message, event):

    group_name = message.message_to
    api.group.grant_roles(obj=message, groupname=group_name, roles=['Reader'])
    message.reindexObject()


boxtypes = SimpleVocabulary(
    [SimpleTerm(value=u'messagesbox', title=_(u'Messages Box')),
     SimpleTerm(value=u'readingnotificationsbox', title=_(u'Reading notifications Box')),]
)


class IMailbox(model.Schema):

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

    message= schema.TextLine(
        title=_("Messaggio"),
        required=True
    )

