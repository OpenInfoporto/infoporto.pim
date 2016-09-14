import logging

from Products.Five.browser import BrowserView
from plone import api


logger = logging.getLogger('infoporto.pim')


class MailboxView(BrowserView):

    def getMyMessages(self):
        results = list()

        current_user = api.user.get_current().getUserName()

        logger.info('getMyMessage called for %s' % current_user)

        messages = api.content.find(portal_type="Message")

        for msg in messages:
            msg = msg.getObject()

            results.append({
                'message_from': msg.message_from,
                'subject': msg.subject,
                'body': msg.body,
                'created_at': msg.creation_date,
                'is_unread': True, #TODO: make reading confirm list
                'uuid': msg.UID,
            })

        return results

    def getConfirmations(self):
        results = list()

        current_user = api.user.get_current().getUserName()
        
        logger.info('getConfirmations called for %s' % current_user)

        confirmations = api.content.find(portal_type="ReadingConfirmation")

        for confirmation in confirmations:
            confirmation = confirmation.getObject()
            messages = api.content.find(UID=confirmation.message)
            if messages:
                message = messages[0].getObject()

                results.append({
                    'user': confirmation.user,
                    'message': "%s from %s" % (message.subject, message.message_from),
                    'created_at': message.created,
                    'uuid': message.UID,
                })

        return results


class MarkAsRead(BrowserView):

    def __call__(self):
        logger.info('Marking message %s as read.' % self.request.uuid)

        container = api.content.get(path='/conferme-di-lettura/')
        username = api.user.get_current().getUserName()

        obj = api.content.create(
            type='ReadingConfirmation',
            title='%s-%s' % (username, self.request.uuid),
            user=username,
            message=self.request.uuid,
            container=container)

        api.content.transition(obj=obj, transition='publish')

        return "Done."


class ReadingConfirmationView(BrowserView):

    pass


class InboxView(BrowserView):

    def getMyMessages(self):
        results = list()

        current_user = api.user.get_current().getUserName()

        logger.info('getMyMessage called for %s' % current_user)

        messages = api.content.find(portal_type="Message")

        for msg in messages:
            msg = msg.getObject()

            results.append({
                'message_from': msg.message_from,
                'subject': msg.subject,
                'body': msg.body,
                'created_at': msg.creation_date,
                'is_unread': True, #TODO: make reading confirm list
                'uuid': msg.UID,
            })

        return results


class CountUnread(BrowserView):
    def __call__(self):   
        current_user = api.user.get_current().getUserName()

        logger.info('countUnread called for %s' % current_user)

        return 1
