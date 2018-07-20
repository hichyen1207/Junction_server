from mongoengine import *
import os
# from Server.settings import MONGODB_HOST, MONGODB_DB_NAME, MONGODB_USER, MONGODB_PASSWORD

if os.environ['DJANGO_SETTINGS_MODULE'] == 'Server.setting.prod':
    from Server.setting.prod import MONGODB_HOST, MONGODB_DB_NAME, MONGODB_USER, MONGODB_PASSWORD
else:
    from Server.setting.dev import MONGODB_HOST, MONGODB_DB_NAME, MONGODB_USER, MONGODB_PASSWORD

connect(
    db=MONGODB_DB_NAME,
    username=MONGODB_USER,
    password=MONGODB_PASSWORD,
    host=MONGODB_HOST
)

class Friend(EmbeddedDocument):
    user_id = StringField()
    message_id = StringField()

class FriendList(Document):
    user_id = StringField()
    message_id = StringField()
    chinese_name = StringField()
    english_name = StringField()
    photo = StringField()
    job_title = StringField()
    unread_message_number = IntField()
    last_message_time = StringField(required=False)

class Device(EmbeddedDocument):
    ios = StringField(default='')
    android = StringField(default='')

class Flags(EmbeddedDocument):
    pm = IntField()
    marketing = IntField()
    data_analysis = IntField()
    uiux = IntField()
    startup = IntField()
    sales = IntField()
    finance = IntField()
    information_technology = IntField()
    business = IntField()
    other = StringField()

class User(Document):
    user_id = StringField(primary_key=True)
    id_type = StringField()
    token = StringField()
    device = EmbeddedDocumentField(Device)
    chinese_name = StringField()
    english_name = StringField()
    photo = StringField(required=False)
    gender = StringField()
    company = StringField()
    job_title = StringField()
    career_year = IntField()
    job_type = ListField(StringField())
    industry_type = StringField()
    bachelor_school = StringField()
    bachelor_major = StringField()
    master_school = StringField()
    master_major = StringField()
    phone_number = StringField(required=False)
    email = EmailField(required=False)
    introduction = StringField(required=False)
    satisfied_project = StringField(required=False)
    cooperation_things = StringField(required=False)
    professional_field = EmbeddedDocumentField(Flags)
    interest_issue = EmbeddedDocumentField(Flags)
    friends = ListField(EmbeddedDocumentField(Friend), required=False)
    draw_card_status = StringField()
    card_drawer = StringField(default='')
    card_drawer_of_next_day = StringField()
    # friend_invitation = BooleanField(default=None)
    linked_code = StringField(required=False)
    invitation_code = ListField(StringField(), required=False)

    def __str__(self):
        return self.user_id

class MessageContent(EmbeddedDocument):
    id = IntField()
    user_id = StringField()
    time = StringField()
    content = StringField()
    is_read = BooleanField(default=False)

class UserString(EmbeddedDocument):
    user_1 = StringField()
    user_2 = StringField()

class UserBoolaen(EmbeddedDocument):
    user_1 = BooleanField(default=True)
    user_2 = BooleanField(default=True)

class User_last_read_message(EmbeddedDocument):
    user_1 = IntField(default=0)
    user_2 = IntField(default=0)

class Message(Document):
    message_id = StringField(primary_key=True)
    user_id = EmbeddedDocumentField(UserString)
    notification = EmbeddedDocumentField(UserBoolaen)
    last_read_message = EmbeddedDocumentField(User_last_read_message, default={"user_1": 0, "user_2": 0})
    messages = ListField(EmbeddedDocumentField(MessageContent), default=[])

class Invitation_code(Document):
    invitation_code = StringField()
    linked_code = StringField()
    is_used = BooleanField(default=False)

class Typeform_applicant(Document):
    token = StringField(primary_key=True)
    language = StringField()
    chinese_name = StringField()
    english_name = StringField()
    gender = StringField()
    phone_number = StringField()
    email = EmailField()
    career_len = IntField()
    company = StringField()
    job_title = StringField()
    job_type = ListField(StringField())
    industry_type = StringField()
    college_name = StringField()
    college_major = StringField()
    grad_name = StringField(required=False)
    grad_major = StringField(required=False)
    satisfied_project = StringField(required=False)
    cooperation_things = StringField(required=False)
    pm_i_rating = IntField()
    market_i_rating = IntField()
    ds_i_rating = IntField()
    uiux_i_rating = IntField()
    startup_i_rating = IntField()
    sales_i_rating = IntField()
    finance_i_rating = IntField()
    it_i_rating = IntField()
    business_i_rating = IntField()
    other_i_rating = StringField(required=False)
    pm_rating = IntField()
    market_rating = IntField()
    ds_rating = IntField()
    uiux_rating = IntField()
    startup_rating = IntField()
    sales_rating = IntField()
    finance_rating = IntField()
    it_rating = IntField()
    business_rating = IntField(required=False)
    other_rating = StringField(required=False)

class Applicant(Document):
    token = StringField(primary_key=True)
    language = StringField()
    chinese_name = StringField()
    english_name = StringField()
    gender = StringField()
    phone_number = StringField()
    email = EmailField()
    career_len = IntField()
    company = StringField()
    job_title = StringField()
    job_type = ListField(StringField())
    industry_type = StringField()
    college_name = StringField()
    college_major = StringField()
    grad_name = StringField(required=False)
    grad_major = StringField(required=False)
    satisfied_project = StringField(required=False)
    cooperation_things = StringField(required=False)
    pm_i_rating = IntField()
    market_i_rating = IntField()
    ds_i_rating = IntField()
    uiux_i_rating = IntField()
    startup_i_rating = IntField()
    sales_i_rating = IntField()
    finance_i_rating = IntField()
    it_i_rating = IntField()
    business_i_rating = IntField()
    other＿i_rating = StringField(required=False)
    pm_rating = IntField()
    market_rating = IntField()
    ds_rating = IntField()
    uiux_rating = IntField()
    startup_rating = IntField()
    sales_rating = IntField()
    finance_rating = IntField()
    it_rating = IntField()
    business_rating = IntField()
    other_rating = StringField(required=False)
    linked_code = StringField()
    invitation_code = ListField(StringField())

class MatchAlgorithmScore(Document):
    user_id = StringField(primary_key=True)
    pm_profession_score = IntField()
    marketing_profession_score = IntField()
    data_analysis_profession_score = IntField()
    uiux_profession_score = IntField()
    startup_profession_score = IntField()
    sales_profession_score = IntField()
    finance_profession_score = IntField()
    information_technology_profession_score = IntField()
    business_profession_score = IntField()
    pm_interest_score = IntField()
    marketing_interest_score = IntField()
    data_analysis_interest_score = IntField()
    uiux_interest_score = IntField()
    startup_interest_score = IntField()
    sales_interest_score = IntField()
    finance_interest_score = IntField()
    information_technology_interest_score = IntField()
    business_interest_score = IntField()
    job_type_score = IntField()
    industry_type_score = IntField()

class Feedback_beta(Document):
    user_id = StringField(primary_key=True)
    score = IntField()