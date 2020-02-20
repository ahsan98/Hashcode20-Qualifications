from operator import attrgetter
import copy


class Library:
    id = 0
    total_books = 0
    score = 0
    signup_days = 0
    books_per_day = 0
    avg_score = 0
    selection_points = 0
    start_day = -1
    end_day = -1

    books = []
    scanned_books = []

    def __init__(self):
        self.id = 0
        self.total_books = 0
        self.score = 0
        self.signup_days = 0
        self.books_per_day = 0
        self.avg_score = 0
        self.selection_points = 0
        self.start_day = -1
        self.end_day = -1

        self.books = []
        self.scanned_books = []


file = open('f_libraries_of_the_world.txt', 'r')

data = file.readlines()

first_line = data[0].split()

book_count = int(first_line[0])
libraries_count = int(first_line[1])
scanning_days = int(first_line[2])

book_line = data[1].split()

books = {}

libraries = [None] * libraries_count

books_to_libraries = {}

for i, score in enumerate(book_line):
    books[i] = int(score)

for l in range(libraries_count):
    first_l_line = (2*l) + 2
    fll = data[first_l_line].split()

    lib_id = l
    libraries[lib_id] = Library()
    libraries[lib_id].id = l
    libraries[lib_id].total_books = int(fll[0])
    libraries[lib_id].signup_days = int(fll[1])
    libraries[lib_id].books_per_day = int(fll[2])

    sll = data[first_l_line+1].split()

    libraries[lib_id].books = []
    for book_id in sll:
        book_id = int(book_id)
        libraries[lib_id].score += books[book_id]

        libraries[lib_id].books.append(book_id)

        if book_id in books_to_libraries:
            books_to_libraries[book_id].append(libraries[lib_id].id)
        else:
            books_to_libraries[book_id] = [libraries[lib_id].id]

    libraries[lib_id].avg_score = libraries[lib_id].score / libraries[lib_id].total_books

    libraries[lib_id].selection_points = libraries[lib_id].signup_days/(libraries[lib_id].books_per_day * libraries[lib_id].avg_score)

    libraries[lib_id].books = copy.deepcopy(libraries[lib_id].books)
    # libraries[libraries[lib_id].id] = copy.deepcopy(libraries[lib_id])
    # lib = {}

sorted_libraries = sorted(libraries, key=attrgetter('selection_points'))

selected_libraries = []

remaining_days = scanning_days

library_index = 0
current_day = 0

all_selected_books_1 = {}
while remaining_days > 0 and library_index < libraries_count:
    if sorted_libraries[library_index].start_day == -1 and sorted_libraries[library_index].signup_days <= remaining_days:
        curr_lib = sorted_libraries[library_index]
        selected_libraries.append(curr_lib)
        remaining_days -= curr_lib.signup_days
        curr_lib.start_day = current_day
        curr_lib.end_day = current_day + curr_lib.signup_days
        current_day = curr_lib.end_day + 1

        for book in curr_lib.books:
            if book in all_selected_books_1:
                continue
            book_libraries = books_to_libraries[book]
            all_selected_books_1[book] = True
            for library in book_libraries:
                lib = libraries[library]
                lib.score -= books[book]
                lib.avg_score = lib.score / lib.total_books
                lib.selection_points = lib.signup_days / (lib.books_per_day * lib.avg_score) if lib.avg_score > 0 else 0

        sorted_libraries = sorted(libraries, key=attrgetter('selection_points'))

    library_index += 1


all_selected_books = []
skipped_libs = 0

for lib in selected_libraries:
    selection_days = scanning_days - lib.end_day
    selectable_books = lib.books_per_day * selection_days
    if selectable_books <= 0:
        skipped_libs += 1
        continue

    sorted_books = sorted(lib.books, key=lambda book: books[book])

    sorted_cleaned_books = [b for b in sorted_books if b not in all_selected_books]

    selected_books = sorted_cleaned_books[:selectable_books]
    all_selected_books += selected_books

    lib.scanned_books = selected_books

out = open('output_f.txt', 'w')

out.write(str(len(selected_libraries) - skipped_libs) + '\n')
for lib in selected_libraries:
    if len(lib.scanned_books) <= 0:
        continue
    out.write(str(lib.id) + ' ' + str(len(lib.scanned_books)) + '\n')
    for book in lib.scanned_books:
        out.write(str(book) + ' ')
    out.write('\n')
