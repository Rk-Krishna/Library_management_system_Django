"""
URL configuration for LBM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from Library_app import views
from django.contrib.auth.views import LogoutView,LoginView

urlpatterns = [
   path('admin/', admin.site.urls),
   path('',views.index  ,name="library_app"),
   path('student_register/',views.StudentCreateView.as_view(),name="student_register"),
   path('student_profile/',views.student_profile,name="student_profile"),
   path('staff_profile/',views.staff_profile,name="staff_profile"),
   path('student_edit_profile/',views.student_edit_profile,name="student_edit_profile"),
   path('staff_edit_profile/',views.staff_edit_profile,name="staff_edit_profile"),
   path('staff_registration/',views.StaffCreateView.as_view(),name="staff_registration"),
   path('approve_list/', views.admin_approve_list, name='admin_approve_list'),
   path('logout/',views.logout_custom,name='logout'), 
   path('login/',views.login_view,name='login'),
   path('admin_approve_staff/<int:user_id>/',views.admin_approve_staff,name='admin_approve_staff'),
   path('admin_approve_list/',views.admin_approve_list,name='admin_approve_list'),
   path('dashboard',views.dashboard,name="dashboard"),
   path('admin_dashboard',views.admin_dashboard,name="admin_dashboard"),
   path('create_book',views.create_book,name="create_book"),
   path('view_book',views.view_book,name="view_book"),
   path('edit_book/<int:id>/',views.edit_book,name="edit_book"),
   path('delete_book/<int:id>/',views.delete_book,name="delete_book"),
   path('view_student',views.view_student,name="view_student"),
   path('view_staff',views.view_staff,name="view_staff"),
   path('delete_student/<int:id>/',views.delete_student,name="delete_student"),
   path('delete_staff/<int:id>/',views.delete_staff,name="delete_staff"),
   path('staff_issue_book',views.issue_book_to_staff,name="staff_issue_book"),
   path('view_staff_books',views.view_staff_issued_book,name="view_staff_books"),
    path('student_issue_book',views.issue_book_to_student,name="student_issue_book"),
   path('view_student_books',views.view_student_issued_book,name="view_student_books"),
   path('student_return_book/<str:id>/<int:isbn>',views.student_return_book,name="student_return_book"),
    path('staff_return_book/<str:id>/<int:isbn>',views.staff_return_book,name="staff_return_book"),
    path('fines',views.fine,name="fines"),
]
    