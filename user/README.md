# User App

## models.py

> The models of the database. In this file, define the structure of the database.
>
1. JobExperience:
 
    The model in the **User** model. There are company, job_title,
    job_starting_date, job_ending_date, and company_logo in this models.
   
2. User:

    The main model of the user app. There are `linkedin_id`, `name, photo`,
    `gender`, `job_experience`, `professional_field`, `educational_background`, `phone_number`,
    `email`, `introduction`, `satisfied_project`, `cooperation_things`, `interest_issue`,
    `friends`, `card_drawer`, and `friend_invitation` in the model.


## views.py

> The view of the server. In this file, implement the GET, POST, PUT function and 
  response the result of Json format.
> 
1. CheckUser:

    * GET:
    
        Check if the given linkedin id is already register or not. Response a `boolean`. 

2. UserList:

    * POST:
    
        Receive the POST request and create a new user into the database.  
        
3. UserDetail:

    * GET:
    
        Receive a request with a linkedin id, and response the user detail of that user.
        
    * PUT:
    
        Update the user information from the request.
        
4. FriendList:

    * GET:
    
        Receive a request with a linkedin id, and response the friend list of that user.
        
5. FriendInvitation:

    * PUT:
    
        when user press the invitation button, sending a friend request. this function 
        would check if the two users both send the friend requet or not. If both of them
        send the friend, they will becaome friend, or the user will set `friend_invitation=True`
        and wait for another user sending the friend request.
        
6. CardDetail:

    * GET:
    
        Receive a request with a linkedin id, and response the card datail of that user.
    

## serializers.py

> Define the serializers of the rest framework.
>

1. UserSerializer:
    
    The serializer of the user information, and return all the items.
    
2. FriendSerializer:

    The serializer of the friend information, and return `linkedin_id`, `name`, `gender`, `photo`,
    `job_experience`, `professional_field`, `educational_background`, `email`, `phone_number`,
    `introduction`, `interest_issue`, `satisfied_project`, `cooperation_things`


## cardDrawer.py

> The function `drawer_card()` would match every two users into a pair.