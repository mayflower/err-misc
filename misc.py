import random
import re

from errbot import BotPlugin, re_botcmd, webhook


class Misc(BotPlugin):
    @re_botcmd(pattern=r'^(ser(vu)?s|hi(ya)?|hallo|hello|good( [d\'])?ay(e)?|aho(i|j)) ', prefixed=False, flags=re.IGNORECASE)
    def hello(self, msg, args):
        '''Hello'''
        hellos = [
            "Well hello there, {}",
            "Hey {}, Hello!",
            "Marnin', {}",
            "Good day, {}",
            "Good 'aye!, {}",
            "Servus {}",
            "Ahoi {}"
        ]

        if not self.bot_identifier.nick == msg.frm.nick:
            return random.choice(hellos).format(msg.frm.nick)

    @re_botcmd(pattern=r'(^(good )?m(a|o)(rn)?ing?) ', prefixed=False, flags=re.IGNORECASE)
    def morning(self, msg, args):
        '''Good morning'''
        mornings = [
            "Good morning, {}",
            "Good morning to you too, {}",
            "Good day, {}",
            "Good 'aye!, {}",
            "Moin {}"
        ]

        if not self.bot_identifier.nick == msg.frm.nick:
            return random.choice(mornings).format(msg.frm.nick)

    @re_botcmd(pattern=r'ticket.*\?', prefixed=False, flags=re.IGNORECASE)
    def ticket(self, msg, args):
        '''Should I open a ticket?'''
        if hasattr(msg.frm, 'room') and (str(msg.frm.room) == 'administrator@conference.mayflower.de' or \
            str(msg.frm.room) == '#administrator'):

            return (
                "Hi, thanks for asking for support, we are definitely happy to help.\nBut...\nOne thing...\n"
                "Could you open an issue for us by either mailing administrator@mayflower.de or visiting https://jira.mayflower.de/secure/CreateIssue!default.jspa?pid=10000\n"
                "Thank you very much for your support and we'll get back to you very soon."
            )

    @re_botcmd(pattern=r'announce "(.*)"')
    def announce(self, msg, match):
        for room in self.rooms():
            self.send(room, match.group(1))

    @re_botcmd(pattern=r'announce downtime for "(.*)" starting (.*)')
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
            self.send(room, message)

    @re_botcmd(pattern=r'announce downtime complete for "(.*)"')
    def announce_up(self, msg, match):
        service = match.group(1)
        message = "Maintenance for the '{}' service is complete.".format(service)

        for room in self.rooms():
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
