from datetime import date
from decimal import Decimal
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import CreateView, DetailView
from .forms import BookForm, StudentForm, StaffForm,staffIssuedBookForm,studentIssuedBookForm
from django.urls import reverse
from django.contrib import messages
from .models import Book, User, Student, Staff,staffIssuedBook,studentIssuedBook
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm



# Create your views here.
def index(request):
    return render(request,'home.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)   
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user.is_superuser:
                login(request,user)
                return redirect('admin_dashboard')
            elif user is not None and user.is_student or user.is_staff :
                login(request,user)
                return redirect('dashboard')
            
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_custom(request):
    logout(request)
    return redirect('library_app')

def admin_dashboard(request):
    return render(request,'admin_dashboard.html')

def dashboard(request):
    return render(request,'dashboard.html')

class BookCreateView(CreateView):
    template_name="create_book.html"
    form_class=BookForm
    def get_success_url(self):
        messages.info('Book has been CreatedSuccessfully')
        book=Book.objects.all()
        return reverse('view_book',{'books':book})
    
class StudentCreateView(CreateView):
      template_name='student_register.html'
      form_class=StudentForm
      def form_valid(self, form):
        user = form.save(commit=False)
        user.is_student = True
        user.save()
        return super().form_valid(form)
      def get_success_url(self):
        return reverse('login')
    

def student_profile(request):
    return render(request,'student_profile.html')  



def staff_profile(request):
    return render(request,'staff_profile.html')  


def student_edit_profile(request):
     student = Student.objects.get(user=request.user)

     if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        dept = request.POST['dept']
        branch=request.POST['branch_name']
        register_no = request.POST['register_no']
        student.user.username=username
        student.user.first_name=first_name
        student.user.last_name=last_name
        student.user.email=email
        student.phone=phone
        student.dept=dept
        student.branch=branch
        student.register_no=register_no
        student.user.save()
        student.save()
        return render(request, "student_profile.html")
     else:
        return render(request, "student_edit_profile.html")
     
class StaffCreateView(CreateView):
      template_name='staff_registration.html'
      form_class=StaffForm
      def form_valid(self, form):
        response = super().form_valid(form)
        admin_email = settings.ADMIN_EMAIL
        send_mail(
                subject="New staff Signup",
                message=f"A new staff has signed up. Please review and approve: {self.request.build_absolute_uri(reverse('admin_approve_staff', args=[form.instance.id]))}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[admin_email],
            )
        return response
      def get_success_url(self):
        return reverse('login')
      
def admin_approve_staff(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        user.is_staff = True
        user.save()
        send_mail(
            subject="Your account has been approved",
            message="Your account has been approved by the admin. You can now log in by giving forgot password and change according to you .",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        
        return redirect('admin_approve_list')
    context = {
        "user": user
    }
    return render(request, 'admin_approve_staff.html', context)

def admin_approve_list(request):
    users = User.objects.filter(is_staff=False,is_student=False)
    context = {
        "users": users
    }
    return render(request, 'admin_approve_list.html', context)

def staff_registration(request):
    form = StaffForm()
    if request.method == "POST":
        form = StaffForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            dept = form.cleaned_data['dept']
            branch = request.POST.get('branch_name', '') 
            staff_id = form.cleaned_data['staff_id']
            password = form.cleaned_data['password1']
            confirm_password = form.cleaned_data['password2']

            if password != confirm_password:
                messages.info(request, 'Both the passwords should be same')
                return render(request, "staff_registration.html", {'form': form})
            

            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            staff = Staff.objects.create(user=user, phone=phone, dept=dept, staff_id=staff_id, branch=branch)
            user.save()
            staff.save()

            admin_email = settings.ADMIN_EMAIL
            send_mail(
                subject="New Staff registered",
                message=f"A new staff has signed up. Please review and approve: {request.build_absolute_uri(reverse('admin_approve_staff', args=[user.id]))}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[admin_email],
            )
            return redirect("login")
        else:
            messages.error(request, "Invalid form submission.")
    return render(request, "staff_registration.html", {'form': form})
def create_book(request):
    if request.method == "POST":
        name = request.POST['name']
        author = request.POST['author']
        isbn = request.POST['isbn']
        category = request.POST['category']
        publication=request.POST['publication']

        books = Book.objects.create(name=name, author=author, isbn=isbn, category=category,publication=publication)
        books.save()
        
        return redirect("view_book")
    return render(request,'create_book.html')

def view_book(request):
    books = Book.objects.all()
    return render(request,'view_book.html',{'books':books})
def view_student(request):
    students = Student.objects.all()
    return render(request,'view_students.html',{'students':students})
def view_staff(request):
    staffs = Staff.objects.all()
    return render(request,'view_staff.html',{'staffs':staffs})

def delete_book(request,id):
    books = Book.objects.get(id=id)
    books.delete()
    return redirect("view_book")
    
def delete_staff(request,id):
    
    staffs = Staff.objects.get(id=id)
    staffs.delete()
    return redirect("view_staff")
    
def delete_student(request,id):
    student = Student.objects.get(id=id)
    student.delete()
    return redirect("view_student")
def edit_book(request,id):
    books = Book.objects.get(id=id)
    if request.method == "POST":
        book=Book.objects.all()
        books.name = request.POST['name']
        books.author = request.POST['author']
        books.isbn = request.POST['isbn']
        books.category = request.POST['category']
        books.publication = request.POST['publication']
        books.save()
        return render(request,'view_book.html',{'books':book})
    return render(request,'edit_book.html',{'book':books})

def staff_edit_profile(request):
    staff = Staff.objects.get(user=request.user)

    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        dept = request.POST['dept']
        branch=request.POST['branch_name']
        staff.user.username=username
        staff.user.first_name=first_name
        staff.user.last_name=last_name
        staff.user.email=email
        staff.phone=phone
        staff.dept=dept
        staff.branch=branch
        staff.user.save()
        staff.save()
        return render(request, "staff_profile.html")
    else:
        return render(request, "staff_edit_profile.html")
    
def issue_book_to_staff(request):
    if request.method == 'POST':
        form = staffIssuedBookForm(request.POST)
        if form.is_valid():
            selected_staff= form.cleaned_data['staff_id']
            staff_id=selected_staff.staff_id
            selected_book = form.cleaned_data['book']
            book_name = selected_book.name 
            book=staffIssuedBook.objects.filter(staff_id=staff_id).count
            if(book >4):
                messages.info(request,'one staff cannot take morethan 4 book')
                return render(request, 'issue_book_to_staff.html')
            else:
                staffIssuedBook.objects.create(staff_id=staff_id, book=book_name)
                return redirect('admin_dashboard')  
    else:
        form = staffIssuedBookForm()
    return render(request, 'staff_issue_book.html', {'form': form})

def view_staff_issued_book(request):
    if(request.user.is_staff and not request.user.is_superuser):
        issuedBooks=staffIssuedBook.objects.filter(staff_id=request.user.staff.staff_id)
    else:
        issuedBooks = staffIssuedBook.objects.all()
    
    details = []
    for issuedBook in issuedBooks:                                      
      
        try:
        
            book = Book.objects.get(name=issuedBook.book)
            staff = Staff.objects.get(staff_id=issuedBook.staff_id)
            detail = (
                    staff.user.username, 
                    staff.staff_id,
                     book.name,
                    book.isbn,
                    issuedBook.issued_date,
                    issuedBook.expiry_date,
                    issuedBook.fine
                    )
            if request.user.is_superuser:
                template_name = 'admin_dashboard.html'
            else:
                template_name = 'dashboard.html'
            details.append(detail)
        except Book.DoesNotExist:
            print(f"Book with ISBN {issuedBook.book} does not exist.")
        except Staff.DoesNotExist:
            print(f"Staff with ID {issuedBook.staff_id} does not exist.")

    return render(request, "view_staff_issued_books.html", {'issuedBooks': issuedBooks, 'details': details,'template_name':template_name})

def issue_book_to_student(request):
    if request.method == 'POST':
        form = studentIssuedBookForm(request.POST)
        if form.is_valid():
            selected_student= form.cleaned_data['student_register_no']
            register_no=selected_student.register_no
            selected_book = form.cleaned_data['book']
            book_name = selected_book.name  
            book=Book.objects.filter(name=book_name).first()
            studentIssuedBook.objects.create(student_register_no=register_no, book=book_name,isbn=book.isbn)
            return redirect('admin_dashboard')  
    else:
        form = studentIssuedBookForm()
    return render(request, 'student_issue_book.html', {'form': form})

def view_student_issued_book(request):
    if(request.user.is_student):
        issuedBooks=studentIssuedBook.objects.filter(student_register_no=request.user.student.register_no)
    else:
        issuedBooks = studentIssuedBook.objects.all()
    
    details = []
    for issuedBook in issuedBooks:
        try:
            
            book = Book.objects.get(name=issuedBook.book)
            student = Student.objects.get(register_no=issuedBook.student_register_no)
            detail = (
                student.user.username, 
                student.register_no,
                book.name,
                book.isbn,
                issuedBook.issued_date,
                issuedBook.expiry_date,
                issuedBook.fine
            )
            details.append(detail)
            if request.user.is_superuser:
                 template_name = 'admin_dashboard.html'
            elif hasattr(request.user, 'student'):
                template_name = 'dashboard.html'
            else:
                template_name = 'base.html'

        except Book.DoesNotExist:
            print(f"Book with ISBN {issuedBook.book} does not exist.")
        except Student.DoesNotExist:
            print(f"student with ID {issuedBook.student_id} does not exist.")
    return render(request, "view_student_issued_books.html", {'issuedBooks': issuedBooks, 'details': details,'template_name':template_name})

def student_return_book(request, id, isbn):
    book = studentIssuedBook.objects.filter(student_register_no=id, isbn=isbn).first()
    book.delete()
    return redirect(reverse('view_student_books'))

def staff_return_book(request,id,isbn):
    book=staffIssuedBook.objects.filter(staff_id=id,isbn=isbn)
    book.delete()
    return redirect('view_staff_books')

def fine(request):
    if(request.user.is_student):
        fines=studentIssuedBook.objects.filter(student_register_no=request.user.student.register_no)
    elif(request.user.is_staff) and not (request.user.is_superuser):
        fines=staffIssuedBook.objects.filter(staff_id=request.user.staff.staff_id)
    fine_amount=0.0
    for fines in fines:
        fine_amount=Decimal(fine_amount)+Decimal(fines.fine)
    return render(request,"fines.html",{'fine_amount':fine_amount})
