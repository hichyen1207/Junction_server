from .models import User, Flags, Message, FriendList, Friend, Invitation_code, Applicant, Typeform_applicant, UserString, UserBoolaen, User_last_read_message, Device, Feedback_beta
from .invitationCode import createInvitationcode
import random
import requests, hashlib
import json
from websocket import create_connection
import datetime

def create_invitation_code():
    print('start')
    new_invitation_code_1 = Invitation_code(
        invitation_code='Vicky392',
        linked_code='Vicky0000'
    )

    new_invitation_code_2 = Invitation_code(
        invitation_code='Vicky133',
        linked_code='Vicky0000'
    )

    new_invitation_code_3 = Invitation_code(
        invitation_code='Vicky232',
        linked_code='Vicky0000'
    )

    new_invitation_code_1.save()
    new_invitation_code_2.save()
    new_invitation_code_3.save()

    print('end')

def delete_invitation_code():
    count = 1
    invitation_code_instances = Invitation_code.objects.all()
    for invitation_code_instance in invitation_code_instances:
        print(count)
        delete = True
        applicants = Applicant.objects.all()
        for applicant in applicants:
            if applicant.linked_code == invitation_code_instance.linked_code:
                delete = False
                break
        if delete:
            print(invitation_code_instance.linked_code, 'delete')
            invitation_code_instance.delete()
        count += 1

def typform_to_applicant():
    count_user = 1
    count = 0
    typeform_applicants = Typeform_applicant.objects.all()
    for typeform_applicant in typeform_applicants:
        print(count_user, 'start:')
        typeform_applicant_token = typeform_applicant.token
        applicants = Applicant.objects.all()
        is_applicant = False
        for applicant in applicants:
            if applicant.token == typeform_applicant_token:
                print('already in applicant')
                is_applicant = True
                break
        if not is_applicant:
            print(typeform_applicant.token, typeform_applicant.chinese_name)
            # create linked_code
            linked_code = typeform_applicant.english_name.replace(' ', '') + str(random.randint(1000, 9999))
            invitation_code_list = createInvitationcode(typeform_applicant.english_name)


            applicant = Applicant(
                token=typeform_applicant.token,
                language=typeform_applicant.language,
                chinese_name=typeform_applicant.english_name,
                english_name=typeform_applicant.english_name,
                gender=typeform_applicant.gender,
                job_title=typeform_applicant.job_title,
                company=typeform_applicant.company,
                career_len=typeform_applicant.career_len,
                job_type=typeform_applicant.job_type,
                industry_type=typeform_applicant.industry_type,
                college_name=typeform_applicant.college_name,
                college_major=typeform_applicant.college_major,
                grad_name=typeform_applicant.grad_name,
                grad_major=typeform_applicant.grad_major,
                phone_number=typeform_applicant.phone_number,
                email=typeform_applicant.email,
                satisfied_project=typeform_applicant.satisfied_project,
                cooperation_things=typeform_applicant.cooperation_things,

                pm_i_rating=typeform_applicant.pm_i_rating,
                market_i_rating=typeform_applicant.market_i_rating,
                ds_i_rating=typeform_applicant.ds_i_rating,
                uiux_i_rating=typeform_applicant.uiux_i_rating,
                startup_i_rating=typeform_applicant.startup_i_rating,
                sales_i_rating=typeform_applicant.sales_i_rating,
                finance_i_rating=typeform_applicant.finance_i_rating,
                it_i_rating=typeform_applicant.it_i_rating,
                business_i_rating=typeform_applicant.business_i_rating,
                other_i_rating=typeform_applicant.other_i_rating,

                pm_rating=typeform_applicant.pm_rating,
                market_rating=typeform_applicant.market_rating,
                ds_rating=typeform_applicant.ds_rating,
                uiux_rating=typeform_applicant.uiux_rating,
                startup_rating=typeform_applicant.startup_rating,
                sales_rating=typeform_applicant.sales_rating,
                finance_rating=typeform_applicant.finance_rating,
                it_rating=typeform_applicant.it_rating,
                business_rating=typeform_applicant.business_rating,
                other_rating=typeform_applicant.other_rating,

                linked_code=linked_code,
                invitation_code=invitation_code_list
            )

            # print(typeform_applicant.token, 'insert')
            payload = {
                'merge_fields': {
                    'BETA': 'YES',
                    'LINK_CODE': linked_code
                }
            }
            email_md5 = hashlib.md5(typeform_applicant.email.lower().encode('utf-8')).hexdigest()
            put_request = requests.put(
                'https://us17.api.mailchimp.com/3.0/lists/916a2d1aa2/members/%s' % email_md5,
                data=json.dumps(payload),
                auth=('Harrison', '5f81fd3e696f14de75c8b227d1b17636-us17')
            )

            print(put_request.content)
            if put_request.ok:
                try:
                    applicant.save()
                    for invitation_code in invitation_code_list:
                        new_invitation_code = Invitation_code(
                            invitation_code=invitation_code,
                            linked_code=linked_code
                        )
                        new_invitation_code.save()
                except Exception as e:
                    print(e)
                print(typeform_applicant.token, 'insert')

            count += 1
        count_user += 1
    print('done with:', count)

def deleteFriend(user1_id, user2_id, message_id):
    try:
        user1 = User.objects.get(user_id=user1_id)
        user1.update(pull__friends={'user_id': user2_id, 'message_id': message_id})
    except Exception as e:
        print('user 1 error:', e)

    try:
        user2 = User.objects.get(user_id=user2_id)
        user2.update(pull__friends={'user_id': user1_id, 'message_id': message_id})
    except Exception as e:
        print('user 2 error:', e)

    try:
        message = Message.objects.get(message_id=message_id)
        message.delete()
    except:
        print('Does not exist')

    print('done')

def sendMessage(user_id, message_id):
    print('Thomas send message')
    message_content = 'test message'
    ws = create_connection('ws://52.91.88.137/message/%s/' % (message_id))
    default_message_content = json.dumps({
        'user_id': user_id,
        'time': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        'content': message_content
    })
    ws.send(default_message_content)
    ws.close()

def fix_job_type_industry_type():
    count = 1
    typeform_applicants = Typeform_applicant.objects.all()
    for typeform_applicant in typeform_applicants:
        try:
            print(count, 'start:')
            token = typeform_applicant.token
            job_type = typeform_applicant.job_type
            industry_type = typeform_applicant.industry_type

            applicant = Applicant.objects.get(token=token)
            applicant.job_type = job_type
            applicant.industry_type = industry_type
            applicant.save()
            count += 1
        except:
            print(typeform_applicant.token, 'fial')
            count += 1
            continue

def fix_invitation_code():
    count = 1
    applicants = Applicant.objects.all()
    for applicant in applicants:
        print(count, 'start:')
        linked_code = applicant.linked_code
        invitation_codes = applicant.invitation_code
        for invitation_code in invitation_codes:
            code_instances = Invitation_code.objects.all()
            is_existed = False
            for code_instance in code_instances:
                code = code_instance.invitation_code
                if code == invitation_code:
                    is_existed = True
                    break
            if not is_existed:
                new_code = Invitation_code(
                    invitation_code=invitation_code,
                    linked_code=linked_code
                )
                new_code.save()
                print(invitation_code, 'insert!')
        count += 1


def typeform_to_applicant_with_token(token):
    typeform_applicant = Typeform_applicant.objects.get(token=token)
    print(typeform_applicant.token, typeform_applicant.chinese_name)
    # create linked_code
    linked_code = typeform_applicant.english_name.replace(' ', '') + str(random.randint(1000, 9999))
    invitation_code_list = createInvitationcode(typeform_applicant.english_name)

    applicant = Applicant(
        token=typeform_applicant.token,
        language=typeform_applicant.language,
        chinese_name=typeform_applicant.english_name,
        english_name=typeform_applicant.english_name,
        gender=typeform_applicant.gender,
        job_title=typeform_applicant.job_title,
        company=typeform_applicant.company,
        career_len=typeform_applicant.career_len,
        job_type=typeform_applicant.job_type,
        industry_type=typeform_applicant.industry_type,
        college_name=typeform_applicant.college_name,
        college_major=typeform_applicant.college_major,
        grad_name=typeform_applicant.grad_name,
        grad_major=typeform_applicant.grad_major,
        phone_number=typeform_applicant.phone_number,
        email=typeform_applicant.email,
        satisfied_project=typeform_applicant.satisfied_project,
        cooperation_things=typeform_applicant.cooperation_things,

        pm_i_rating=typeform_applicant.pm_i_rating,
        market_i_rating=typeform_applicant.market_i_rating,
        ds_i_rating=typeform_applicant.ds_i_rating,
        uiux_i_rating=typeform_applicant.uiux_i_rating,
        startup_i_rating=typeform_applicant.startup_i_rating,
        sales_i_rating=typeform_applicant.sales_i_rating,
        finance_i_rating=typeform_applicant.finance_i_rating,
        it_i_rating=typeform_applicant.it_i_rating,
        business_i_rating=typeform_applicant.business_i_rating,
        other_i_rating=typeform_applicant.other_i_rating,

        pm_rating=typeform_applicant.pm_rating,
        market_rating=typeform_applicant.market_rating,
        ds_rating=typeform_applicant.ds_rating,
        uiux_rating=typeform_applicant.uiux_rating,
        startup_rating=typeform_applicant.startup_rating,
        sales_rating=typeform_applicant.sales_rating,
        finance_rating=typeform_applicant.finance_rating,
        it_rating=typeform_applicant.it_rating,
        business_rating=typeform_applicant.business_rating,
        other_rating=typeform_applicant.other_rating,

        linked_code=linked_code,
        invitation_code=invitation_code_list
    )

    # print(typeform_applicant.token, 'insert')
    payload = {
        'merge_fields': {
            'BETA': 'YES',
            'LINK_CODE': linked_code
        }
    }
    email_md5 = hashlib.md5(typeform_applicant.email.lower().encode('utf-8')).hexdigest()
    put_request = requests.put(
        'https://us17.api.mailchimp.com/server/%s' % email_md5,
        data=json.dumps(payload),
        auth=('Harrison', '*********************************')
    )

    print(put_request.content)
    if put_request.ok:
        try:
            applicant.save()
            for invitation_code in invitation_code_list:
                new_invitation_code = Invitation_code(
                    invitation_code=invitation_code,
                    linked_code=linked_code
                )
                new_invitation_code.save()
        except Exception as e:
            print(e)
        print(typeform_applicant.token, 'insert')