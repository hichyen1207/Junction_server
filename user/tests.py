import json
import boto3
import os
import unittest
from django.test import Client
from .models import User

if os.environ['DJANGO_SETTINGS_MODULE'] == 'Server.setting.prod':
    from Server.setting.prod import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_NAME, AWS_S3_REGION
else:
    from Server.setting.dev import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_NAME, AWS_S3_REGION

class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def userDetail(self):
        response = self.client.get('/user/testuser01/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def userRegister(self):
        body = {
            "user_id": "testCat1",
            "id_type": "facebook",
            "chinese_name": "貓",
            "english_name": "Cat",
            "gender": "女生",
            "photo": "",
            "company": "Junction",
            "job_title": "CEO",
            "career_year": 2,
            "job_type": ["產品管理"],
            "industry_type": "消費性產品",
            "bachelor_school": "NCCU",
            "bachelor_major": "NCCU",
            "master_school": "NCCU",
            "master_major": "NCCU",
            "phone_number": "0987654321",
            "email": "aaa@gmail.com",
            "introduction": "hihi",
            "satisfied_project": "satisfied_project",
            "cooperation_things": "cooperation_things",
            "linked_code": "Harrison0000",
            "pm_i_rating": 2,
            "marketing_i_rating": 3,
            "data_analysis_i_rating": 4,
            "uiux_i_rating": 5,
            "startup_i_rating": 4,
            "sales_i_rating": 3,
            "finance_i_rating": 2,
            "information_technology_i_rating": 1,
            "business_i_rating": 0,
            "other_i_rating": "",
            "pm_rating": 2,
            "marketing_rating": 1,
            "data_analysis_rating": 3,
            "uiux_rating": 4,
            "startup_rating": 5,
            "sales_rating": 4,
            "finance_rating": 3,
            "information_technology_rating": 2,
            "business_rating": 1,
            "other_rating": ""
        }
        response = self.client.post('/user/', json.dumps(body), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        status = response.status_code

        if status == 200:
            User.objects(user_id='testCat1').delete()

            s3 = boto3.resource('s3', AWS_S3_REGION,
                                aws_access_key_id=AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
            bucket = AWS_BUCKET_NAME
            s3.Object(bucket, 'images/user/testCat1.jpg').delete()