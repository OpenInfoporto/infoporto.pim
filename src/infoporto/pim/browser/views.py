import logging

from Products.Five.browser import BrowserView
from plone import api
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


logger = logging.getLogger('infoporto.pim')

class MailboxView(BrowserView):

    def getMyMessages(self):
        results = []
    
        current_user = api.user.get_current().getUserName()

        logger.info('getMyMessage called for %s' % current_user)
    
        portal_catalog = api.portal.get_tool('portal_catalog')

        brains = portal_catalog(portal_type="Message")

        #TODO: filter for valid recipients
        
        for brain in brains:
            msg = brain.getObject()

            results.append({
                'message_from': msg.message_from,
                'subject': msg.subject,
                'body': msg.body,
                'url': brain.getURL(),
                'created_at': msg.creation_date,
                'is_unread': True, #TODO: make reading confirm list
                'uuid': brain.UID,
                })

        return results


class MarkAsRead(BrowserView):

    def __call__(self):
        logger.info('Marking message %s as read.' % self.request.uuid)
        
        return "Done."


class ReadingConfirmationView(BrowserView):

    def getConfirmations(self):
        results = []

        current_user = api.user.get_current().getUserName()

        logger.info('getConfirmations called for %s' % current_user)

        portal_catalog = api.portal.get_tool('portal_catalog')

        brains = portal_catalog(portal_type="ReadingConfirmation")

        for brain in brains:
            confirmation = brain.getObject()
            message = confirmation.message #TODO: get details

            results.append({
                'user': confirmation.user,
                'message': message,
                'created_at': brain.created,
                'uuid': brain.UID,
                })

        return results

