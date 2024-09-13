from django import forms
from .models import Book, Author, Category

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'category', 'publication_date', 'isbn']

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'bio']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']