import json
from abc import ABC
from enum import Enum


class Dictionaryable(ABC):
    """
    (c) Based on pyTelegramBotAPI (https://github.com/eternnoir/pyTelegramBotAPI) Dictionaryable
    Subclasses of this class are guaranteed to be able to be converted to dictionary.
    All subclasses of this class must override to_dict.
    """

    def to_dict(self):
        """
        Returns a DICT with class field values
        This function must be overridden by subclasses.

        :return: a DICT
        """
        raise NotImplementedError


class JsonSerializable(ABC):
    """
    (c) Based on pyTelegramBotAPI (https://github.com/eternnoir/pyTelegramBotAPI) JsonSerializable
    Subclasses of this class are guaranteed to be able to be converted to JSON format.
    All subclasses of this class must override to_json.
    """

    def to_json(self):
        """
        Returns a JSON string representation of this class.
        This function must be overridden by subclasses.

        :return: a JSON formatted string.
        """
        raise NotImplementedError


class JsonDeserializable(ABC):
    """
    (c) Based on pyTelegramBotAPI (https://github.com/eternnoir/pyTelegramBotAPI) JsonDeserializable
    Subclasses of this class are guaranteed to be able to be created from a json-style dict or json formatted string.
    All subclasses of this class must override de_json.
    """

    @classmethod
    def de_json(cls, json_dict, process_mode = 0):
        """
        Returns an instance of this class from the given json dict or string.
        This function must be overridden by subclasses.

        :param json_dict: The json dict from which to create the object.
        :param process_mode: 0 - do nothing, 1 - create class instance, 2 - create class instance and fill fields

        :return: an instance of this class created from the given json dict or string.
        """
        if process_mode == 0:
            return None
        instance = cls()
        if process_mode == 2:
            for key, value in json_dict.items():
                if key.isdigit(): pass
                setattr(instance, key, value)
        return instance

    @staticmethod
    def check_json(input_json, dict_copy=False):
        """
        Checks whether input_json is a dict or a string. If it is already a dict, it is returned as-is.
        If it is not, it is converted to a dict by means of json.loads(json_type)

        :param input_json: input json or parsed dict
        :param dict_copy: if dict is passed and it is changed outside
        :return: Dictionary parsed from json or original dict
        """
        if isinstance(input_json, dict):
            return input_json.copy() if dict_copy else input_json
        elif isinstance(input_json, str):
            return json.loads(input_json)
        else:
            raise ValueError("input_json should be a json dict or string.")

    def __str__(self):
        # d = {
        #     x: y.__dict__ if hasattr(y, '__dict__') else y
        #     for x, y in self.__dict__.items()
        # }
        d = {}
        for x, y in self.__dict__.items():
            if isinstance(y, list):
                d[x] = [str(i) for i in y]
            elif isinstance(y, dict):
                d[x] = {k:str(v) for k, v in y.items()}
            elif hasattr(y, '__dict__'):
                d[x] = y.__dict__
            else:
                d[x] = y
        return str(d)


# noinspection PyMethodOverriding
class Balance(JsonDeserializable):
    def __init__(self):
        self.balance = None
        self.ref_balance = None

    @classmethod
    def de_json(cls, json_dict):
        data = cls.check_json(json_dict)
        instance = super(Balance, cls).de_json(data, process_mode=2)
        instance.balance = float(instance.balance)
        instance.ref_balance = float(instance.ref_balance)
        return instance


class PaymentCurrency(Enum):
    RUB = "Rubles"
    USD = "US Dollars"
    EUR = "Euro"
    UAH = "Hryvnias"
    RUB2 = "Rubles (Alternative gateway)"
    Unknown = "Unknown"


# noinspection PyMethodOverriding
class Transaction(JsonDeserializable):
    def __init__(self):
        self.num = None
        self.transaction = None
        self.email = None
        self.amount = None
        self.currency = None
        self.currency_amount = None
        self.comission_percent = None
        self.comission_fixed = None
        self.amount_profit = None
        self.method = None
        self.payment_id = None
        self.description = None
        self.date = None
        self.pay_date = None
        self.transaction_status = None
        self.custom_fields = None
        self.webhook_status = None
        self.webhook_amount = None

    @classmethod
    def de_json(cls, json_dict, num):
        data = cls.check_json(json_dict)
        instance = super(Transaction, cls).de_json(data, process_mode=2)
        instance.num = num
        if instance.currency and (instance.currency in PaymentCurrency.__members__):
            instance.currency = PaymentCurrency(instance.currency)
        else:
            instance.currency = PaymentCurrency.Unknown
        return instance


# noinspection PyMethodOverriding
class Transactions(JsonDeserializable):
    def __init__(self):
        self.items = []

    @classmethod
    def de_json(cls, json_dict):
        data = cls.check_json(json_dict)
        instance = super(Transactions, cls).de_json(data, process_mode=2)
        instance.items = []
        for key, value in data.items():
            if not key.isdigit(): pass
            transaction = Transaction.de_json(json.dumps(value), int(key))
            instance.items.append(transaction)
        return instance


class PaymentMethod(Enum):
    card = "Bank card"
    card_uah = "Bank card (Ukraine)"
    card_foreign = "Bank card (Foreign)"
    qiwi = "Qiwi"
    yoomoney = "Yoomoney"
    payeer = "Payeer"
    advcash = "Advcash"
    perfect_money = "Perfect Money"
    webmoney = "Webmoney"
    bitcoin = "Bitcoin"
    litecoin = "Litecoin"
    tether = "Tether USDT"
    tron = "Tron"
    dogecoin = "Dogecoin"
    ethereum = "Ethereum"
    ripple = "Ripple"
    unknown = "Unknown"


class PayoutStatus(Enum):
    waiting = 0
    success = 1
    fail = 2
    unknown = 99


class PaymentCommissionType(Enum):
    balance = "Comission from balance"
    payment = "Comission from payment"


# noinspection PyMethodOverriding
class Payout(JsonDeserializable):
    def __init__(self):
        self.num = None
        self.payout_id = None
        self.method = None
        self.amount = None
        self.comission_percent = None
        self.comission_fixed = None
        self.amount_profit = None
        self.date_create = None
        self.date_pay = None
        self.status = None
        self.remain_balance = None
        self.payout_status_code = None
        self.payout_status_text = None

    @classmethod
    def de_json(cls, json_dict, num):
        data = cls.check_json(json_dict)
        instance = super(Payout, cls).de_json(data, process_mode=2)
        instance.num = num
        if instance.method and (instance.method in PaymentMethod.__members__):
            instance.method = PaymentMethod(instance.method)
        else:
            instance.method = PaymentMethod.unknown
        if instance.status and (instance.status in PayoutStatus.__members__):
            instance.status = PayoutStatus(instance.status)
            instance.payout_status_code = instance.status.value
        elif instance.payout_status_code and (instance.payout_status_code in PayoutStatus.__members__):
            instance.payout_status_code = PayoutStatus(instance.payout_status_code)
            instance.status = instance.payout_status_code.value
        else:
            instance.status = PayoutStatus.unknown
            instance.payout_status_code = PayoutStatus.unknown
        return instance


# noinspection PyMethodOverriding
class Payouts(JsonDeserializable):
    def __init__(self):
        self.items = []

    @classmethod
    def de_json(cls, json_dict):
        data = cls.check_json(json_dict)
        instance = super(Payouts, cls).de_json(data, process_mode=2)
        instance.items = []
        for key, value in data.items():
            if not key.isdigit(): pass
            payout = Payout.de_json(json.dumps(value), int(key))
            instance.items.append(payout)
        return instance
