# Junction Server
> This is the server API document of Junction app.

## Information

* python 3.6
* django 2.0.2
* mongoDB & mLab
* AWS EC2 Ubuntu

**framework:**

* Django 2.0.2
* mongoengine 0.15.0
* rest_framework 0.1.0
* rest_frame_mongoengine 3.3.1
* Celery 4.1.0
* channels 2.0.2
* channels-redis 2.1.0
* boto3 1.6.16
* django-ses 0.8.5
* apns2 0.3.0
* websocket-client 0.47.0



## API Document

#### http://server/

---------

### Table
#### 1. [Create User API](#create-user)
#### 2. [Check Invitation Code API](#check-invitation-code)
#### 3. [User Detail API](#user-detail)
#### 4. [Update User Information API](#update-user-information)
#### 5. [Friend List API](#friend-list)
#### 6. [Friend Invitation API](#friend-invitation)
#### 7. [Draw Card Status API](#is-draw-card)
#### 8. [Update Draw Card Status API](#update-is-draw-card)
#### 9. [Card Detail API](#card-detail)
#### 10. [Get Invitation Code API](#get-invitation-code)
#### 11. [Message Detail API](#message-detail)
#### 12. [Read Message API](#read-message)
#### 13. [User Report API](#user-report)
#### 14. [Device Setting API](#device-setting)
#### 15. [Send Message: WebSocket API](#send-message-websocket)
#### 16. [Friend List: WebSocket API](#friend-list-websocket)
#### 17. [Create Applicant API](#create-applicant)
#### 18. [Check Applicant API](#check-applicant)
#### 19. [Applicant Detail API](#applicant-detail)
#### 20. [Push Notification Setting API](#push-notification-setting)
#### 21. [Feedback Beta API](#feedback-beta)

---------

* ### User

### check user
> Check if user is already member or not
>
**GET:** http://server/checkUser/<user_id>/

**Response**

    {
	    "user_exist": boolean
	}

---------

### Create User
> Create a new user
>
**POST:** http://server/user/

**Parameter**

    {
        "user_id": string,
        "id_type": string,
        "chinese_name": string,
        "english_name": string,
        "gender": string,
        "photo": string,
        "company": string,
        "job_title": string,
        "career_year": int,
        "job_type": [string, string],
        "industry_type": string,
        "bachelor_school": string,
        "bachelor_major": string,
        "master_school": string,
        "master_major": string,
        "phone_number": string,
        "email": string(email),
        "introduction": string,
        "satisfied_project": string,
        "cooperation_things": string,
        "linked_code": string,
        
        "pm_i_rating": int,
        "marketing_i_rating": int,
        "data_analysis_i_rating": int,
        "uiux_i_rating": int,
        "startup_i_rating": int,
        "sales_i_rating": int,
        "finance_i_rating": int,
        "information_technology_i_rating": int,
        "business_i_rating": int,
        "other_i_rating": string,
        
        "pm_rating": int,
        "marketing_rating": int,
        "data_analysis_rating": int,
        "uiux_rating": int,
        "startup_rating": int,
        "sales_rating": int,
        "finance_rating": int,
        "information_technology_rating": int,
        "business_rating": int,
        "other_rating": string,        
    }
	
**Response**

    {	    
        "message": "user insert successfully"
	}

---------

### Check Invitation Code
> check invitation code from user input
>
**GET:** http://serverserver/checkInvitationCode/<invitation_code>/

**Response**
> Exist and the code is not used up:
>
    {
	    "message": "this invitation code is valid"
	}

> Exist but the code is used up:
>    
	status: 500,
	message: "this invitation code is used up"
	

> Does Not Exist:
>    
	status: 404,
	message: "invitation code dos not exist"	

---------

### User Detail
> get the user detail
>
**GET:** http://server/user/<user_id>/

**Response**

    {
        "user_id": string,
        "id_type": string,
        "token": string,
        "chinese_name": string,
        "english_name": string,
        "photo": string,
        "gender": string,
        "company": string,
        "job_title": string,
        "career_year": int,
        "job_type": [string, string],
        "industry_type": string,
        "bachelor_school": string,
        "bachelor_major": string,
        "master_school": string,
        "master_major": string,
        "phone_number": string,
        "email": string,
        "introduction": string,
        "satisfied_project": string,
        "cooperation_things": string,
        "friends": [
            {
                "user_id": string,
                "message_id": string
            }
        ],
        "card_drawer": string,
        "friend_invitation": string or null,
        "linked_code": string,
        "invitation_code": [
            string,
            string,
            string
        ],
        "professional_field": {
            "pm": int,
            "marketing": int,
            "data_analysis": int,
            "uiux": int,
            "startup": int,
            "sales": int,
            "finance": int,
            "information_technology": int,
            "business": int,
            "other": string
        },
        "interest_issue": {
            "pm": int,
            "marketing": int,
            "data_analysis": int,
            "uiux": int,
            "startup": int,
            "sales": int,
            "finance": int,
            "information_technology": int,
            "business": int,
            "other": string
        }
    }

---------

### Update User Information
> update user's information
>
**PUT:** http://server/user/<user_id>/

**Parameter**

    {
        "chinese_name": string,
        "english_name": string,
        "gender": string,
        "photo": string (change: base64, not change: URL, none: 'default'),
        "company": string,
        "job_title": string,
        "career_year": int,
        "job_type": [string, string],
        "industry_type": string,
        "bachelor_school": string,
        "bachelor_major": string,
        "master_school": string,
        "master_major": string,
        "phone_number": string,
        "email": string(email),
        "introduction": string,
        "satisfied_project": string,
        "cooperation_things": string,
        
        "pm_i_rating": int,
        "marketing_i_rating": int,
        "data_analysis_i_rating": int,
        "uiux_i_rating": int,
        "startup_i_rating": int,
        "sales_i_rating": int,
        "finance_i_rating": int,
        "information_technology_i_rating": int,
        "business_i_rating": int,
        "other_i_rating": string,
        
        "pm_rating": int,
        "marketing_rating": int,
        "data_analysis_rating": int,
        "uiux_rating": int,
        "startup_rating": int,
        "sales_rating": int,
        "finance_rating": int,
        "information_technology_rating": int,
        "business_rating": int,
        "other_rating": string,        
    }
	
**Response**

    {	    
        "message": "Update successfully"
	}

---------

### Friend List
>get the user's friend list
>
**GET:** http://server/user/<user_id>/friends/

**Response**

    [
        {
            "user_id": string,
            "message_id": string,
            "chinese_name": string,
            "english_name": string,
            "photo": string,
            "job_title": string,
            "unread_message_number": int,
            "last_message_time": string
        }
    ]

----------

### Friend Invitation
>request the invitation of friend when user push the "add friend" button
>
**PUT:** http://server/inviteFriend/<user_id>/

**Parameter**

    {
	    "message": "invite",
	    "action": "accept/reject"
	}

**Response**
> Success (Accept: Becoming friend):
>
    {	    
	     "message": "these two user become friends!"
	}

> Success (Accept: Not becoming friend):
>
    {	    
	    "message": "waiting for another user accepts the invitation!"
	}

> Success (Reject):
>
    {	    
	    "message": "Reject friend invitation."
	}

> Fail:
>
    status: 500
    message: error message/action

---------

### Draw Card Status
> check if the user has already drawed card or not
>
**GET:** http://server/user/<user_id>/drawCardStatus/

**Response**

    {
        "draw_card_status": 'undraw/draw/accept/reject'
    }
    
---------

### Update Draw Card Status
> update the user's status of is_draw_card after usser draws card
>
**PUT:** http://server/user/<user_id>/drawCardStatus/

**Parameter**

    {
        "message": "draw card"
    }

**Response**
> Success:
>
    {
        "message": "user draw card successfully"
    }

> Fail:
>
    status: 500
    message: error message

---------

### Card Detail
> get the user’s card detail
>
**GET:** http://server/user/<user_id>/card/

**Response**

    {
        "user_id": string,
        "chinese_name": string,
        "english_name": string,
        "photo": string,
        "gender": string,
        "company": string,
        "job_title": string,
        "career_year": int,
        "job_type": [string, string],
        "industry_type": string,
        "bachelor_school": string,
        "bachelor_major": string,
        "master_school": string,
        "master_major": string,
        "phone_number": string,
        "email": string,
        "introduction": string,
        "satisfied_project": string,
        "cooperation_things": string,
        "professional_field": {
            "pm": int,
            "marketing": int,
            "data_analysis": int,
            "uiux": int,
            "startup": int,
            "sales": int,
            "finance": int,
            "information_technology": int,
            "business": int,
            "other": string
        },
        "interest_issue": {
            "pm": int,
            "marketing": int,
            "data_analysis": int,
            "uiux": int,
            "startup": int,
            "sales": int,
            "finance": int,
            "information_technology": int,
            "business": int,
            "other": string
        }
        "draw_card_status": string ("undraw/draw/accept/reject")
    }

---------

### Get Invitation Code
> get invitation code by user id
>
**GET:** http://server/invitationCode/<linked_code>/

**Response**

    [
        {
            "invitation_code": string,
            "is_used": boolean
        },
        {
            "invitation_code": string,
            "is_used": boolean
        },
        {
            "invitation_code": string,
            "is_used": boolean
        }
    ]


---------

* ### Message

### Message Detail
> get message detail by message id
>
**GET:** http://server/message/messageDetail/<message_id>/

**Response**

    {
        "message_id": string,
        "user_id": {
            "user_1": string,
            "user_2": string
        },
        "notification": {
            "user_1": boolean,
            "user_2": boolean
        }
        "messages": [
            {
                "id": int,
                "user_id": string,
                "time": date,
                "content": string,
                "is_read": boolean 
            }
        ]
    }

---------

### Read Message
> read the message by message id and content id
>
**PUT:** http://server/message/readMessage/<message_id>/

**Parameter**

    {
	    "message": "read",
	    "user_id": string (user who reads messages)
	}

**Response**
> Success:
>        
    {        
        "message": "user: <user_id> reads messages."
    }
> Fail:
>
    status: 500
    message: "error message"
    
---------

#### Update Message Notification
> update the notification in the message
>
**PUT:** http://server/message/updateNotification/<message_id>/

**Parameter**

    {
        "user_id": String,
        "notification": boolean
    }
    
**Response**

    {
        "message": "update successfully"
    }

---------

#### User Report
> report the user to report@junction.solutions
>
**PGET:** http://server/report/<user_id>/

**Response**
    
    {
        "message": "report successfully"
    }

---------

* ### Push Notification
### Device Setting
> setting the device id for push notifications
>
**PUT** http://server/user/deviceSetting/<user_id>/

**Parameter**

    {
        "ios": string, (not required)
        "android": string (not required)
    }

**Response**

    {
        "message": "setting is successful"
    }

---------

### Push Notification Setting
> setting for push notification
>
**Custom Payload**
    
    message:
    {
        "type": "message",
        'message_id': string,
        'user_id': string,
        'english_name': string,
        'chinese_name': string,
        'photo': string
    }
    
    card:
    {
        "type": "card"        
    }
    
    becoming friend:
    {
        "type": "friend"        
    }

---------

### Send Message: WebSocket
> send message with WebSocket
>
**WEBSOCKET:** ws://server/message/<message_id>/

**Parameter**

    {
        "user_id": string,
        "time": date,
        "content": string
    }

**Example:**

    socket = new WebSocket("ws://server/message/<message_id>/");

    socket.onmessage = function(message) {
        alert(message.data);
    }

    var message = JSON.stringify({
        "user_id": "testuser01",
        "time": "2018-03-06T00:00:00.000Z",
        "content": "hello"})

    socket.send(message)

---------

### Friend List: WebSocket
>get unread messages and time on friend list page
>
**WEBSOCKET:** ws://server/friendList/<acceptor_user_id>/

**Parameter**

    {
        "user_id": string(sender),
        "time": date,
        "message_id": string
    }

**Response**

    {
        "message_id": string,
        "time": string,
        "unread_message_number": string
    }

---------

## For Web Register Flow

### Create Applicant
> create applicant to database
>
**GET** http://server/applicant/register/<token>/

**Response**

    {        
        "message": "applicant insert successfully."        
    }

---------

### Check Applicant
>check if the invitation code exists or not
>
**GET** http://server/checkApplicant/<linked_code>/

**Response**
    
    {        
        "applicant_exist": true/false,
        "user_exist": true/false
    }

---------

### Applicant Detail
> get the applicant detail by invitation code
>
**GET** http://server/applicant/<linked_code>/

**Response**
    
    {
        "token": string,
        "chinese_name": string,
        "english_name": string,
        "photo": string,
        "gender": string,
        "company": string,
        "job_title": string,
        "career_year": int,
        "job_type": [string, string],
        "industry_type": string,
        "bachelor_school": string,
        "bachelor_major": string,
        "master_school": string,
        "master_major": string,
        "phone_number": string,
        "email": string,
        "introduction": string,
        "satisfied_project": string,
        "cooperation_things": string,
        "linked_code": string,
        "professional_field": {
            "pm": int,
            "marketing": int,
            "data_analysis": int,
            "uiux": int,
            "startup": int,
            "sales": int,
            "finance": int,
            "information_technology": int,
            "business": int,
            "other": string
        },
        "interest_issue": {
            "pm": int,
            "marketing": int,
            "data_analysis": int,
            "uiux": int,
            "startup": int,
            "sales": int,
            "finance": int,
            "information_technology": int,
            "business": int,
            "other": string
        }
    }

---------

## Feedback

### Feedback Beta
> for beta user giving feedback
>
**GET** http://server/feedback/beta/

**Parameter**

    {
        "user_id": String,
        "score": int
    }
    
**Response**

    {
        "message": "scoring successfully"
    }

---------
## Version

### V1.0.1
date: 2018.02.03
* fix POST USER -> add invitation_code & register_with_invitation_code
* fix friend list -> return fields change to: user_id, message_id, user_name, photo, job_title
* add API CheckInvitationCode
* add API MessageDetail
* add API ReadMessage
* add API ReadGroupMessage

--------

### V1.0.2
date: 2018.02.04
* fix User model -> linkedin_id to user_id & id_type, add access_token
* fix Friends model -> user_name to name

-------

### V1.0.3
date: 2018.02.14
* fix create user API document -> add **company_logo** field
* fix user detail API document -> add **job_experience** field and fix other related fields
* fix check invitation code API -> add response when the code is used up

--------

### v1.0.4
date: 2018.02.20
* fix friend invitation API -> add reject friend invitation
* fix the invitation code API -> add left time the GET invitation code
* fix PULL user API -> check user fills up all the fields or not

--------

### v1.0.5
date: 2018.02.23
* fix card detail API -> add friend invutation status

--------

### v1.1.0
date: 2018.03.07
* add send message WebSocket API

--------

### v1.2.0
date: 2018.03.08
* change invitation code model
* change invitation code GET API

--------

### v1.3.0
date: 2018.03.11
* add friend list WebSocket API

--------

### v1.4.0
date: 2018.03.13
* add [web] applicant POST API
* add applicant detail GET API
* add check applicant GET API
* change read message PUT API

--------

### v1.4.1
date: 2018.03.15
* fix message detail -> **user_id** from list to object
* fix GET invitation code API document -> **user_id** to **register_invitation_code**
* fix GET friend list -> **last_unread_message_time** to **last_message_time** 

---------

### v1.4.2
date:2018.03.17
* fix WebSocket Friend list -> **sender_id** to **message_id**

---------

### v1.4.3
date:2018.03.19
* delete tags API

---------

### v2.0.0
date: 2018.04.08
* change user model, applicant model
* add typeform_applicant model
* change GET user API -> change lots of fields, especial **photo** field from base64 to url
* change POST user API -> change lots of parameter fields
* change PUT user API -> change change lots of parameter fields
* add GET register applicant API
* fix GET invitation code API -> parameter from **invitation_code** to **token**
* fix GET checkApplicant API -> parameter from **invitation_code** to  **linked_code**
* fix GET applicant detail API -> parameter from **invitation_code** to  **linked_code**

--------

### v2.0.1
date: 2018.04.10
* fix POST user API -> remove **token** and **invitation_code** fields
* fix GET applicant API -> rating change to **professional_field** and **interest_issue** display
* fix friendList API -> change **name** to **chinese_name** and **englisg_name**
* fix GET invitation_code API -> change parameter **token** to **linked_code**

--------

### v2.0.2
date: 2018.04.15
* fix user model -> **bachelor** to **bachelor_school** and **bachelor_major**, **master** to **master_school** and **master_major**

--------

### v2.0.3
date 2018.04.20
* add Device Setting API

--------

### v2.0.4
date: 2018.04.21
* add push notification Document

--------

### v2.1.0
date: 2018.05.03
* add is_draw_card and update_is_draw_card API

--------

### v2.1.1
date: 2018.05.05
* combine **friend_invitation** and **is_draw_card** to **draw_card_status**
* fix card detail -> **friend_invitation**  to **draw_card_status**
* change **Is Draw Card API** to **Draw Card Status API** -> **draw_card_status**: string

--------

### v2.2.0
date: 2018.05.09
* add User Report API
* add Update Message Notification API
* fix Message Detail API -> add notification field

--------

### v2.3.0
date: 2018.05.15
* add Feedback Beta API

--------

### v2.3.1
date: 2018.05.22
* fix checkApplicant API -> response from **invitation_code_exist** to **applicant_exist** and **user_exist**  