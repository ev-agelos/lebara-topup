Topup your Lebara sim card with credits.
------------------
* Only iDeal is supported (for now) as a paypent method.
* LebaraOne is only supported(for now).
* Opens the default browser just before signing in bank's website, to let user finish up the payment.
------------------
Install in a virtual environment with pipenv:
`pipenv install`

Supply required info and run with:
```
$ LEBARA_MOBILE=06.. LEBARA_EMAIL=.. LEBARA_BANK=.. ./topup.py
```

Use your own choice of browser:
```
$ LEBARA_MOBILE=06.. LEBARA_EMAIL=.. LEBARA_BANK=.. BROWSER=chromium ./topup.py
```

Banks to choose from:
- ABN Amro
- ASN Bank
- bunq
- ING
- Knab
- ~~Rabobank~~
- RegioBank
- SNS Bank
- Triodos Bank
- ~~Van Lanschot Bankiers~~
