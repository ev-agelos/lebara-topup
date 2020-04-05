import re

from bs4 import BeautifulSoup


class Form:

    def __init__(self, html):
        if html.name == 'form':
            self._form = html
        else:
            self._form = html.find('form')

        self.action = self._form.attrs['action']
        self.fields = self._form.find_all(re.compile('(input|select)'))
        self.errors = {
            span.text.strip()
            for span in self._form.find_all('span', id=re.compile('\.errors'))
        }

        self.data = {}
        for element in self.fields:
            if element.name == 'input':
                self.data[element['name']] = element['value']
            elif element.name == 'select':
                self.data[element['name']] = ''

    @classmethod
    def from_id(cls, html, id):
        soup = BeautifulSoup(html, 'html5lib')
        html_form = soup.find('form', id=id)
        return cls(html_form) if html_form else None


class Product:

    def __init__(self, li):
        self.li = li
        self.form = Form(li)

    @property
    def name(self):
        # FIXME use re
        element = (self.li.find('div', class_='marketing-name')
                   or self.li.find('div', class_='product-name'))
        return element.text.strip()

    @property
    def price(self):
        # FIXME use re
        element = (self.li.find('div', class_='product-price')
                   or self.li.find('div', class_='price'))
        return element.text.strip()

    @property
    def data(self):
        data_section = self.li.find('div', class_='data-section')
        if not data_section:
            return ''
        quantity = data_section.find('span', class_='data-qty')
        unit = data_section.find('span', class_='data-unit')
        return (quantity.text.strip().replace('\n', '')
                + unit.text.strip().replace('\n', ''))


def get_products(html):
    soup = BeautifulSoup(html, 'html5lib')
    li_elements = soup.find_all('li', class_='product-item')
    return [Product(li) for li in li_elements]
