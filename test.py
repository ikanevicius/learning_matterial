import random


def input_to_float(question):
    """Ask for user input and checks if user input is a float."""
    other_symbols_found = []
    user_input = input(question)

    if len(user_input) == 1 and user_input[0] == '.':
        print("You must enter a value which has to be a number.")
        return

    for i in user_input:
        if i == ',':
            user_input = user_input.replace(',', '.')
        else:
            if i.isalpha() or i.isspace():
                other_symbols_found.append(i)
            else:
                pass

    if len(other_symbols_found) == 0:
        user_input = float(user_input)
        return user_input
    elif len(other_symbols_found) > 0:
        print("You must enter a value which has to be a number.")
        return


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

    def check_pin(self):
        """Asks to enter PIN code and checks if the entered PIN code is correct."""
        attempts_given = 3
        while attempts_given:
            pin_entered = int(input("Enter your PIN code: "))
            if pin_entered == self.pin_code:
                return
            elif pin_entered != self.pin_code:
                attempts_given -= 1
                print(f"PIN code entered wrong. Attempts left: {attempts_given}")

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
            ## TODO: Use 'pin_result' in order to stop program from further actions.

        money_added = input_to_float("How much money you want to add: ")
        self.balance = self.balance + money_added
        money_added_info = "+" + str(money_added) + "€"
        self.transactions.append(money_added_info)
        self.update_transactions()
        print(f"{money_added}€ added successfully!")

        return self.balance, self.transactions

    def take_money(self):
        pin_result = self.check_pin()
        if pin_result == 0:
            return pin_result

        money_taken = input_to_float("How much money you want to withdraw: ")
        if money_taken <= self.balance:
            if money_taken <= self.takeout_limit:
                self.balance = self.balance - money_taken
                money_taken_info = "-" + str(money_taken) + "€"
                self.transactions.append(money_taken_info)
                self.update_transactions()
                print(f"{money_taken}€ taken successfully!")
            elif money_taken > self.takeout_limit:
                print(f"Your can`t takeout more than {self.takeout_limit}€ at once.")
        elif money_taken > self.balance:
            print(f"""You don`t have enough money to withdraw {money_taken}€ from your account.""")

            return self.balance, self.transactions

    def change_takeout_limit(self):
        self.check_pin()
        set_new_limit = input_to_float("Enter your new takeout limit: ")
        ## TODO: Has to be changed into 'int' in future update.
        self.takeout_limit = set_new_limit

        print(f"""Your takeout limit was changed successfully!
You can now takeout up to {self.takeout_limit}€ at once.
""")
        return self.takeout_limit

    def change_pin(self):
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
                print(f"""Your PIN code was successfully changed! \nYour new PIN is {self.pin_code}.\n""")
                return attempts_given

            elif len(str(new_pin)) == 4 and new_pin == old_pin:
                print("New PIN code can`t bet the same as the old one.")
                attempts_given -= 1

            elif len(str(new_pin)) != 4:
                print("PIN code must contain 4 digits.")
                attempts_given -= 1

        print("You failed 3 times and can`t change the PIN code now.")
        return attempts_given


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
    print(f"""Dear {card.holder_name} {card.holder_surname}, your debit card was created successfully!
Your card number is {card.card_number}, PIN: {card.pin_code}.
You will be able to take no more than {card.takeout_limit}€ at once.
""")


def card_info(card):
    print(f"""___
Balance: {round(card.balance, 2)}€, 
Last 3 transactions made: {card.transactions}
""")


card_1 = create_new_card()
card_created_greet(card_1)
card_1.change_pin()
card_1.add_money()
card_1.take_money()
