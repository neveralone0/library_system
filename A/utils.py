from kavenegar import *
from django.contrib.auth.mixins import UserPassesTestMixin


def send_otp_code(phone_number, code):
    # try:
    #     api = KavenegarAPI('645854525561445A2F535944746675494E7A5243722B6730574279524A6C597952712B65333233435A366B3D')
    #     params = {'sender': '',
    #               'receptor': phone_number,
    #               'message': f'کد {code} ',
    #               }
    #     response = api.sms_send(params)
    #     print(response)
    # except APIException as e:
    #     print(e)
    # except HTTPException as e:
    #     print(e)
    pass


class IsAdminUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin
