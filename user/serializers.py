from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework import serializers
from .models import User, FriendList, Message, Invitation_code, Applicant, Typeform_applicant

class UserSerializer(DocumentSerializer):

    class Meta:
        model = User
        fields = '__all__'

class FriendsSerializer(DocumentSerializer):

    class Meta:
        model = User
        fields = ('user_id', 'chinese_name', 'english_name', 'gender', 'photo', 'company', 'job_title', 'job_type',
                  'industry_type', 'bachelor_school', 'bachelor_major', 'master_school', 'master_major', 'email', 'phone_number', 'introduction', 'interest_issue',
                  'professional_field', 'satisfied_project', 'cooperation_things', 'draw_card_status')

class FriendListSerializer(DocumentSerializer):

    class Meta:
        model = FriendList
        fields = ('message_id', 'user_id', 'chinese_name', 'english_name', 'photo', 'job_title', 'unread_message_number', 'last_message_time')


class MessageDetailSerializer(DocumentSerializer):

    class Meta:
        model = Message
        fields = '__all__'

class InvitationCodeSerializer(DocumentSerializer):

    class Meta:
        model = Invitation_code
        fields = ('invitation_code', 'is_used')