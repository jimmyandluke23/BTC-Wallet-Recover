

import logging


def recover_wallet_from_mnemonic(mnemonic_phrase):
    seed = mnemonic.Mnemonic.to_seed(mnemonic_phrase)
    root_key = bip32utils.BIP32Key.fromEntropy(seed)
    child_key = root_key.ChildKey(44 | bip32utils.BIP32_HARDEN).ChildKey(0 | bip32utils.BIP32_HARDEN).ChildKey(0 | bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(0)
    address = child_key.Address()
    balance = check_BTC_balance(address)
    return mnemonic_phrase, balance, address

def recover_wallet_from_partial_mnemonic(partial_mnemonic):
    partial_mnemonic_words = partial_mnemonic.split()
    if len(partial_mnemonic_words) >= 12:
        logging.error("Provided mnemonic phrase should contain less than 12 words.")
        return None, 0, None

    provided_words = len(partial_mnemonic_words)
    missing_words = 12 - provided_words
    logging.info(f"Attempting to recover wallet from {provided_words} words. Missing {missing_words} words.")

    wordlist = mnemonic.Mnemonic("english").wordlist
    for guess in itertools.product(wordlist, repeat=missing_words):
        full_mnemonic = ' '.join(partial_mnemonic_words + list(guess))
        mnemonic_phrase, balance, address = recover_wallet_from_mnemonic(full_mnemonic)
        logging.info(f"Trying mnemonic phrase: {full_mnemonic}")
        logging.info(f"Wallet Address: {address}, Balance: {balance} BTC")
        if balance > 0:
            logging.info(f"Found wallet with non-zero balance: {balance} BTC")
            logging.info(f"Mnemonic Phrase: {mnemonic_phrase}")
            with open("wallet.txt", "a") as f:
                f.write(f"Mnemonic Phrase: {mnemonic_phrase}\n")
                f.write(f"Wallet Address: {address}\n")
                f.write(f"Balance: {balance} BTC\n\n")
            return mnemonic_phrase, balance, address

    logging.info("No wallet found with the provided partial mnemonic phrase.")
    return None, 0, None


