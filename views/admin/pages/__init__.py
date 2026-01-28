class ManageBooksPage:
    def __init__(self):
        self.current_book_id = None
        self.books = []
        self.table = None

        # fields (để tránh AttributeError)
        self.title_field = None
        self.author_field = None
        self.category_field = None
        self.price_field = None
        self.quantity_field = None
