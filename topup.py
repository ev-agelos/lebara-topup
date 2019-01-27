#!/usr/bin/env python3

import os
from urllib.parse import urljoin
import webbrowser

import requests
from bs4 import BeautifulSoup


NUMBER = os.environ['LEBARA_NUMBER']
EMAIL = os.environ['LEBARA_EMAIL']
BANK = os.environ['LEBARA_BANK']

URL = 'https://mobile.lebara.com'
LEBARA_ONE_FORM_ID = 'buyNowFormLebaraOne'
PAY_FORM_ID = 'localPaymentForm'


def get_form_by_id(response, id):
    html = response.content.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find(id=id)


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
        guest_form = get_form_by_id(topup_login, 'lebara-form')
        csrf_token = guest_form.find('input', dict(name='CSRFToken'))['value']
        payload = dict(email=EMAIL, msisdn=NUMBER, msisdnCheck=NUMBER,
                       CSRFToken=csrf_token)
        login_response = s.post(urljoin(URL, guest_form['action']), data=payload)
        if 'Please enter valid number' in login_response.text:
            print('Invalid mobile number.')
            return

        # select payment method
        response = s.get(urljoin(URL, '/nl/en/cart/checkout'), allow_redirects=True)
        form = get_form_by_id(response, PAY_FORM_ID)
        select_field = form.find('select', id='payment.choose.bank.label')
        bank_code = select_field.find('option', text=BANK)['value']
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
        os.system('wmctrl -a ' + os.environ.get('BROWSER', ''))


if __name__ == '__main__':
    main()
