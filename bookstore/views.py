from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Book, Author, Category
from .forms import BookForm, CategoryForm, AuthorForm
from django.db.models import Count
from django.db.models.functions import ExtractYear
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def book_chart_data(request):
    # Extract the year from the publication_date and count the number of books per year
    books_per_year = (
        Book.objects
        .annotate(year=ExtractYear('publication_date'))  # Extract the year from the date
        .values('year')  # Group by the extracted year
        .annotate(book_count=Count('id'))  # Count the number of books per year
        .order_by('year')  # Order by year
    )

    # Prepare the data for Chart.js
    labels = [entry['year'] for entry in books_per_year]  # X-axis: years
    data = [entry['book_count'] for entry in books_per_year]  # Y-axis: number of books

    # Return the data as JSON
    return JsonResponse({
        'labels': labels,  # Years
        'data': data  # Number of books per year
    })
    
# Create your views here.
def category_chart_data(request):
    # Count the number of books in each category
    categories = Category.objects.annotate(book_count=Count('book'))  # Assumes 'book' is the related name for the ForeignKey in the Book model

    # Prepare the data for Chart.js
    labels = [category.name for category in categories]  # Category names as labels
    data = [category.book_count for category in categories]  # Number of books in each category

    # Return the data as JSON
    return JsonResponse({
        'labels': labels,  # Category names
        'data': data  # Number of books in each category
    })
    
# Create your views here.
def author_chart_data(request):
    # Count the number of books for each author
    authors = Author.objects.annotate(book_count=Count('books'))  # Assumes 'books' is the related name for the ForeignKey

    # Prepare the data for Chart.js
    labels = [author.name for author in authors]  # Author names as labels
    data = [author.book_count for author in authors]  # Number of books for each author

    # Return the data as JSON
    return JsonResponse({
        'labels': labels,  # Author names
        'data': data  # Number of books per author
    })
    
# Optional: You can customize the login template
class CustomLoginView(LoginView):
    template_name = 'login.html'  # Custom template for login page
    
class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'admin/layout/dashboard.html')

# Book CRUD Views
class BookListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        authors = Author.objects.all()
        categories = Category.objects.all()
        return render(request, 'admin/layout/book_list.html', {'books': books, 'authors': authors, 'categories': categories})

class BookCRUDView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # Handle book creation and updating
        book_id = request.POST.get('bookId')
        
        # If there's a book_id, this is an update
        if book_id:
            book = get_object_or_404(Book, id=book_id)
            form = BookForm(request.POST, instance=book)
        else:
            # Otherwise, we're creating a new book
            form = BookForm(request.POST)
        
        if form.is_valid():
            book = form.save()
            self.send_author_email(book)
            
            return JsonResponse({'success': True, 'id': book.id, 'title': book.title})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    def send_author_email(self, book):
        """
        Sends an email notification to the author when their book is successfully created or updated.
        """
        subject = 'Your Book Has Been Published'
        message = f'Dear {book.author.name},\n\nYour book "{book.title}" has been successfully published!\n\nBest regards,\nYour Bookstore Team'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [book.author.email]  # Send to the author's email

        # Send the email
        send_mail(subject, message, from_email, recipient_list)
        
    def delete(self, request, *args, **kwargs):
        try:
            # Get the book ID from the request body and delete the book
            book_id = request.GET.get('bookId')
            if not book_id:
                return JsonResponse({'success': False, 'error': 'No book ID provided'}, status=400)
            book = get_object_or_404(Book, id=book_id)
            book.delete()
            return JsonResponse({'success': True})
        
        except Exception as e:
            return HttpResponseBadRequest(f"Error: {str(e)}")

    def get(self, request, *args, **kwargs):
        # Optional: To handle GET requests for fetching book data (if needed)
        return HttpResponseBadRequest("Invalid method for this endpoint")

# Category CRUD
class CategoryListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        return render(request, 'admin/layout/category_list.html', {'categories': categories})

class CategoryCRUDView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # Handle category creation and updating
        category_id = request.POST.get('categoryId')

        if category_id:
            category = get_object_or_404(Category, id=category_id)
            form = CategoryForm(request.POST, instance=category)
        else:
            form = CategoryForm(request.POST)
        
        if form.is_valid():
            category = form.save()
            return JsonResponse({'success': True, 'id': category.id, 'name': category.name})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    def delete(self, request, *args, **kwargs):
        try:
            # Get the category ID from the request body
            category_id = request.GET.get('categoryId') 
            if not category_id:
                return JsonResponse({'success': False, 'error': 'No category ID provided'}, status=400)

            category = get_object_or_404(Category, id=category_id)
            category.delete()

            # Return a success response
            return JsonResponse({'success': True})
        
        except Exception as e:
            return HttpResponseBadRequest(f"Error: {str(e)}")

# Author CRUD
class AuthorListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            # Attempt to fetch authors
            authors = Author.objects.all()
            return render(request, 'admin/layout/author_list.html', {'authors': authors})
        except Exception as e:
            # Handle the exception
            print(f"Error occurred: {e}")
        finally:
            # This block runs regardless of whether an exception occurred or not
            print("Cleaning up")

        

class AuthorCRUDView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        author_id = request.GET.get('authorId')
        if author_id:
            author = get_object_or_404(Author, id=author_id)
            form = AuthorForm(request.POST, instance=author)
        else:
            form = AuthorForm(request.POST)
        
        if form.is_valid():
            author = form.save()
            return JsonResponse({'success': True, 'id': author.id, 'name': author.name, 'bio': author.bio, 'email': author.email})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
        
    def delete(self, request, *args, **kwargs):
        try:
            # Get the ID of the author to delete from the request body
            author_id = request.GET.get('authorId')
            if not author_id:
                return JsonResponse({'success': False, 'error': 'No author ID provided'}, status=400)
            # Ensure the author exists
            author = get_object_or_404(Author, id=author_id)
            
            # Delete the author
            author.delete()

            # Return a success response
            return JsonResponse({'success': True})
        except Exception as e:
            # Handle the exception
            print(f"Error occurred: {e}")
        finally:
            # This block runs regardless of whether an exception occurred or not
            print("Cleaning up")
            
        
