import random
import re

from errbot import BotPlugin, re_botcmd, webhook


class Misc(BotPlugin):
    @re_botcmd(pattern=r'ANNOUNCE "(.*)"', prefixed=False)
    def announce(self, msg, match):
        for room in self.rooms():
            if self.to_be_announced(room):
                self.send(room, match.group(1))

    @re_botcmd(pattern=r'ANNOUNCE downtime for "(.*)" starting (.*)', prefixed=False)
    def announce_downtime(self, msg, match):
        user = msg.frm.nick
        room = msg.frm.room if hasattr(msg.frm, 'room') else None
        service = match.group(1)
        start_time = match.group(2)

        message = (
            "The '{}' service will be going down for maintenance starting {}.\n"
            "If you have questions about this maintenance, please talk to {} in the {} room. Thank you for your patience."
        ).format(service, start_time, user, room)

        for room in self.rooms():
            if self.to_be_announced(room):
                self.send(room, message)

    @re_botcmd(pattern=r'ANNOUNCE downtime complete for "(.*)"', prefixed=False)
    def announce_up(self, msg, match):
        service = match.group(1)
        message = "Maintenance for the '{}' service is complete.".format(service)

        for room in self.rooms():
            if self.to_be_announced(room):
                self.send(room, message)

    def callback_message(self, message):
        self.log.debug(message.body == '{}?'.format(self._bot.bot_config.CHATROOM_FN))
        self.log.debug(message.body)
        self.log.debug('{}?'.format(self._bot.bot_config.CHATROOM_FN))
        if message.body == '{}?'.format(self._bot.bot_config.CHATROOM_FN):
            phrases = [
                "Yes, master?",
                "At your service",
                "Unleash my strength",
                "I'm here. As always",
                "By your command",
                "Ready to work!",
                "Yes, milord?",
                "More work?",
                "Ready for action",
                "Orders?",
                "What do you need?",
                "Say the word",
                "Aye, my lord",
                "Locked and loaded",
                "Aye, sir?",
                "I await your command",
                "Your honor?",
                "Command me!",
                "At once",
                "What ails you?",
                "Yes, my firend?",
                "Is my aid required?",
                "Do you require my aid?",
                "My powers are ready",
                "It's hammer time!",
                "I'm your robot",
                "I'm on the job",
                "You're interrupting my calculations!",
                "What is your wish?",
                "How may I serve?",
                "At your call",
                "You require my assistance?",
                "What is it now?",
                "Hmm?",
                "I'm coming through!",
                "I'm here, mortal",
                "I'm ready and waiting",
                "Ah, at last",
                "I'm here",
                "Something need doing?",
            ]

            self.send(message.frm.room if hasattr(message.frm, 'room') else message.frm, random.choice(phrases))


    @webhook('/', methods=('GET',), raw=True)
    def receive(self, request):
        pass

    def to_be_announced(self, room):
        "Returns true if ANNOUNCEMENT_ROOMS isn't specified or true for the specified rooms"
        return str(room) in getattr(self._bot.bot_config, 'ANNOUNCEMENT_ROOMS', [])
