from django.test import TestCase

# Create your tests here.
from django.contrib.auth import authenticate

user = authenticate(username='staff', password='KBD45dkak00@#')
if user is not None:
    print(f"Authenticated user: {user.username}")
    print(f"is_staff: {user.is_staff}")
    print(f"is_student: {user.is_student}")
else:
    print("Authentication failed")
