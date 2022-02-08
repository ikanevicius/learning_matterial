import random


def ask_input_float(question):
    """Ask for user input and checks if user input is a float.
    If The input is incorrect, the function returns '0'."""

    user_input = input(question)
    user_input = user_input.replace(' ', '')
    user_input = user_input.replace(',', '.')
    if user_input.count(".") > 1:
        print("\n"
              "TYPE ERROR.\n"
              "You can`t use more than one dot (ether ',' or '.' to separate decimals.\n"
              " ")
        return 0

    numbers = []
    for i in user_input:
        if i.isnumeric() or i == ".":
            numbers.append(i)
        else:
            continue

    if len(numbers) == len(user_input):
        user_input = float(user_input)
        user_input = round(user_input, 2)
        # TODO: In future only numbers with two decimals could be added.
        return user_input
    else:
        print("\n"
              "TYPE ERROR. \n"
              "Your input must be a number.\n"
              " ")
        return 0


def ask_input_int(question):
    """Ask for user input and checks if user input is an integer.
    If The input is incorrect, the function returns '0'."""

    user_input = input(question)
    user_input = user_input.replace(' ', '')

    if user_input.isnumeric():
        user_input = int(user_input)
        return user_input
    else:
        print("\n"
              "TYPE ERROR. \n"
              "Your input must be a number and can`t have decimals.\n"
              " ")
        return 0


class DebitCard:
    def __init__(
            self,
            card_number,
            pin_code,
            holder_name,
            holder_surname,
            balance,
            takeout_limit,
            transactions
    ):

        self.card_number = card_number
        self.pin_code = int(pin_code)
        self.holder_name = holder_name
        self.holder_surname = holder_surname
        self.balance = float(round(balance, 2))
        self.takeout_limit = int(takeout_limit)
        self.transactions = transactions

    def lobby(self):
        user_input = input("""___
Your orders: """)
        if user_input == "0":
            self.card_info()
            self.lobby()
        elif user_input == "1":
            self.add_money()
            self.lobby()
        elif user_input == "2":
            self.change_pin()
            self.lobby()
        elif user_input == "3":
            self.take_money()
            self.lobby()
        elif user_input == "4":
            self.change_takeout_limit()
            self.lobby()
        elif user_input == "x":
            print(f"""PROGRAM HAS BEEN STOPPED.
Have a nice day, {self.holder_name}!""")
        else:
            self.lobby()

    def check_pin(self):
        """Asks to enter PIN code and checks if the entered PIN code is correct.
        If PIN was entered wrong 3 times, the function returns '0'."""

        attempts_given = 3
        while attempts_given:
            pin_entered = input("Enter your PIN code: ")

            if len(pin_entered) == 4 and pin_entered.isnumeric():
                pin_entered = int(pin_entered)

                if pin_entered != self.pin_code:
                    attempts_given -= 1
                    print(f"""TYPE ERROR.
PIN code entered wrong. Attempts left: {attempts_given}
""")
                else:
                    return

            else:
                attempts_given -= 1
                print(f"""TYPE ERROR.
PIN code entered wrong. Attempts left: {attempts_given}
""")

        print("You failed 3 times and can`t continue.")
        return int(attempts_given)

    def update_transactions(self):
        """Checks transactions history and makes sure not more than 5 would be kept."""

        while len(self.transactions) > 5:
            self.transactions.pop(0)

    def add_money(self):
        pin_result = self.check_pin()
        if pin_result == 0:
            return pin_result
            # TODO: Use 'pin_result' in order to stop program from further actions.

        money_added = ask_input_float("How much money you want to add: ")
        if money_added == 0:
            print()
            # TODO: Has to be changed in future.
        else:
            self.balance = self.balance + money_added
            money_added_info = "+" + str(money_added) + "€"
            self.transactions.append(money_added_info)
            self.update_transactions()
            print(f"""{money_added}€ added successfully!
""")

            return self.balance, self.transactions

    def take_money(self):
        pin_result = self.check_pin()
        if pin_result == 0:
            return pin_result

        money_taken = ask_input_float("How much money you want to withdraw: ")
        if money_taken <= self.balance:
            if money_taken <= self.takeout_limit:
                self.balance = self.balance - money_taken
                money_taken_info = "-" + str(money_taken) + "€"
                self.transactions.append(money_taken_info)
                self.update_transactions()
                print(f"""{money_taken}€ taken successfully!
""")
            elif money_taken > self.takeout_limit:
                print(f"""
TAKEOUT LIMIT EXCEEDED.
Your can`t takeout more than {self.takeout_limit}€ at once.
""")
        elif money_taken > self.balance:
            print(f"""
NOT ENOUGH MONEY.
You don`t have enough money to withdraw {money_taken}€ from your account.
""")

            return self.balance, self.transactions

    def change_takeout_limit(self):
        self.check_pin()
        set_new_limit = ask_input_int("Enter your new takeout limit: ")
        if set_new_limit == 0:
            print()
            # TODO: Has to be changed in future.
        else:
            self.takeout_limit = set_new_limit

        print(f"""Your takeout limit was changed successfully!
You can now takeout up to {self.takeout_limit}€ at once.
""")
        return self.takeout_limit

    def change_pin(self):
        """If PIN was entered wrong 3 times, function returns '0'."""

        attempts_given = 3
        while attempts_given:
            old_pin = int(input("Enter your old PIN code: "))

            if old_pin != self.pin_code:
                print(f"Old PIN code was entered wrong. Please try again.")
                attempts_given -= 1
                continue

            new_pin = int(input("Enter your new PIN code: "))
            if len(str(new_pin)) == 4 and new_pin != old_pin:
                self.pin_code = new_pin
                print(f"""Your PIN code was successfully changed!
Your new PIN is {self.pin_code}.
""")
                return attempts_given

            elif len(str(new_pin)) == 4 and new_pin == old_pin:
                print("New PIN code can`t bet the same as the old one.")
                attempts_given -= 1

            elif len(str(new_pin)) != 4:
                print("PIN code must contain 4 digits.")
                attempts_given -= 1

        print("You failed 3 times and can`t change the PIN code now.")
        return attempts_given

    def card_info(self):
        print(f"""Balance: {round(self.balance, 2)}€, 
Last 3 transactions made: {self.transactions}
""")


def create_new_card():
    card_number = int(random.uniform(1000000, 9999999))
    pin_code = int(random.uniform(1000, 9999))
    holder_name = input("Enter card holder name: ")
    holder_surname = input("Enter card holder surname: ")
    balance = 0
    takeout_limit = 250
    transactions = []

    card_created = DebitCard(
        card_number,
        pin_code,
        holder_name,
        holder_surname,
        balance,
        takeout_limit,
        transactions
    )

    return card_created


def card_created_greet(card):
    print(f"""
Dear {card.holder_name} {card.holder_surname}, your debit card was created successfully!
Your card number is {card.card_number}, PIN: {card.pin_code}.
You will be able to take no more than {card.takeout_limit}€ at once.
""")


card_1 = create_new_card()
card_created_greet(card_1)
card_1.lobby()
