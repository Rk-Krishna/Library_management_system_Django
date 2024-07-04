from django import forms
from .models import Book,staffIssuedBook,Staff,Student,studentIssuedBook
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

from django import forms
from django.contrib.auth.forms import UserCreationForm
DEPARTMENT_CHOICES = [
    ('CS', 'Computer Science'),
    ('EEE', 'Electrical Engineering'),
    ('MECH', 'Mechanical Engineering'),
    ('CiVIL', 'Civil Engineering'),
    ('BioTech', 'Biotechnology'),
]
BRANCHES_BY_DEPT = {
    'CS': [
        ('CSE', 'Computer Science and Engineering'),
        ('CSE-DS', 'Computer Science and Engineering with Data Science'),
        ('CSE-AI', 'Computer Science and Engineering with Artificial Intelligence'),
    ],
    'EEE': [
        ('EEE', 'Electrical Engineering'),
        ('EEE-PE', 'Electrical Engineering with Power Engineering'),
        ('EEE-CE', 'Electrical Engineering with Control Engineering'),
    ],
    'MECH': [
        ('ME', 'Mechanical Engineering'),
        ('ME-TE', 'Mechanical Engineering with Thermal Engineering'),
        ('ME-DE', 'Mechanical Engineering with Design Engineering'),
    ],
    'CiVIL': [
        ('CE', 'Civil Engineering'),
        ('CE-SE', 'Civil Engineering with Structural Engineering'),
        ('CE-TE', 'Civil Engineering with Transportation Engineering'),
    ],
    'BioTech': [
        ('BT', 'Biotechnology'),
        ('BT-BE', 'Biotechnology with Bioengineering'),
        ('BT-BI', 'Biotechnology with Bioinformatics'),
    ],
}
class BookForm(forms.ModelForm):
    class Meta:
        model=Book
        fields=(
            'name',
            'author',
            'isbn',
            'category',
            'publication',
        )

User=get_user_model()
class StudentForm(UserCreationForm):
    phone = forms.IntegerField(max_value=9999999999)
    dept = forms.ChoiceField(choices=DEPARTMENT_CHOICES)
    branch = forms.ChoiceField(choices=BRANCHES_BY_DEPT)
    register_no = forms.CharField(max_length=10)

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2'
        )


    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Student.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
                dept=self.cleaned_data['dept'],
                branch=self.cleaned_data['branch'],
                register_no=self.cleaned_data['register_no'],
            )
        return user
    
class StaffForm(UserCreationForm):
    phone = forms.IntegerField(max_value=9999999999)
    dept = forms.ChoiceField(choices=DEPARTMENT_CHOICES)
    branch = forms.ChoiceField(choices=BRANCHES_BY_DEPT)
    staff_id = forms.CharField(max_length=10)

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Student.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
                dept=self.cleaned_data['dept'],
                branch=self.cleaned_data['branch'],
                staff_id=self.cleaned_data['staff_id'],
            )
        return user
class BookChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.name} [{obj.isbn}]'
class StaffChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.user.username} [{obj.staff_id}]'
class StudentChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.user.username} [{obj.register_no}]'

class staffIssuedBookForm(forms.ModelForm):
    staff_id = StaffChoiceField(queryset=Staff.objects.all(), label="Staff ID")
    book = BookChoiceField(queryset=Book.objects.all(), label="Book")

    class Meta:
        model = staffIssuedBook
        fields = ['staff_id', 'book']

class studentIssuedBookForm(forms.ModelForm):
    student_register_no = StudentChoiceField(queryset=Student.objects.all(), label="Student ID")
    book = BookChoiceField(queryset=Book.objects.all(), label="Book")

    class Meta:
        model = studentIssuedBook
        fields = ['student_register_no', 'book']

