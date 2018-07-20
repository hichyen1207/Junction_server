import random
import json
import jwt
import re
import boto3
import base64
import datetime, time
import os
import requests, hashlib

from django.http import HttpResponse, Http404
from mongoengine import DoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, Flags, Message, FriendList, Friend, Invitation_code, Applicant, Typeform_applicant, UserString, UserBoolaen, User_last_read_message, Device, Feedback_beta
from .serializers import UserSerializer, FriendListSerializer, MessageDetailSerializer,FriendsSerializer, InvitationCodeSerializer
from .invitationCode import createInvitationcode
from django.core.mail import EmailMultiAlternatives
from apns2.client import APNsClient
from apns2.payload import Payload
from websocket import create_connection
# from Server.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_NAME, AWS_S3_REGION
# from Server.settings import APNS_CERT, MAIL_FILE, APNS_TOPIC, USE_SANDBOX

from Server.setting.base import APNS_CERT, MAIL_FILE, APNS_TOPIC, USE_SANDBOX
if os.environ['DJANGO_SETTINGS_MODULE'] == 'Server.setting.prod':
    from Server.setting.prod import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_NAME, AWS_S3_REGION
else:
    from Server.setting.dev import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_NAME, AWS_S3_REGION

class CheckUser(APIView):
    def get(self, request, id):
        try:
            user = User.objects.get(user_id=id)
            return Response({"user_exist": True})
        except DoesNotExist:
            return Response({"user_exist": False})

class UserList(APIView):
    # def get(self, request):
    #     userList = User.objects.all()
    #     serializer = UserSerializer(userList, many=True)
    #     return Response(serializer.data)

    def post(self, request):
        user_id = request.data['user_id']
        id_type = request.data['id_type']
        chinese_name = request.data['chinese_name']
        english_name = request.data['english_name']
        photo = request.data['photo']
        gender = request.data['gender']
        job_title = request.data['job_title']
        company = request.data['company']
        career_year = request.data['career_year']
        job_type = request.data['job_type']
        industry_type = request.data['industry_type']
        bachelor_school = request.data['bachelor_school']
        bachelor_major = request.data['bachelor_major']
        master_school = request.data['master_school']
        master_major = request.data['master_major']
        phone_number = request.data['phone_number']
        email = request.data['email']
        introduction = request.data['introduction']
        satisfied_project = request.data['satisfied_project']
        cooperation_things = request.data['cooperation_things']
        linked_code = request.data['linked_code']

        pm_i_rating = request.data['pm_i_rating']
        marketing_i_rating = request.data['marketing_i_rating']
        data_analysis_i_rating = request.data['data_analysis_i_rating']
        uiux_i_rating = request.data['uiux_i_rating']
        startup_i_rating = request.data['startup_i_rating']
        sales_i_rating = request.data['sales_i_rating']
        finance_i_rating = request.data['finance_i_rating']
        information_technology_i_rating = request.data['information_technology_i_rating']
        business_i_rating = request.data['business_i_rating']
        other_i_rating = request.data['other_i_rating']

        pm_rating = request.data['pm_rating']
        marketing_rating = request.data['marketing_rating']
        data_analysis_rating = request.data['data_analysis_rating']
        uiux_rating = request.data['uiux_rating']
        startup_rating = request.data['startup_rating']
        sales_rating = request.data['sales_rating']
        finance_rating = request.data['finance_rating']
        information_technology_rating = request.data['information_technology_rating']
        business_rating = request.data['business_rating']
        other_rating = request.data['other_rating']

        # Get token and invitation_code from applicant
        applicant = Applicant.objects.get(linked_code=linked_code)
        token = applicant.token
        invitation_code = applicant.invitation_code

        # upload user photo to S3
        s3 = boto3.resource('s3', AWS_S3_REGION,
                            aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        bucket = AWS_BUCKET_NAME
        user_photo_object = s3.Object(bucket, 'images/user/%s.jpg' % user_id)
        user_photo_object.put(ACL='public-read', Body=base64.b64decode(photo))
        photo_url = 'https://s3-ap-southeast-1.amazonaws.com/junction-server/images/user/%s.jpg' % user_id

        # interest_issue Flags
        interest_issue = Flags(
            pm=pm_i_rating,
            marketing=marketing_i_rating,
            data_analysis=data_analysis_i_rating,
            uiux=uiux_i_rating,
            startup=startup_i_rating,
            sales=sales_i_rating,
            finance=finance_i_rating,
            information_technology=information_technology_i_rating,
            business=business_i_rating,
            other=other_i_rating
        )

        # professional_field Flags
        professional_field = Flags(
            pm=pm_rating,
            marketing=marketing_rating,
            data_analysis=data_analysis_rating,
            uiux=uiux_rating,
            startup=startup_rating,
            sales=sales_rating,
            finance=finance_rating,
            information_technology=information_technology_rating,
            business=business_rating,
            other=other_rating
        )

        # User
        user = User(
            user_id=user_id,
            id_type=id_type,
            token=token,
            chinese_name=chinese_name,
            english_name=english_name,
            photo=photo_url,
            gender=gender,
            bachelor_school=bachelor_school,
            bachelor_major=bachelor_major,
            master_school=master_school,
            master_major=master_major,
            company=company,
            job_title=job_title,
            career_year=career_year,
            job_type=job_type,
            industry_type=industry_type,
            phone_number=phone_number,
            email=email,
            introduction=introduction,
            professional_field=professional_field,
            interest_issue=interest_issue,
            satisfied_project=satisfied_project,
            cooperation_things=cooperation_things,
            invitation_code=invitation_code,
            linked_code=linked_code,
            device=Device(),
            draw_card_status='undraw',
            card_drawer = '10102347454878415',
            card_drawer_of_next_day = '10102347454878415'
        )

        try:
            user.save()
        except Exception as e:
            print(e)
            raise HttpResponse(status=500, content=e)

        return Response({
            "message": "user insert successfully."
        })

class CheckInvitationCode(APIView):
    def get(self, request, invitation_code):
        try:
            invitation_code_instance = Invitation_code.objects.get(invitation_code=invitation_code)
            token = invitation_code_instance.token
            is_used = invitation_code_instance.is_used

            if is_used:
                return HttpResponse(status=500, content="this invitation code is used up")
            else:
                return Response({
                    "message": "this invitation code is valid"
                })
        except DoesNotExist:
            return HttpResponse(status=404, content="invitation code does not exist")

class UserDetail(APIView):
    def get(self, request, id):
        try:
            # get user
            user = User.objects.get(user_id=id)

            # change other tags to 'other' from job_type and industry_type
            for index in range(len(user.job_type)):
                if user.job_type[index] not in ['產品管理', '使用者體驗', '數據分析', '行銷', '銷售', '工程', '資訊科技', '金融', '策略']:
                    user.job_type[index] = '其他'

            if user.industry_type not in ['軟體網路', '半導體及電子', '消費性產品', '傳產製造', '金融服務', '法律及會計', '旅遊休閒']:
                user.industry_type = '其他'
            else:
                user.industry_type = user.industry_type

            serializer = UserSerializer(user)
            return Response(serializer.data)
        except DoesNotExist:
            raise Http404

    def put(self, request, id):
        try:
            user = User.objects.get(user_id=id)

            chinese_name = request.data['chinese_name']
            english_name = request.data['english_name']
            photo = request.data['photo']
            gender = request.data['gender']
            job_title = request.data['job_title']
            company = request.data['company']
            career_year = request.data['career_year']
            job_type = request.data['job_type']
            industry_type = request.data['industry_type']
            bachelor_school = request.data['bachelor_school']
            bachelor_major = request.data['bachelor_major']
            master_school = request.data['master_school']
            master_major = request.data['master_major']
            phone_number = request.data['phone_number']
            email = request.data['email']
            introduction = request.data['introduction']
            satisfied_project = request.data['satisfied_project']
            cooperation_things = request.data['cooperation_things']

            pm_i_rating = request.data['pm_i_rating']
            marketing_i_rating = request.data['marketing_i_rating']
            data_analysis_i_rating = request.data['data_analysis_i_rating']
            uiux_i_rating = request.data['uiux_i_rating']
            startup_i_rating = request.data['startup_i_rating']
            sales_i_rating = request.data['sales_i_rating']
            finance_i_rating = request.data['finance_i_rating']
            information_technology_i_rating = request.data['information_technology_i_rating']
            business_i_rating = request.data['business_i_rating']
            other_i_rating = request.data['other_i_rating']

            pm_rating = request.data['pm_rating']
            marketing_rating = request.data['marketing_rating']
            data_analysis_rating = request.data['data_analysis_rating']
            uiux_rating = request.data['uiux_rating']
            startup_rating = request.data['startup_rating']
            sales_rating = request.data['sales_rating']
            finance_rating = request.data['finance_rating']
            information_technology_rating = request.data['information_technology_rating']
            business_rating = request.data['business_rating']
            other_rating = request.data['other_rating']

            user.chinese_name = chinese_name
            user.english_name = english_name
            user.gender = gender
            user.job_title = job_title
            user.company = company
            user.career_year = career_year
            user.job_type = job_type
            user.industry_type = industry_type
            user.bachelor_school = bachelor_school
            user.bachelor_major = bachelor_major
            user.master_school = master_school
            user.master_major = master_major
            user.phone_number = phone_number
            user.email = email
            user.introduction = introduction
            user.satisfied_project = satisfied_project
            user.cooperation_things = cooperation_things

            user.interest_issue.pm = pm_i_rating
            user.interest_issue.marketing = marketing_i_rating
            user.interest_issue.data_analysis = data_analysis_i_rating
            user.interest_issue.uiux = uiux_i_rating
            user.interest_issue.startup = startup_i_rating
            user.interest_issue.sales = sales_i_rating
            user.interest_issue.finance = finance_i_rating
            user.interest_issue.information_technology = information_technology_i_rating
            user.interest_issue.business = business_i_rating
            user.interest_issue.other = other_i_rating

            user.professional_field.pm = pm_rating
            user.professional_field.marketing = marketing_rating
            user.professional_field.data_analysis = data_analysis_rating
            user.professional_field.uiux = uiux_rating
            user.professional_field.startup = startup_rating
            user.professional_field.sales = sales_rating
            user.professional_field.finance = finance_rating
            user.professional_field.information_technology = information_technology_rating
            user.professional_field.business = business_rating
            user.professional_field.other = other_rating

            # upload to AWS S3
            photo_url = 'https://s3-ap-southeast-1.amazonaws.com/junction-server/images/user/%s.jpg' % id
            if photo == photo_url:
                pass
            elif photo == 'default':
                user.photo = 'https://s3-ap-southeast-1.amazonaws.com/junction-server/images/user/default.jpg'
            else:
                s3 = boto3.resource('s3', AWS_S3_REGION,
                                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
                bucket = AWS_BUCKET_NAME
                user_photo_object = s3.Object(bucket, 'images/user/%s.jpg' % id)
                user_photo_object.put(ACL='public-read', Body=base64.b64decode(photo))

            user.save()

            return Response({
                "message": "Update successfully"
            })

        except DoesNotExist:
            raise Http404

class FriendsList(APIView):
    def get(self, request, id):
        try:
            friendDetailList = list()
            user = User.objects.get(user_id=id)
            friendList = user.friends
            for friend in friendList:
                # get friend Object and other fields
                friendDetail = User.objects.get(user_id=str(friend.user_id))
                friend_id = str(friend.user_id)
                message_id = str(friend.message_id)
                friend_chinese_name = friendDetail.chinese_name
                friend_english_name = friendDetail.english_name
                friend_photo = friendDetail.photo
                friend_job_title = friendDetail.job_title

                # get message Object and count unread message and last message time
                message = Message.objects.get(message_id=message_id)
                total_message = len(message.messages)
                unread_message_number = 0
                if message.user_id.user_1 == friend_id:
                    last_read_message = message.last_read_message.user_1
                else:
                    last_read_message = message.last_read_message.user_2

                for message_index in range(last_read_message, total_message):
                    if message.messages[message_index].user_id == friend_id and message.messages[message_index].is_read == False:
                        unread_message_number += 1
                try:
                    last_message_time = message.messages[total_message-1].time
                except:
                    last_message_time = ""

                friendPreview = FriendList(
                    user_id=friend_id,
                    message_id=message_id,
                    chinese_name=friend_chinese_name,
                    english_name=friend_english_name,
                    photo=friend_photo,
                    job_title=friend_job_title,
                    unread_message_number=unread_message_number,
                    last_message_time=last_message_time
                )
                serializer = FriendListSerializer(friendPreview)
                friendDetailList.append(serializer.data)
            return Response(friendDetailList)

        except DoesNotExist:
            raise Http404

class FriendInvitation(APIView):
    def put(self, request, id):
        try:
            # check parameter
            # parameter needs to be:
            #   message: invite
            #   action: accept/reject
            receive_data = json.loads(request.body).get('message')
            if receive_data == "invite":
                receive_action = json.loads(request.body).get('action')
                if receive_action == "accept":
                    # user1 -> user who call the API
                    # user2 -> user1's card_drawer
                    user1 = User.objects.get(user_id=id)
                    user1_id = str(user1.user_id)
                    user1.update(draw_card_status='accept')
                    user2_id = user1.card_drawer
                    user2 = User.objects.get(user_id=str(user2_id))
                    user2_draw_card_status = user2.draw_card_status

                    if user2_id == '10102347454878415':
                        # create message_id
                        user1_code = ''.join(re.findall("[a-zA-Z0-9]+", user1_id)).replace(" ", '')
                        user1_code = ''.join(random.sample(user1_code, len(user1_code)))[:5]
                        user2_code = ''.join(re.findall("[a-zA-Z0-9]+", user2_id)).replace(" ", '')
                        user2_code = ''.join(random.sample(user2_code, len(user2_code)))[:5]
                        message_id = 'C' + user1_code + 'x' + user2_code

                        userString = UserString(
                            user_1=user1_id,
                            user_2=user2_id
                        )
                        user_last_read_message = User_last_read_message()
                        message = Message(
                            message_id=message_id,
                            user_id=userString,
                            notification=UserBoolaen(),
                            last_read_message=user_last_read_message
                        )

                        # add friend to user1
                        in_user1_friends = False
                        for friend in user1.friends:
                            if friend.user_id == user2.user_id:
                                in_user1_friends = True
                                break
                        if not in_user1_friends:
                            friend2 = Friend(user_id=user2_id, message_id=message_id)
                            user1.update(add_to_set__friends=friend2)

                        # add friend to user2
                        in_user2_friends = False
                        for friend in user2.friends:
                            if friend.user_id == user1.user_id:
                                in_user2_friends = True
                                break
                        if not in_user2_friends:
                            friend1 = Friend(user_id=user1_id, message_id=message_id)
                            user2.update(add_to_set__friends=friend1)

                        # save message
                        if not in_user1_friends or not in_user2_friends:
                            message.save()

                        # Send Push Notifications
                        try:
                            custome_payload = {
                                'type': 'friend'
                            }
                            # Send Push Notifications to user1
                            if user1.device.ios != '':
                                user1_payload = Payload(
                                    alert='􏰃􏰄􏰅􏰆􏰇􏰈􏰉恭喜你已經和 Thomas 成為好友囉！',
                                    sound="default", badge=1,
                                    custom=custome_payload
                                )
                                client = APNsClient(APNS_CERT, use_sandbox=USE_SANDBOX, use_alternative_port=False)
                                client.send_notification(user1.device.ios, user1_payload, APNS_TOPIC)
                        except Exception as e:
                            print(e)

                        # Thomas Send Default Message
                        print('Thomas send message')
                        message_content = '嗨！你好，我是Junction的CEO Thomas，很高興你可以加入我們的網路。如果有什麼我可以協助你的，可以直接在這裡訊息給我，我會親自為你服務！'
                        ws = create_connection('ws://52.91.88.137/message/%s/' % (message_id))
                        default_message_content = json.dumps({
                            'user_id': user2_id,
                            'time': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                            'content': message_content
                        })
                        ws.send(default_message_content)
                        ws.close()

                        # message Push Notification
                        user1_device_id = user1.device.ios
                        notification_content = user2.english_name + ': ' + message_content
                        try:
                            if user1_device_id != '':
                                custom_payload = {
                                    'type': 'message',
                                    'message_id': message_id,
                                    'user_id': user2_id,
                                    'english_name': user2.english_name,
                                    'chinese_name': user2.chinese_name,
                                    'photo': user2.photo
                                }
                                payload = Payload(alert=notification_content, sound="default", badge=1,
                                                  custom=custom_payload)
                                client = APNsClient(APNS_CERT, use_sandbox=USE_SANDBOX, use_alternative_port=False)
                                client.send_notification(user1_device_id, payload, APNS_TOPIC)
                        except Exception as e:
                            print(e)

                        return Response({
                            "message": "these two user become friends!"
                        })
                    else:
                        # check if user2 also accept the invitation
                        if user2_draw_card_status == 'accept' and user2.card_drawer == user1_id:
                            # create message_id
                            user1_code = ''.join(re.findall("[a-zA-Z0-9]+", user1_id)).replace(" ", '')
                            user1_code = ''.join(random.sample(user1_code, len(user1_code)))[:5]
                            user2_code = ''.join(re.findall("[a-zA-Z0-9]+", user2_id)).replace(" ", '')
                            user2_code = ''.join(random.sample(user2_code, len(user2_code)))[:5]
                            message_id = 'C' + user1_code + 'x' + user2_code

                            userString = UserString(
                                user_1=user1_id,
                                user_2=user2_id
                            )
                            user_last_read_message = User_last_read_message()
                            message = Message(
                                message_id=message_id,
                                user_id=userString,
                                notification=UserBoolaen(),
                                last_read_message=user_last_read_message
                            )
                            message.save()

                            # add friend to user1
                            friend2 = Friend(user_id=user2_id, message_id=message_id)
                            user1.update(add_to_set__friends=friend2)

                            # add friend to user2
                            friend1 = Friend(user_id=user1_id, message_id=message_id)
                            user2.update(add_to_set__friends=friend1)

                            # Send Push Notifications
                            try:
                                custome_payload = {
                                    'type': 'friend'
                                }
                                # Send Push Notifications to user1
                                if user1.device.ios != '':
                                    user1_payload = Payload(alert='恭喜你已經和 %s 成為好友囉！' % (user2.english_name), sound="default", badge=1, custom=custome_payload)
                                    client = APNsClient(APNS_CERT, use_sandbox=USE_SANDBOX, use_alternative_port=False)
                                    client.send_notification(user1.device.ios, user1_payload, APNS_TOPIC)

                                # Send Push Notifications to user2
                                if user2.device.ios != '':
                                    user2_payload = Payload(alert='恭喜你已經和 %s 成為好友囉！' % (user1.english_name), sound="default", badge=1, custom=custome_payload)
                                    client = APNsClient(APNS_CERT, use_sandbox=USE_SANDBOX, use_alternative_port=False)
                                    client.send_notification(user2.device.ios, user2_payload, APNS_TOPIC)
                            except Exception as e:
                                print(e)

                            return Response({
                                "message": "these two user become friends!"
                            })
                        else:
                            # user2 doesn't accept the invitation
                            return Response({
                                "message": "waiting for another user accepts the invitation!"
                            })
                elif receive_action == "reject":
                    # user1 reject the invitation
                    user = User.objects.get(user_id=id)
                    user.update(draw_card_status='reject')

                    return Response({
                        "message": "Reject friend invitation."
                    })
                else:
                    # wrong action
                    return HttpResponse(status=500, content="error action")
            else:
                # wrong message
                return HttpResponse(status=500, content="error message")
        except DoesNotExist:
            raise Http404

class DrawCardStatus(APIView):
    def get(self, request, id):
        try:
            user = User.objects.get(user_id=id)
            draw_card_status = user.draw_card_status
            return Response({
                "draw_card_status": draw_card_status
            })
        except DoesNotExist:
            raise Http404

    def put(self, request, id):
        try:
            message = request.data['message']
            if message == 'draw card':
                user = User.objects.get(user_id=id)
                user.update(draw_card_status='draw')
                return Response({
                    'message': 'user draws card successfully'
                })
            else:
                return HttpResponse(status=500, content="error message")
        except DoesNotExist:
            raise Http404

class CardDetail(APIView):
    def get(self, request, id):
        try:
            # note: draw_card_status in response is user's status, not card_drawer's
            user = User.objects.get(user_id=id)
            friend_draw_card_status = user.draw_card_status
            card_drawer_id = user.card_drawer
            card_drawer = User.objects.get(user_id=card_drawer_id)
            card_drawer.draw_card_status = friend_draw_card_status
            serializer = FriendsSerializer(card_drawer)
            return  Response(serializer.data)
        except DoesNotExist:
            raise Http404

class MessageDetail(APIView):
    def get(self, request, id):
        try:
            message = Message.objects.get(message_id=id)
            serializer = MessageDetailSerializer(message)
            return Response(serializer.data)
        except DoesNotExist:
            raise Http404

class ReadMessage(APIView):
    def put(self, request, message_id):
        try:
            # check parameter
            # parameter needs to be:
            #   message: read
            #  user_id: <iser_id> (note: user_id is the user who read the message)
            receive_data = json.loads(request.body).get('message')
            user_id = json.loads(request.body).get('user_id')
            if receive_data == "read":
                message = Message.objects.get(message_id=message_id)

                # check which user is reader and which is sender
                read_message_user = message.user_id.user_1
                if read_message_user == user_id:
                    another_message_user = message.user_id.user_2
                    last_read_message = message.last_read_message.user_1
                else:
                    read_message_user = message.user_id.user_2
                    another_message_user = message.user_id.user_1
                    last_read_message = message.last_read_message.user_2

                # change the unread message to read
                total_message = len(message.messages)
                print(another_message_user)
                for messages_index in range(last_read_message, total_message):
                    if message.messages[messages_index].user_id == another_message_user:
                        message.messages[messages_index].is_read = True

                # update the read messages number
                if read_message_user == message.user_id.user_1:
                    message.last_read_message.user_1 = total_message
                else:
                    message.last_read_message.user_2 = total_message
                message.save()
                return Response({
                    "message": "user: " + user_id + " reads messages."
                })
            else:
                return HttpResponse(status=500, content="error message")
        except DoesNotExist:
            raise Http404

class UpdateMessageNotification(APIView):
    def put(self, request, message_id):
        try:
            user_id = json.loads(request.body).get('user_id')
            notification_status = json.loads(request.body).get('notification')
            message = Message.objects.get(message_id=message_id)
            # check user_1 or user_2
            if user_id == message.user_id.user_1:
                # user is user 1
                message.notification.user_1 = notification_status
            else:
                # user is user 2
                message.notification.user_2 = notification_status
            message.save()
            return Response({
                "message": "update successfully"
            })
        except:
            raise Http404

class InvitationCodeGetter(APIView):
    def get(self, request, linked_code):
        try:
            invitation_code_instance_list = Invitation_code.objects(linked_code=linked_code)
            print(invitation_code_instance_list)
            serializer = InvitationCodeSerializer(invitation_code_instance_list, many=True)
            return Response(serializer.data)
        except DoesNotExist:
            raise Http404

class DeviceSetting(APIView):
    def put(self, request, id):
        try:
            user = User.objects.get(user_id=id)
            request_data = json.loads(request.body)
            for key, value in request_data.items():
                if key == 'ios':
                    print(value)
                    print(user.device.ios)
                    user.device.ios = value
                if key == 'android':
                    print(value)
                    user.device.android = value
            user.save()
            return Response({
                "message": "setting is successful"
            })
        except DoesNotExist:
            raise Http404

class UserReport(APIView):
    def get(self, request, id):
        try:
            user = User.objects.get(user_id=id)
            mail_content = '''
                ID: %s,
                English name: %s,
                Chinese name: %s,
                gender: %s
                email: %s,
                phone number: %s,
                photo: %s,
                company: %s,
            ''' % (user.user_id, user.english_name, user.chinese_name, user.gender, user.email, user.phone_number, user.photo, user.company)
            try:
                msg = EmailMultiAlternatives(
                    'User Report',
                    mail_content,
                    'report@junction.solutions',
                    ['report@junction.solutions']
                )
                msg.send()
            except Exception as e:
                print(e)
            return Response({
                'message': 'report successfully'
            })
        except:
            raise Http404

# Web Flow

class ApplicantRegister(APIView):
    def get(self, request, token):
        try:
            typeform_applicant = Typeform_applicant.objects.get(token=token)
            try:
                # check if applicant already existed
                check_applicant = Applicant.objects.get(token=token)

                return HttpResponse(
                    status=500,
                    content="applicant has already registered"
                )
            except:
                # create linked_code
                linked_code = typeform_applicant.english_name.replace(' ', '') + str(random.randint(1000, 9999))
                invitation_code_list = createInvitationcode(typeform_applicant.english_name)
                for invitation_code in invitation_code_list:
                    new_invitation_code = Invitation_code(
                        invitation_code=invitation_code,
                        linked_code=linked_code
                    )

                # uniform the different names of the tags in job_type and industry_type
                applicant_job_type = typeform_applicant.job_type
                fixed_job_type = list()
                for item in applicant_job_type:
                    if 'Product Management' in item:
                        item = '產品管理'
                        fixed_job_type.append(item)
                    elif 'UI / UX Design' in item:
                        item = '使用者體驗'
                        fixed_job_type.append(item)
                    elif 'Data Analytics' in item:
                        item = '數據分析'
                        fixed_job_type.append(item)
                    elif 'Marketing' in item:
                        item = '行銷'
                        fixed_job_type.append(item)
                    elif 'Sales / Business Development' in item:
                        item = '銷售'
                        fixed_job_type.append(item)
                    elif 'Engineering' in item:
                        item = '工程'
                        fixed_job_type.append(item)
                    elif 'IT' in item:
                        item = '資訊科技'
                        fixed_job_type.append(item)
                    elif 'Finance' in item:
                        item = '金融'
                        fixed_job_type.append(item)
                    elif 'Strategy' in item:
                        item = '策略'
                        fixed_job_type.append(item)
                    else:
                        fixed_job_type.append(item)

                applicant_industry_type = typeform_applicant.industry_type
                if 'Software and Internet' in applicant_industry_type:
                    applicant_industry_type = '軟體網路'
                elif 'Hardware and Semiconductor' in applicant_industry_type:
                    applicant_industry_type = '半導體及電子'
                elif 'Consumer Packaged Goods' in applicant_industry_type:
                    applicant_industry_type = '消費性產品'
                elif 'Traditional Manufacturing' in applicant_industry_type:
                    applicant_industry_type = '傳產製造'
                elif 'Financial Services' in applicant_industry_type:
                    applicant_industry_type = '金融服務'
                elif 'Legal and Auditing Services' in applicant_industry_type:
                    applicant_industry_type = '法律及會計'
                elif 'Media and Education' in applicant_industry_type:
                    applicant_industry_type = '文教傳播'
                elif 'Tourism' in applicant_industry_type:
                    applicant_industry_type = '旅遊休閒'

                applicant = Applicant(
                    token=typeform_applicant.token,
                    language=typeform_applicant.language,
                    chinese_name=typeform_applicant.chinese_name,
                    english_name=typeform_applicant.english_name,
                    gender=typeform_applicant.gender,
                    job_title=typeform_applicant.job_title,
                    company=typeform_applicant.company,
                    career_len=typeform_applicant.career_len,
                    job_type=fixed_job_type,
                    industry_type=applicant_industry_type,
                    college_name=typeform_applicant.college_name,
                    college_major=typeform_applicant.college_major,
                    grad_name=typeform_applicant.grad_name,
                    grad_major=typeform_applicant.grad_major,
                    phone_number=typeform_applicant.phone_number,
                    email=typeform_applicant.email,
                    satisfied_project=typeform_applicant.satisfied_project,
                    cooperation_things=typeform_applicant.cooperation_things,

                    pm_i_rating=typeform_applicant.pm_i_rating,
                    market_i_rating = typeform_applicant.market_i_rating,
                    ds_i_rating = typeform_applicant.ds_i_rating,
                    uiux_i_rating = typeform_applicant.uiux_i_rating,
                    startup_i_rating = typeform_applicant.startup_i_rating,
                    sales_i_rating = typeform_applicant.sales_i_rating,
                    finance_i_rating = typeform_applicant.finance_i_rating,
                    it_i_rating = typeform_applicant.it_i_rating,
                    business_i_rating = typeform_applicant.business_i_rating,
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

                new_invitation_code.save()
                applicant.save()

                # Send confirmation email to applicant
                # try:
                #     with open(MAIL_FILE) as f:
                #         mail_content = f.read()
                #         mail_content = mail_content.replace('<% english_name %>', applicant.english_name).replace('<% linked_code %>', applicant.linked_code)
                #     msg = EmailMultiAlternatives('Django Test', mail_content, 'sign_up@junction.solutions', ['hichyen1207@gmail.com'])
                #     msg.attach_alternative(mail_content, "text/html")
                #     msg.send()
                # except Exception as e:
                #     print(e)

                #  call mailchimp API
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

                if put_request.ok:
                    return Response({
                        "message": "applicant insert successfully."
                    })
                else:
                    return HttpResponse(status=500, content='fail to update mailchimps')

        except:
            raise Http404

class CheckApplicant(APIView):
    def get(self, request, linked_code):
        # check applicant
        try:
            applicant = Applicant.objects.get(linked_code=linked_code)

            # check user
            try:
                user = User.objects.get(linked_code=linked_code)

                return Response({
                    "applicant_exist": True,
                    "user_exist": True
                })
            except DoesNotExist:
                return Response({
                    "applicant_exist": True,
                    "user_exist": False
                })

        except DoesNotExist:
            return Response({
                "applicant_exist": False,
                "user_exist": False
            })

class ApplicantDetail(APIView):
    def get(self, request, linked_code):
        try:
            applicant = Applicant.objects.get(linked_code=linked_code)

            # change other tags to 'other'
            job_type = applicant.job_type
            for index in range(len(job_type)):
                if job_type[index] not in ['產品管理', '使用者體驗', '數據分析', '行銷', '銷售', '工程', '資訊科技', '金融', '策略']:
                    job_type[index] = '其他'

            if applicant.industry_type not in ['軟體網路', '半導體及電子', '消費性產品', '傳產製造', '金融服務', '法律及會計', '旅遊休閒']:
                industry_type = '其他'
            else:
                industry_type = applicant.industry_type

            return Response({
                'token': applicant.token,
                'chinese_name': applicant.chinese_name,
                'english_name': applicant.english_name,
                'gender': applicant.gender,
                'phone_number': applicant.phone_number,
                'email': applicant.email,
                'career_year': applicant.career_len,
                'company': applicant.company,
                'job_title': applicant.job_title,
                'job_type': job_type,
                'industry_type': industry_type,
                'bachelor_school': applicant.college_name,
                'bachelor_major': applicant.college_major,
                'master_school': applicant.grad_name,
                'master_major': applicant.grad_major,
                'satisfied_project': applicant.satisfied_project,
                'cooperation_things': applicant.cooperation_things,
                'linked_code': applicant.linked_code,
                'invitation_code': applicant.invitation_code,
                'professional_field': {
                    'pm': applicant.pm_rating,
                    'marketing': applicant.market_rating,
                    'data_analysis': applicant.ds_rating,
                    'uiux': applicant.uiux_rating,
                    'startup': applicant.startup_rating,
                    'sales': applicant.sales_rating,
                    'finance': applicant.finance_rating,
                    'information_technology': applicant.it_rating,
                    'business': applicant.business_rating,
                    'other': applicant.other_rating
                },
                'interest_issue': {
                    'pm': applicant.pm_i_rating,
                    'marketing': applicant.market_i_rating,
                    'data_analysis': applicant.ds_i_rating,
                    'uiux': applicant.uiux_i_rating,
                    'startup': applicant.startup_i_rating,
                    'sales': applicant.sales_i_rating,
                    'finance': applicant.finance_i_rating,
                    'information_technology': applicant.it_i_rating,
                    'business': applicant.business_i_rating,
                    'other': applicant.other_i_rating
                }
            })
        except DoesNotExist:
            raise Http404

# Feedback API

class BetaFeedback(APIView):
    def post(self, request):
        try:
            user_id = request.data['user_id']
            score = request.data['score']
            feedback = Feedback_beta(
                user_id=user_id,
                score=score
            )
            feedback.save()
            return Response({
                'message': 'scoring successfully'
            })
        except DoesNotExist:
            raise Http404
