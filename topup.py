#!/usr/bin/env python3

from urllib.parse import urljoin
import webbrowser

import requests

from product import get_products, Form


URL = 'https://mobile.lebara.com'
PAY_FORM_ID = 'localPaymentForm'


def select_product(products):
    # FIXME tabularize
    print('# - Product - Price')
    for i, p in enumerate(products, start=1):
        print(i, p.name, p.data, p.price)

    while True:
        answer = int(input('Select package: '))
        if answer > 0 and answer <= len(products):
            break

    return products[answer - 1]


def select_bank(options):
    banks = [f'{idx}: {o.text}' for idx, o in enumerate(options, start=1)]
    answer = 0
    while 1:
        answer = input('\n'.join(banks) + '\nChoose your bank: ')
        try:
            answer = int(answer)
        except ValueError:
            answer = 0

        if 0 < answer << len(options):
            break

        print('\nInvalid option!\n')

    return options[answer - 1].text


def main():
    with requests.Session() as s:
        # get products
        response = s.get(urljoin(URL, '/nl/en/prepaid-beltegoed-opwaarderen'))
        products = get_products(response.content)

        # select product
        product = select_product(products)
        buynow = s.post(urljoin(URL, product.form.action), data=product.form.data)
        form = Form.from_id(buynow.content, 'buyNowAutoSubmit')
        topup_login = s.post(urljoin(URL, form.action), data=form.data,
                             allow_redirects=True)

        # Authorize
        email = input('Email: ')
        number = input('Mobile number: ')
        guest_form = Form.from_id(topup_login.content, 'lebara-form')
        guest_form.data.update(email=email, msisdn=number, msisdnCheck=number)
        auth_response = s.post(urljoin(URL, guest_form.action), data=guest_form.data)
        auth_form = Form.from_id(auth_response.content, 'lebara-form')
        if auth_form and auth_form.errors:
            print('\n'.join(auth_form.errors))
            return

        # select payment method
        response = s.get(urljoin(URL, '/nl/en/cart/checkout'), allow_redirects=True)
        form = Form.from_id(response.content, PAY_FORM_ID)
        for field in form.fields:
            if field.name == 'select':
                selection = select_bank(field.find_all('option')[1:])
                value = field.find('option', text=selection)['value']
                form.data[field['name']] = value

        # checkout to get the form to pay
        process_response = s.post(urljoin(URL, form.action), data=form.data)
        form = Form.from_id(process_response.content, PAY_FORM_ID)
        del form.data['CSRFToken']
        response = s.post(form.action, data=form.data, allow_redirects=True)

        webbrowser.open_new_tab(response.url)


if __name__ == '__main__':
    main()
