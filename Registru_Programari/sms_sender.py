from twilio.rest import Client
import constants_programari
from sinch import Client



class SendSmsAppointment:

    def modify_telephone_number(self, tel_number_original):
        tel_number_modified = "+4"+tel_number_original
        return tel_number_modified

    def add_phone_to_list(self, telephone_number, first_name, last_name):
        account_sid = constants_programari.ACCOUNT_SID
        account_api = constants_programari.ACCOUNT_API
        telephone_number_modified = self.modify_telephone_number(telephone_number)
        if telephone_number_modified !="+40748313438":
            client = Client(account_sid, account_api)
            #make validation
            client.validation_requests .create(
                friendly_name=first_name+" "+last_name,
                phone_number=telephone_number_modified
            )

    def send_sms(self, telephone_number, appointment_day, hour):
        account_sid = constants_programari.ACCOUNT_SID
        account_api = constants_programari.ACCOUNT_API
        telephone_number_modified = self.modify_telephone_number(telephone_number)
        # define the client
        client = Client(account_sid, account_api)
        message_text = "Buna ziua! Acest mesaj confirma faptul ca ati fost programat pentru consultatie pe data de {}, in intervalul orar {}. Va dorim o zi buna!".format(
            appointment_day, hour)
        # create the message
        message = client.messages.create(
            body=message_text,
            from_=constants_programari.PHONE_NUMBER,
            to=telephone_number_modified
        )

    def send_sms2(self, telephone_number,appointment_day,hour):
        sinch_client = Client(
            key_id=constants_programari.KEY_ID,
            key_secret=constants_programari.KEY_SECRET,
            project_id=constants_programari.PROJECT_ID
        )

        message_text = "Buna ziua! Acest mesaj confirma faptul ca ati fost programat pentru consultatie pe data de {}, in intervalul orar {}. Va dorim o zi buna!".format(
            appointment_day, hour)
        telephone_number_modified = self.modify_telephone_number(telephone_number)
        telephone_number_modified2 = telephone_number_modified[1:]

        sinch_client.sms.batches.send(
            body=message_text,
            to=[telephone_number_modified2],
            from_=constants_programari.PHONE_NUMBER_SINCH,
            delivery_report="none"
        )



