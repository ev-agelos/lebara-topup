# Topup your Lebara sim card with credits

Prompts user for email, mobile number and bank selection and then opens up the browser in the selected banks website and lets user finish up the payment.

### Install
Install in a virtual environment with pipenv:
`pipenv install`

### Run
```
$ ./topup.py
```

or supply the `BROWSER` env variable to use a different browser other than the default:
```
$ BROWSER=chromium ./topup.py
```

### Problems
* Only _iDeal_ is supported (for now) as a paypent method
* _LebaraOne_ is only supported(for now)
* Selecting _Rabobank_ or _Van Lanschot Bankiers_ do not seem to work

