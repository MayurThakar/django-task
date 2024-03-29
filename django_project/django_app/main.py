from .models import Users
import datetime
import re


def duplicate_email(email):
    fetched_email = Users.objects.filter(email=email).values_list()

    if fetched_email:
        return False
    return True


def encrypt_password(username, password):
    encr_paswd = ''
    un_paswd = username + password

    for each_char in un_paswd:
        if each_char.isdigit():
            encr_paswd = "".join([encr_paswd, chr(int(each_char)+70)])
        else:
            encr_paswd = "".join([encr_paswd, str(ord(each_char))])

    return encr_paswd


class Main:

    def __init__(self, request):
        self.request = request

    def is_exist(self):
        if not self.request.POST['email'] or not self.request.POST['password']:
            return 'Please fill up all details'

        elif len(self.request.POST['password']) < 8:
            return 'Password must contain 8 characters'

        else:
            user = Users.objects.filter(
                email=self.request.POST['email']).values_list('username', 'password')

            if user:
                encr_paswd = encrypt_password(
                    user[0][0], self.request.POST['password'])
                if encr_paswd != user[0][1]:
                    return 'Incorrect password'

            else:
                return 'User does not exist'

        return True

    def is_validate(self):
        if not self.request.POST['username'] or not self.request.POST['email'] or not self.request.POST['new-password'] or not self.request.POST['re-paswd'] or not self.request.POST['address']:
            return 'Please fill up all details'

        else:
            if len(self.request.POST['username']) < 5:
                return 'Username must contain 5 or more characters'
            elif not duplicate_email(self.request.POST['email']):
                return 'Sorry, Email is already taken!'
            elif len(self.request.POST['new-password']) < 8:
                return 'Password must contain 8 characters and one digit, upper, lower character'
            elif len(self.request.POST['new-password']) >= 8:
                re_pattern = '[A-Z]+[a-z]+[0-9]'
                if not re.search(re_pattern, self.request.POST['new-password']):
                    return 'Password must contain one digit, upper, lower character'
            elif self.request.POST['new-password'] != self.request.POST['re-paswd']:
                return 'Repeat password did not match'
            elif len(self.request.POST['address']) < 5:
                return 'Address must contain 5 or more characters'

        return True

    def add_user(self):
        reference = Users()
        timestamp = datetime.datetime.now()
        reference.userid = str(timestamp).split('.')[1]
        reference.username = str(
            self.request.POST['username']).replace(' ', '')
        reference.email = str(
            self.request.POST['email']).replace(' ', '').lower()
        reference.password = encrypt_password(
            str(self.request.POST['username']).replace(' ', ''),
            str(self.request.POST['new-password']).replace(' ', ''))
        reference.address = str(self.request.POST['address']).replace(' ', '')
        reference.save()

    def fetch(self, index=None):
        if index:
            user = Users.objects.values_list(
                'userid', 'username', 'email', 'address')

            return user[index-1]
        return Users.objects.values_list('username', 'email', 'address')

    def update(self, data, user_id):
        timestamp = datetime.datetime.now()
        Users.objects.filter(userid=user_id).update(
            userid=str(timestamp).split('.')[1],
            username=str(data['username']).replace(' ', ''),
            email=str(data['email']).replace(' ', '').lower(),
            password=encrypt_password(
                str(data['username']).replace(' ', ''),
                str(data['new-password']).replace(' ', '')),
            address=str(data['address']).replace(' ', ''))

    def delete(self, user_id):
        Users.objects.filter(userid=user_id).delete()
