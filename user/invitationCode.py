import random
import string
from .models import Invitation_code

def createInvitationcode(english_name):
    print('start creat invitation code')
    new_invitation_code_prefix = english_name.replace(' ', '')
    code_exist = True
    while(code_exist):
        code_exist = False
        new_invitation_code_prefix += 'x'

        invitation_code_instance_set = Invitation_code.objects.all()
        for invitation_code_instance in invitation_code_instance_set:
            code = invitation_code_instance.invitation_code[:-3]
            if code == new_invitation_code_prefix:
                code_exist = True
                print('code already exist')

    random_num_list = list()
    for count in range(3):
        random_num = random.randrange(100, 999)
        if random_num not in random_num_list:
            random_num_list.append(random_num)

    invitation_code_list = list()
    for number in random_num_list:
        invitation_code_list.append(new_invitation_code_prefix + str(number))

    return invitation_code_list

