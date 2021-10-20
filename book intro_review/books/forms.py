from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    title = forms.CharField(
        label='책 제목',
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '제목을 적어주세요.',
                'maxlength': 100
            }
        ),
        error_messages = {
        'required':'제목이 비었습니다.',
            }
    )
    
    author = forms.CharField(
        label='저자',
        widget = forms.TextInput(
            attrs={
                'class': 'my-author form-control',
                'placeholder': '저자를 적어주세요.',
                'maxlength': 100
            }
        ), 
        error_messages = {
        'required':'저자가 비었습니다.'
            }
    )
    description = forms.CharField(
        label='내용',
        widget = forms.Textarea(
            attrs={
                'class': 'my-description form-control',
                'placeholder': '내용을 적어주세요.',
                'rows':10,
                'cols': 50,
            }
        ),
         error_messages = {
        'required':'내용이 비었습니다.'
            }
    )

    class Meta:
        model = Book
        fields = '__all__'