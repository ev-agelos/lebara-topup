#!/usr/bin/env python3

from urllib.parse import urljoin
import webbrowser

import requests
from bs4 import BeautifulSoup


URL = 'https://mobile.lebara.com'
LEBARA_ONE_FORM_ID = 'buyNowFormLebaraOne'
PAY_FORM_ID = 'localPaymentForm'


def get_form_by_id(response, id):
    html = response.content.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find(id=id)


def get_user_details():
    answer = ''
    while answer != 'Y':
        email = input('Email: ')
        number = input('Mobile number: ')
        answer = input(
            'Phone: {} Email: {}\nAre the details correct? [Y/n] '
            .format(number, email)
        )
        print('\n')
    return email, number


def get_user_bank(options):
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
        # get lebara packages
        response = s.get(urljoin(URL, '/nl/en/prepaid-beltegoed-opwaarderen'))
        lebara_one_form = get_form_by_id(response, LEBARA_ONE_FORM_ID)
        payload = {element['name']: element['value']
                   for element in lebara_one_form.find_all('input')}

        # select lebara one
        buynow = s.post(urljoin(URL, lebara_one_form['action']), data=payload)
        returned_form = get_form_by_id(buynow, 'buyNowAutoSubmit')
        payload = {element['name']: element['value']
                   for element in returned_form.find_all('input')}
        topup_login = s.post(urljoin(URL, returned_form['action']), data=payload,
                             allow_redirects=True)
        # Guest login
        email, number = get_user_details()
        guest_form = get_form_by_id(topup_login, 'lebara-form')
        csrf_token = guest_form.find('input', dict(name='CSRFToken'))['value']
        payload = dict(email=email, msisdn=number, msisdnCheck=number,
                       CSRFToken=csrf_token)
        login_response = s.post(urljoin(URL, guest_form['action']), data=payload)
        if 'Please enter valid number' in login_response.text:
            print('Invalid mobile number.')
            return

        # select payment method
        response = s.get(urljoin(URL, '/nl/en/cart/checkout'), allow_redirects=True)
        form = get_form_by_id(response, PAY_FORM_ID)
        select_field = form.find('select', id='payment.choose.bank.label')
        options = select_field.find_all('option')[1:]
        bank = get_user_bank(options)
        bank_code = select_field.find('option', text=bank)['value']
        payload = dict(
            issuerId=bank_code,
            brandCode='ideal',
            recurringContract='ONECLICK',
            CSRFToken=csrf_token
        )
        # checkout to get the form to pay
        process_response = s.post(urljoin(URL, form['action']), data=payload)
        form = get_form_by_id(process_response, PAY_FORM_ID)
        payload = {element['name']: element['value']
                   for element in form.find_all('input')
                   if element['name'] != 'CSRFToken'}
        response = s.post(form['action'], data=payload, allow_redirects=True)

        webbrowser.open_new_tab(response.url)


if __name__ == '__main__':
    main()
