import datetime
import hashlib
import logging
import traceback

from config import smtpConfig
from data.dataVault import DataVault
from util.queryCollection import QueryCollection
from util.twoFAUtil import TwoFactor
from data import dumps as d

logger = logging.getLogger()

class Validation:
    # 3 components: check names for numbers, check email ID for @ and .com
    # Check contact number for alpha-special
    # check password for special and nums, need both + length > 8 and store hash
    # General purpose input validation
    # TODO: CHANGE function to have default values for
    def inputValidation(self, formlabel, password=None, first=None, last=None, email=None, phone=None, retype_pass=None, dob=None):
        passbool, hash = self.passValidation(Validation, password, retype_pass, formlabel)
        namebool = self.nameValidation(Validation, first, last, formlabel)
        # check name
        emailbool = self.emailValidation(Validation, email, formlabel)
        # check contact num - all nums and length = 10
        phonebool = self.phoneValidation(Validation, phone, formlabel)
        # validate dob
        dobbool = self.dobValidation(Validation, dob, formlabel)

        if password :
            return phonebool and emailbool and namebool and passbool and dobbool, hash
        else:
            return phonebool and emailbool and namebool and passbool and dobbool, None


    def passValidation(self, password, retype_pass, formlabel):
        passbool = False
        if password:
            hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
            if password == retype_pass:
                if any(s in d.specials for s in password) and any(s.isalnum() for s in password):
                    passbool = True
                else:
                    formlabel['text'] = "Passwords must be alphanumeric and contain special chatracters"
            else:
                formlabel['text'] = "Passwords do not match"
        else:
            passbool = True

        return passbool, hash

    def nameValidation(self, first, last, formlabel):
        namebool = False
        if first and last:
            if first.isalpha() and last.isalpha():
                namebool = True
            else:
                formlabel['text'] = "Names must only contain alphabets"
        else:
            namebool = True

        return namebool

    def emailValidation(self, email, formlabel):
        # check email, must contain @ and .com, and length > 5
        emailbool = False
        if email:
            if any(s == "@" for s in email) and any(ext in email for ext in smtpConfig.extensions) and len(email) >= 7:
                if QueryCollection.checkEmailExists(QueryCollection, email, "Staff"):
                    formlabel['text'] = "Email already in use"
                else:
                    emailbool = True
            else:
                formlabel['text'] = "Not a valid email"
        else:
            emailbool = True

        return emailbool

    def phoneValidation(self, phone, formlabel):
        phonebool = False
        if phone:
            if phone.isnumeric():
                if len(phone) == 10:
                    phonebool = True
                else:
                    formlabel['text'] = "Invalid phone number length"
            else:
                formlabel['text'] = "Only numbers allowed in Contact"
        else:
            phonebool = True

        return phonebool

    def dobValidation(self, dob, formlabel):
        # credit : https://stackoverflow.com/questions/16870663/how-do-i-validate-a-date-string-format-in-python
        dobbool = False
        if dob:
            try:
                formatted_dob = datetime.datetime.strptime(dob, "%Y-%m-%d")
                if dob == formatted_dob.strftime('%Y-%m-%d'):
                    dobbool = True
                else:
                    formlabel['text'] = "Date must be in YYYY-MM-DD form"
            except ValueError as e:
                formlabel['text'] = "Date must be in YYYY-MM-DD form"
                logger.error("Error in dob input validation: " + str(e) + traceback.format_exc())
        else:
            dobbool = True

        return dobbool
