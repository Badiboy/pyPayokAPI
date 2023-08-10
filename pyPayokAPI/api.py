import requests
import hashlib
import urllib
import urllib.parse
from time import sleep

from .payok_types import *

API_URL = "https://payok.io/api/"


# noinspection PyPep8Naming
class pyPayokAPIException(Exception):
    def __init__(self, code, message, full_error = ""):
        self.code = code
        self.message = message
        self.full_error = full_error
        super().__init__(self.message)


# noinspection PyPep8Naming
class pyPayokAPI:
    """
    pyPayokAPI API Client
    """

    def __init__(self, api_id, api_key,
                 secret_key = None,
                 print_errors = False, timeout = None):
        """
        Create the pyPayokAPI instance.

        :param api_id: API id for access
        :param api_key: API key for access
        :param secret_key: (Optional) Secret key for payment links
        :param print_errors: (Optional) Print dumps on request errors
        :param timeout: (Optional) Request timeout
        """
        self.api_id = api_id
        self.api_key = api_key
        self.secret_key = secret_key
        self.print_errors = print_errors
        self.timeout = timeout


    def __request(self, method_url, **kwargs):
        """
        Send request to API

        :param method_url: (String) API method url (part)
        :param kwargs: request data
        """
        if kwargs:
            data = dict(kwargs)
        else:
            data = {}
        data["API_ID"] = self.api_id
        data["API_KEY"] = self.api_key

        base_resp = None
        try:
            base_resp = requests.post(API_URL + method_url, data=data, timeout=self.timeout)
            resp = base_resp.json()
        except ValueError as ve:
            code = base_resp.status_code if base_resp else -2
            message = "Response decode failed: {}".format(ve)
            if self.print_errors:
                print(message)
            raise pyPayokAPIException(code, message)
        except Exception as e:
            code = base_resp.status_code if base_resp else -3
            message = "Request unknown exception: {}".format(e)
            if self.print_errors:
                print(message)
            raise pyPayokAPIException(code, message)
        if not resp:
            code = base_resp.status_code if base_resp else -4
            message = "None request response"
            if self.print_errors:
                print(message)
            raise pyPayokAPIException(code, message)
        elif resp.get("status", "") == "error":
            code = resp["error_code"]
            if isinstance(code, str):
                if code.isdigit():
                    code = int(code)
            if "text" in resp:
                message = resp["text"]
            elif "error_text" in resp:
                message = resp["error_text"]
            else:
                message = "No error info provided"
            if self.print_errors:
                print("Response: {}".format(resp))
            raise pyPayokAPIException(code, message)
        # elif not resp.get("status"):
        #     if resp.get("error_code"):
        #         code = resp["error_code"]
        #     elif base_resp:
        #         code = base_resp.status_code
        #     else:
        #         code = -5
        #     if resp.get("text"):
        #         message = resp["text"]
        #     else:
        #         message = "No error info provided"
        #     if self.print_errors:
        #         print("Response: {}".format(resp))
        #     raise pyPayokAPIException(code, message)
        # code -6 is used above
        else:
            return resp


    def balance(self):
        """
        Get balance of account
        https://payok.io/cabinet/documentation/doc_api_balance
        """
        method = "balance"
        resp = self.__request(method)
        return Balance.de_json(resp)


    def transaction(self, shop, payment = None, offset = None):
        """
        Get transactions list.
        Max 100 records, use offset to get more.
        https://payok.io/cabinet/documentation/doc_api_transaction

        :param shop: Shop ID
        :param payment: (Optional) Payment ID (only one record with this payment will be returned)
        :param offset: (Optional) Offset (skip given number of transactions)
        """
        _method = "transaction"
        params = {
            "shop": shop,
        }
        if payment:
            params["payment"] = payment
        if offset:
            params["offset"] = offset
        try:
            resp = self.__request(_method, **params)
        except pyPayokAPIException as pe:
            if pe.code == 10:
                # Error "No transactions"
                return Transactions()
            else:
                raise pe
        return Transactions.de_json(resp)

    def transactions(self, shop, max_results = 15, max_pages = 10, status = None):
        """
        Get transactions list (advanced method for "transaction").

        :param shop: Shop ID
        :param max_results: (Int, Optional, default=15) Max number of results to collect
        :param max_pages: (Int, Optional, default=10) Max number of pages to process
        :param status: (PaymentStatus, Optional) Filter by status
        """

        result = Transactions()

        page_number = 0
        page_size = 100
        offset = 0
        while page_number < max_pages:
            if page_number > 0: sleep(1)
            resp = self.transaction(shop, offset = offset)

            if not resp.items:
                # No (more) transactions
                break

            for transaction in resp.items:
                if transaction.transaction_status != status:
                    continue
                result.items.append(transaction)

                if len(result.items) >= max_results:
                    # Enough results collected
                    break

            if len(result.items) >= max_results:
                # Enough results collected
                break

            offset += page_size
            page_number += 1

        return result


    def payout(self, payout_id = None, offset = None):
        """
        Get payouts list.
        Max 100 records, use offset to get more.
        https://payok.io/cabinet/documentation/doc_api_payout

        :param payout_id: (Optional) Payment ID (only one record with this payout will be returned)
        :param offset: (Optional) Offset (skip given number of payouts)
        """
        _method = "payout"
        params = {}
        if payout_id:
            params["payout_id"] = payout_id
        if offset:
            params["offset"] = offset
        try:
            if params:
                resp = self.__request(_method, **params)
            else:
                resp = self.__request(_method)
        except pyPayokAPIException as pe:
            if pe.code == 7:
                # Error "No payouts"
                return Payouts()
            else:
                raise pe
        return Payouts.de_json(resp)


    def payout_create(self, amount, method, reciever, comission_type, webhook_url = None):
        """
        Create payout.
        https://payok.io/cabinet/documentation/doc_api_payout_create

        :param amount: Amount to payout
        :param method: Payout method (see PayoutMethod)
        :param reciever: Reciever credentials
        :param comission_type: Comission type (see PayoutCommissionType)
        :param webhook_url: (Optional) Webhook URL to call when payout status changes
        """
        _method = "payout_create"
        params = {
            "amount": amount,
            "method": method.name if isinstance(method, PayoutMethod) else method,
            "reciever": reciever,
            "comission_type": comission_type.name if isinstance(comission_type, PaymentCommissionType) else comission_type,
        }
        if webhook_url:
            params["webhook_url"] = webhook_url
        resp = self.__request(_method, **params)
        return Payout.de_json(resp, 1)


    def payment_link_create(
            self, amount, payment, shop, desc, currency,
            email = None, success_url = None, method = None, lang = None, custom = None):
        """
        Create payment link (invoice).

        :param amount: Amount to pay
        :param payment: Order ID (unique in your system, up to 36 characters)
        :param shop: Your shop ID
        :param desc: Product name or description
        :param currency: Currency
        :param email: (Optional) Customer email
        :param success_url: (Optional) URL to redirect after payment
        :param method: (Optional) Payment method / list of methods (see PaymentMethod)
        :param lang: (Optional) Interface language (RU or EN)
        :param custom: (Optional) Your custom parameter to pass in notification
        """
        if not self.secret_key:
            raise pyPayokAPIException(-7, "No secret key provided when creating pyPayokAPI")

        sign_data = [
            amount,
            payment,
            shop,
            currency,
            desc,
            self.secret_key,
        ]
        sign = hashlib.md5("|".join(map(str, sign_data)).encode("utf-8")).hexdigest()

        url = "https://payok.io/pay?amount={amount}&payment={payment}&shop={shop}&desc={desc}&currency={currency}&sign={sign}".format(
            amount=amount,
            payment=urllib.parse.quote(payment),
            shop=shop,
            desc=urllib.parse.quote(desc),
            currency=currency,
            sign=sign,
        )
        if email:
            url += f"&email={email}"
        if success_url:
            success_url = urllib.parse.quote_plus(success_url)
            url += f"&success_url={success_url}"
        if method:
            if isinstance(method, PaymentMethod):
                url += f"&method={method.name}"
            else:
                url += f"&method={method}"
        if lang:
            url += f"&lang={lang}"
        if custom:
            url += f"&customparam={custom}"
        return url
