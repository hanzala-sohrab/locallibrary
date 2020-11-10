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

    context = {
        'noOfBooks': numberOfBooks,
        'noOfInstances': numberOfInstances,
        'noOfInstAvailable': numberOfInstancesAvailable,
        'noOfAuthors': numberOfAuthors,
        'noOfGenres': numberOfGenres,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


from django.views import generic


class BookListView(generic.ListView):
    model = Book
    paginate_by = 2


class BookDetailView(generic.DetailView):
    model = Book
