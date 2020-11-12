from django.shortcuts import render
from catalog.models import Book, Author, Genre, Language, BookInstance


# Create your views here.

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    numberOfBooks = Book.objects.all().count()
    numberOfInstances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    numberOfInstancesAvailable = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    numberOfAuthors = Author.objects.count()

    numberOfGenres = Genre.objects.count()

    # Number of visits to this view, as counted in the session variable.
    numberOfVisits = request.session.get('numberOfVisits', 0)
    request.session['numberOfVisits'] = numberOfVisits + 1

    context = {
        'noOfBooks': numberOfBooks,
        'noOfInstances': numberOfInstances,
        'noOfInstAvailable': numberOfInstancesAvailable,
        'noOfAuthors': numberOfAuthors,
        'noOfGenres': numberOfGenres,
        'noOfVisits': numberOfVisits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


from django.views import generic


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author


from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class BorrowedBooksListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance

    permission_required = 'catalog.can_mark_returned'

    template_name = 'catalog/borrowed_books_list.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


