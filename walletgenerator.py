from mnemonic import Mnemonic
from web3 import Web3
import pandas as pd
from eth_account import Account
import os

input_words = int(input('How many seed phrases to generate?\n'))
input_length = int(input('How many words to use, 12 or 24?\n'))
input_key = int(input('How many wallets are there for one seed phrase?\n'))

w3 = Web3(Web3.HTTPProvider())


def gen_key(input_words, input_length, input_key):
    Account.enable_unaudited_hdwallet_features()
    data = []
    for m in range(input_words):
        mnemo = Mnemonic("english")
        if input_length == 12:
            words = mnemo.generate(strength=128)
        elif input_length == 24:
            words = mnemo.generate(strength=256)
        else:
            print('Wrong number of words')
            continue

        for i in range(input_key):
            acct = Account.from_mnemonic(
                words,
                account_path=f"m/44'/60'/0'/0/{i}"
            )
            addr = acct.address
            key = w3.to_hex(acct._private_key)
            data.append({'wallet address': addr, 'private keys': key, 'seed': words})

    df = pd.DataFrame(data, columns=['wallet address', 'private keys', 'seed'])

    file_path = os.path.join(os.getcwd(), 'seed.xlsx')  # Full path to the 'seed.xlsx' file

    if not os.path.isfile(file_path):
        # Create a new Excel file if it doesn't exist
        df.to_excel(file_path, index=False)
    else:
        # Append to the existing Excel file
        with pd.ExcelWriter(file_path, mode='a', engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False, header=False)


gen_key(input_words, input_length, input_key)
