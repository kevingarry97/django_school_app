from django import forms
from .models import Book, Category, Author

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'category', 'publication_date', 'isbn']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']
