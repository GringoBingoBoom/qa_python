import pytest

from main import BooksCollector


# фикстура BooksCollector()
@pytest.fixture
def collector():
    collector = BooksCollector()
    return collector


class TestBooksCollector:
    # 1. add_new_book Проверка добавления книг
    # тестовые данные 1 книга, 2 книги, дубликат и более 40 символов в названии
    books = [
        ['Вторая жизнь Уве'],  # одна книга
        ['Гордость и предубеждение и зомби',  # две книги
         'Мечтают ли андроиды об электроовцах'],
        ['Вторая жизнь Уве',  # дубликат
         'Вторая жизнь Уве'],
        ['Мечтают ли андроиды об электроовцах Мечтают ли']  # более 40 символов
    ]

    # тестовые данные для проверки результата добавления книг
    books_add_result = [
        {'Вторая жизнь Уве': ''},
        {'Гордость и предубеждение и зомби': '',
         'Мечтают ли андроиды об электроовцах': ''},
        {'Вторая жизнь Уве': ''},  # дубликат
        {}  # более 40 символов
    ]

    # общий список книг и результатов для параметризации
    books_with_results = []
    for i in range(len(books)):
        books_with_results.append([books[i], books_add_result[i]])

    @pytest.mark.parametrize('books, books_result', books_with_results)
    def test_add_new_book_add_one_two_dup_more40simb_books(self, collector, books, books_result):
        # добавляем книги
        for x in books:
            collector.add_new_book(x)
        # проверяем, что добавились книги
        assert collector.books_genre == books_result

    # 2. set_book_genre Проверка установки жанра
    # одна книга с корректным жанром, одна книга с ошибочным жанром
    books_ganres_results = [['Вторая жизнь Уве', 'Комедии', {'Вторая жизнь Уве': 'Комедии'}], # одна книга с корректным жанром
                            ['Гордость и предубеждение и зомби', 'Анимэ', {'Гордость и предубеждение и зомби': ''}]]  # одна книга с ошибочным жанром

    @pytest.mark.parametrize('books, genres, results', books_ganres_results)
    def test_set_book_genre_one_books(self, collector, books, genres, results):
        # добавляем книги и жанр
        collector.add_new_book(books)
        collector.set_book_genre(books, genres)
        # проверяем жанр
        assert collector.books_genre == results

    # 3. get_book_genre Проверка вывода жанра книги по её имени.
    # одна книга с корректным жанром, одна книга с ошибочным жанром
    books_ganres_results = [['Вторая жизнь Уве', 'Комедии', 'Комедии'], # одна книга с корректным жанром
                            ['Гордость и предубеждение и зомби', 'Анимэ', '']] # одна книга с ошибочным жанром

    @pytest.mark.parametrize('books, genres, results', books_ganres_results)
    def test_get_book_genre_one_books(self, collector, books, genres, results):
        # добавляем книги и жанр
        collector.add_new_book(books)
        collector.set_book_genre(books, genres)
        # проверяем жанр по имени
        assert collector.get_book_genre(books) == results

    # 4 get_books_with_specific_genre — Проверяем список книг с определённым жанром.
    # тестовые данные 4 книги с жанрами и результатом
    books = ['Вторая жизнь Уве',
             'Гордость и предубеждение и зомби',
             'Мечтают ли андроиды об электроовцах',
             'Венецианский купец']
    genres = ['Комедии', 'Ужасы', 'Фантастика', 'Комедии']
    results = ['Вторая жизнь Уве', 'Венецианский купец']

    @pytest.mark.parametrize('books, genres, results', [[books, genres, results]])
    def test_get_books_with_specific_genre_four_books_comedy(self, collector, books, genres, results):
        # добавляем книги и жанры
        for i in range(len(books)):
            collector.add_new_book(books[i])
            collector.set_book_genre(books[i], genres[i])
        # проверяем список книг с выбранным жанром
        assert collector.get_books_with_specific_genre('Комедии') == results

    # 5. get_books_genre — Проверяем вывод текущего словаря books_genre.
    # тестовые данные 2 книги с жанрами и результатом
    books_ganres_results = [['Вторая жизнь Уве', 'Комедии', {'Вторая жизнь Уве': 'Комедии'}],
                            ['Гордость и предубеждение и зомби', 'Ужасы',
                             {'Гордость и предубеждение и зомби': 'Ужасы'}]]

    @pytest.mark.parametrize('books, genres, results', books_ganres_results)
    def test_get_books_genre_one_books(self, collector, books, genres, results):
        # добавляем книги и жанр
        collector.add_new_book(books)
        collector.set_book_genre(books, genres)
        # проверяем вывод словаря
        assert collector.get_books_genre() == results

    # 6. get_books_for_children Книги с возрастным рейтингом отсутствуют в списке книг для детей.
    # тестовые данные 3 книги с жанрами
    books_with_ganres = [['Вторая жизнь Уве', 'Комедии'],
                         ['Гордость и предубеждение и зомби', 'Ужасы'],
                         ['Мечтают ли андроиды об электроовцах', 'Фантастика']]

    @pytest.mark.parametrize('books, genres', books_with_ganres)
    def test_get_books_for_children_one_books(self, collector, books, genres):
        # добавляем книги и жанр
        collector.add_new_book(books)
        collector.set_book_genre(books, genres)
        kid_books = collector.get_books_for_children()
        # проверяем что в списке жанров нет Ужасов и Детективов
        assert 'Ужасы' not in kid_books and 'Детективы' not in kid_books

    # 7 add_book_in_favorites — Проверяем добавление книги в избранное. Книга должна находиться в словаре books_genre.
    # Повторно добавить книгу в избранное нельзя.
    # тестовые данные 2 книги с жанрами и результатом
    books = ['Вторая жизнь Уве',
             'Гордость и предубеждение и зомби']
    genres = ['Комедии', 'Ужасы']
    favorites = 'Вторая жизнь Уве'  # избранное

    @pytest.mark.parametrize('books, genres, favorites', [[books, genres, favorites]])
    def test_add_book_in_favorites_two_books(self, collector, books, genres, favorites):
        # добавляем книги и жанры
        for i in range(len(books)):
            collector.add_new_book(books[i])
            collector.set_book_genre(books[i], genres[i])
        # проверяем favorites
        collector.add_book_in_favorites(favorites)
        assert collector.favorites[0] == favorites

    # 8 delete_book_from_favorites — удаляет книгу из избранного, если она там есть.
    # тестовые данные 2 книги с жанрами и результатом
    books = ['Вторая жизнь Уве',
             'Гордость и предубеждение и зомби']
    genres = ['Комедии', 'Ужасы']
    delete = 'Вторая жизнь Уве'
    results = 'Гордость и предубеждение и зомби'

    @pytest.mark.parametrize('books, genres, delete, results', [[books, genres, delete, results]])
    def test_delete_book_from_favorites_two_books(self, collector, books, genres, delete, results):
        # добавляем книги и жанры
        for i in range(len(books)):
            collector.add_new_book(books[i])
            collector.set_book_genre(books[i], genres[i])
            collector.add_book_in_favorites(books[i])
        # проверяем favorites
        collector.delete_book_from_favorites(delete)
        assert collector.favorites[0] == results

    # 9 get_list_of_favorites_books — получает список избранных книг.
    # тестовые данные 2 книги с жанрами и результатом
    books = ['Вторая жизнь Уве',
             'Гордость и предубеждение и зомби']
    genres = ['Комедии', 'Ужасы']
    favorites = ['Вторая жизнь Уве',
                 'Гордость и предубеждение и зомби']  # избранное

    @pytest.mark.parametrize('books, genres, favorites', [[books, genres, favorites]])
    def test_add_book_in_favorites_two_books(self, collector, books, genres, favorites):
        # добавляем книги и жанры и в избранное
        for i in range(len(books)):
            collector.add_new_book(books[i])
            collector.set_book_genre(books[i], genres[i])
            collector.add_book_in_favorites(favorites[i])
        # проверяем список favorites
        assert collector.get_list_of_favorites_books() == favorites
