from  user_authentication import user_auth 

status = user_auth.create_user("Default", "password", "manager")

if not status:
    print("Default User Creation Failed")
else:
    print("Created Default User! | Username: Default | Pass = password | role = manager")
