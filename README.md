Topup your Lebara sim card with credits.
------------------
* Only iDeal is supported (for now) as a paypent method.
* LebaraOne is only supported(for now).
* It opens firefox just before signing in bank's website to finish up the payment. It shifts the focus to firefox and closes it if transaction gets cancelled.
------------------
Install in a virtual environment with pipenv:
`pipenv install`

Supply required info and run with:
```
$ LEBARA_MOBILE=06.. LEBARA_EMAIL=.. LEBARA_BANK=.. ./topup.py
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
