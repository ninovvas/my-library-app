import requests


class BookSearch:

    books_api = 'https://www.googleapis.com/books/v1/volumes'
    parameters = {'q': '',
                  'fields': 'kind,totalItems,items(kind,volumeInfo(title,subtitle,authors,publisher,industryIdentifiers,imageLinks/thumbnail,description,pageCount,language))'
                  }
    search = ''  # user's search query, populated in __init__
    results = ''  # response from google books, populated by parse_results()

    """
    Using
    book_search = BookSearch(search_query)
    book_search.make_a_search()
    results = book_search.get_search_results()
    """

    def __init__(self, search=''):
        self.search = search
        self.search_item = search


    def make_a_search(self):
        self.construct_request()
        self.send_request()
        self.parse_results()


    # adds user's search phrase to parameters
    def construct_request(self):
        self.parameters['q'] = self.search


    def send_request(self):
        self.search = requests.get(self.books_api, params=self.parameters)


    # store the results in a python dictionary
    def parse_results(self):
        self.results = self.search.json()


    def get_search_results(self):
        search_results = []

        #format_search_item = self.search_item.upper()
        #format_search_item = self.search_item.strip()
        format_search_item = self.search_item

        if self.results['totalItems'] == 0:
            return None
        num_results = len(self.results['items'])
        is_results = False
        for result in range(num_results):
            formatted_result = {
                'title': self._get_result_title(result),
                'authors': self._get_result_authors(result),
                'publisher': self._get_result_publisher(result),
                'thumbnail': self._get_thumbnail_url(result),
                'goodreads': self._make_goodreads_url(result),
                'description': self._get_result_description(result),
                'page_count': self._get_result_page_count(result),
                'language': self._get_result_language(result),
                'isbns': self._get_result_all_isbns(result),
            }
            is_found = False
            for field_name, result_value in formatted_result.items():
                if 'title' == field_name:
                    if format_search_item in result_value:
                        is_found = True
                        break
                if 'isbns' == field_name:
                    for d_value in result_value:
                        for value in d_value.values():
                            if format_search_item in value:
                                is_found = True
                                break
                        if is_found:
                            break
                if is_found:
                    break

            if is_found:
                is_results = True
                break

            #formatted_result_contains_none = [value is None for value in formatted_result.values()]
            #if True not in formatted_result_contains_none:
            #    break
            #search_results.append(formatted_result)
        if is_results:
            return formatted_result
        else:
            return {}

    def _get_result_title(self, result):
        __field_name = 'title'
        __field_name_sub = 'subtitle'
        title = None
        if __field_name in self.results['items'][result]['volumeInfo']:
            title = self.results['items'][result]['volumeInfo'][__field_name]

        if __field_name_sub in self.results['items'][result]['volumeInfo']:
            title += ': ' + self.results['items'][result]['volumeInfo'][__field_name_sub]

        return title

    def _get_result_authors(self, result):
        __field_name = 'authors'
        return self._get_volume_info_field_value(result, __field_name)

    def _get_result_description(self, result):
        __field_name = 'description'
        return self._get_volume_info_field_value(result, __field_name)

    def _get_result_page_count(self, result):
        __field_name = 'pageCount'
        return self._get_volume_info_field_value(result, __field_name)

    def _get_result_language(self, result):
        __field_name = 'language'
        return self._get_volume_info_field_value(result, __field_name)

    def _get_volume_info_field_value(self, result, field_name):
        field_result = None
        if field_name in self.results['items'][result]['volumeInfo']:
            field_result = self.results['items'][result]['volumeInfo'][field_name]
        return field_result

    def _get_result_publisher(self, result):
        publisher = None
        __field_name = 'publisher'

        if __field_name in self.results['items'][result]['volumeInfo']:
            publisher = self.results['items'][result]['volumeInfo'][__field_name]

        return publisher

    def _get_thumbnail_url(self, result):
        __field_name = 'imageLinks'
        thumbnail = None
        if __field_name in self.results['items'][result]['volumeInfo']:
            thumbnail = self.results['items'][result]['volumeInfo'][__field_name]['thumbnail']
        return thumbnail

    def _make_goodreads_url(self, result):
        goodreads = 'https://www.goodreads.com/book/show/'
        id = self._get_goodreads_id(result)
        if id is None:
            return None
        return goodreads + str(id)

    def _get_goodreads_id(self, result):
        goodreads_id = None
        isbn = self._get_result_isbn(result)
        if isbn:
            goodreads_api = 'https://www.goodreads.com/book/isbn_to_id'
            params = {'key' : 'Hc3p3luBbcApaSFOTIgadQ', 'isbn' : isbn}
            goodreads_response = requests.get(goodreads_api, params=params)
            goodreads_id = goodreads_response.text
        return goodreads_id

    def _get_result_isbn(self, result):
        __field_name = 'industryIdentifiers'
        if __field_name in self.results['items'][result]['volumeInfo']:
            for id in self.results['items'][result]['volumeInfo'][__field_name]:
                if id['type'] == 'ISBN_13':
                    return id['identifier']
        return None

    def _get_result_all_isbns(self, result):
        __field_name = 'industryIdentifiers'
        if __field_name in self.results['items'][result]['volumeInfo']:
            return self.results['items'][result]['volumeInfo'][__field_name]
        return None

    def _get_results_count(self):
        return self.results.get("totalItems", None)