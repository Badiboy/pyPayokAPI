import inspect
from time import sleep
try:
    from pyPayokAPI import pyPayokAPI, pyPayokAPIException, PayoutMethod, PaymentCommissionType, PaymentStatus, PaymentMethod
except:
    from api import pyPayokAPI, pyPayokAPIException, PayoutMethod, PaymentCommissionType, PaymentStatus, PaymentMethod

try:
    from private_keys import *
except:
    test_api_id = "---"
    test_api_key = "---"
    test_secret_key = "---"
    test_shop_id = "0"

def run_and_print(f):
    try:
        sleep(1)
        print()
        print(inspect.getsourcelines(f)[0][0].strip())
        res = f()
        if isinstance(res, list):
            for i in res:
                print(i)
        else:
            print(res)
        return res
    except pyPayokAPIException as pe:
        if pe.code in [-2]:
            print("API call failed. Code: {}, Message: {}".format(pe.code, pe.message))
        else:
            print("API call failed. Code: {}, Message: {}".format(pe.code, pe.message))
            #raise pe
    except Exception as e:
        raise e
    return None

def test_api_functions():
    client = pyPayokAPI(test_api_id, test_api_key, secret_key=test_secret_key, print_errors=True)
    run_and_print(lambda: client.balance())
    run_and_print(lambda: client.transaction(test_shop_id))
    run_and_print(lambda: client.transactions(test_shop_id, status=PaymentStatus.success))
    run_and_print(lambda: client.payout())
    run_and_print(lambda: client.payout_create(1, PayoutMethod.qiwi, "79111111111", PaymentCommissionType.payment))
    run_and_print(lambda: client.payment_link_create(10, "xxx 2", test_shop_id, "Test payment link", 'RUB'))

test_api_functions()
