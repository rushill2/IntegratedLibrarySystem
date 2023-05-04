import sys
import traceback
from random import randint
from config import twoFAConfig
from pythontextnow import Client
from pythontextnow import ConversationService
import logging
import os
logger = logging.getLogger()
USERNAME = twoFAConfig.user
SID_COOKIE = twoFAConfig.cookie


class TwoFactor:
    OTP = None
    Phone = None
    id = None
    def send_code(self, caller, controller):
        try:
            self.Phone = "+1" + self.Phone
            Client.set_client_config(username=USERNAME, sid_cookie=SID_COOKIE)
            conversation_service = ConversationService(conversation_phone_numbers=[self.Phone])
            self.OTP = ''.join(["{}".format(randint(0, 9)) for num in range(0, 5)])
            conversation_service.send_message(message=twoFAConfig.message.replace('{_otp}', self.OTP))
        except Exception as e:
            logger.error("Error in 2FA OTP: " + str(e) + traceback.format_exc())
            caller.serviceOutage(controller)


    def authenticate(self, Entry):
        if Entry == self.OTP:
            return True
        else:
            return False
