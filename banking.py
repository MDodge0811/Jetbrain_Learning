import secrets
import sqlite3

conn1 = sqlite3.connect('card.s3db')
conn2 = sqlite3.connect('card.s3db')

c = conn1.cursor()
d = conn2.cursor()

# c.execute("""CREATE TABLE card (
#             id INTEGER PRIMARY KEY,
#             number TEXT,
#             pin TEXT,
#             balance INTEGER DEFAULT 0
#             )""")


def user_view(card_number):
    choice = input("1. Balance\n2. Add income \n3. Do transfer \n4. Close account \n5. Log out\n0. Exit")
    if choice == '1':
        c.execute(f"SELECT balance FROM card WHERE number = {card_number}")
        print(f"Balance: {c.fetchone()}")
        return user_view(card_number)
    elif choice == '2':
        return update_balance(card_number)
    elif choice == '3':
        return transfer(card_number)
    elif choice == '4':
        return close_account(card_number)
    elif choice == '5':
        return main()
    elif choice == '0':
        exit()


def close_account(card_number):
    c.execute(f"DELETE FROM card WHERE number = {card_number}")
    conn1.commit()
    print("The account has been closed!")
    return main()


def update_balance(card_number):
    balance_update = int(input("Enter income: "))
    c.execute(f"""UPDATE card SET balance = balance + {balance_update} 
                WHERE number = {card_number}""")
    conn1.commit()
    print("Income was added!")
    return user_view(card_number)


def transfer(card_number):
    transfer_card = input("Enter card number: ")
    d.execute(f"SELECT number FROM card WHERE number = {transfer_card}")
    if luhn_check(transfer_card) is False:
        print("Probably you made a mistake in the card number. Please try again!")
        return user_view(card_number)
    elif d.fetchone() is None:
        print("Such a card does not exist.")
        return user_view(card_number)
    else:
        if card_number == transfer_card:
            print("You can't transfer money to the same account!")
            return user_view(card_number)
        else:
            transfer_amount = int(input("Enter how much money you want to transfer: "))
            d.execute(f"SELECT balance FROM card WHERE number = {card_number}")
            if int(d.fetchone()[0]) - transfer_amount < 0:
                print("Flag A")
                print("Not enough money!")
                return user_view(card_number)
            else:
                print("Flag B")
                d.execute(f"UPDATE card SET balance = balance - {transfer_amount} WHERE number = {card_number}")
                d.execute(f"UPDATE card SET balance = balance + {transfer_amount} WHERE number = {transfer_card}")
                conn2.commit()
                return user_view(card_number)


def create_account():
    pin = '{:0>4}'.format(secrets.randbelow(10**4))
    account_number = '400000' + '{:0>9}'.format(secrets.randbelow(10**9))
    lst = [int(x) for x in account_number]
    for x in range(len(lst)):
        if x % 2 == 0:
            y = lst[x] * 2
            if y >= 10:
                y = y - 9
            lst.pop(x)
            lst.insert(x, y)
    full_card = lst + [0]
    number = ''
    for x in range(0, 10):
        y = (x + sum(lst))
        if y % 10 == 0:
            full_card.insert(15, x)
            number = account_number + str(x)
    c.execute(f"INSERT INTO card (number, pin) VALUES ({number}, {pin})")
    conn1.commit()
    print(f"Your card number: \n{number}\nYour card PIN: \n{pin}")
    return main()


def sum_digits(digit):
    if digit < 10:
        return digit
    else:
        sum = (digit % 10) + (digit // 10)
        return sum


def luhn_check(card_number):
    # reverse the credit card number
    cc_num = card_number[::-1]
    # convert to integer list
    cc_num = [int(x) for x in cc_num]
    # double every second digit
    doubled_second_digit_list = list()
    digits = list(enumerate(cc_num, start=1))
    for index, digit in digits:
        if index % 2 == 0:
            doubled_second_digit_list.append(digit * 2)
        else:
            doubled_second_digit_list.append(digit)

    # add the digits if any number is more than 9
    doubled_second_digit_list = [sum_digits(x) for x in doubled_second_digit_list]
    # sum all digits
    sum_of_digits = sum(doubled_second_digit_list)
    # return True or False
    if sum_of_digits % 10 == 0:
        return True
    else:
        return False


def log_in():
    card_number = input("Enter your card number: ")
    pin = input("Enter your PIN: ")
    c.execute(f"SELECT * FROM card WHERE number={card_number}")
    test = c.fetchone()
    try:
        if card_number != str(test[1]) or pin != str(test[2]):
            print("Wrong card number or PIN!\n")
            return main()
        else:
            print("You have successfully logged in!")
            return user_view(card_number)
    except TypeError:
        print("Wrong card number or PIN!\n")
        return main()


def main():
    choice = input("1. Create an account\n2. Log into account\n0. Exit\n")
    if choice == '1':
        return create_account()
    elif choice == '2':
        return log_in()
    elif choice == '0':
        exit()


main()


conn1.close()
