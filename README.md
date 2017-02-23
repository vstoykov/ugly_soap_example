Example project for bug in python-zeep
---------------------------------------

This project is created to show issue in python-zeep about parsing
RPC encoded SOAP messages
https://github.com/mvantellingen/python-zeep/issues/326

## 1. Install requirements

    pip install -r requirements.txt

## 2. Start server

    python soap_server.py

## 3.  Run the client

    python soap_client.py

Client will print responses from `suds` and `zeep` in order to see the difference
