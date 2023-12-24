import Expenses
import calendar
from datetime import datetime

def get_user_input():
    expense_date_str = input("Enter the date of expense (MM-DD-YYYY): ")
    expense_date = datetime.strptime(expense_date_str, '%m-%d-%Y').date()

    expense_name = input("What would you like to name this expense as? ")

    expense_amt = float(input("Enter the expense amount: $"))

    categories = ["Food", "Home", "Fun", "Work", "Misc"]
    print("Category options: " , categories)
    expense_category = input("What category would you like to consider this expense as? ")
    while expense_category not in categories:
        print("Sorry, that was not one of the options. Try again")
        expense_category = input("What category would you like to consider this expense as? ")

    new_expense = Expenses.expenses(expense_date, expense_name, expense_category, expense_amt)
    return new_expense

def write_expenses_toFile(fileName, expense):
    with open(fileName, "a") as file:
        file.write(f"{expense.date}, {expense.name}, {expense.category}, ${expense.amount}\n")

def summarize_expenses(fileName, budget):
    expensesList = []

    now = datetime.now()
    _, last_day = calendar.monthrange(now.year, now.month)
    remaining_days = last_day - now.day

    # makes a list of expenses from this month
    with open(fileName, "r") as file:
        lines = file.readlines()
        for line in lines:
            expense_date, expense_name, expense_category, expense_amount = line.split(",")
            # remove unnecesary characters in category and amount
            expense_category = expense_category.strip()
            expense_amount = expense_amount.strip(" $")
            if int(expense_date.split("-")[0]) == now.year and int(expense_date.split("-")[2]) == now.month:
                line_expense = Expenses.expenses(expense_date, expense_name, expense_category, float(expense_amount))
                expensesList.append(line_expense)
            else:
                continue
    
    amountByCat = {}
    categories = ["Food", "Home", "Fun", "Work", "Misc"]
    for element in categories:
        for expense in expensesList:
            key = element
            if key not in amountByCat and expense.category == key:
                amountByCat[key] = expense.amount
            elif key in amountByCat and expense.category == key:
                amountByCat[key] += expense.amount
            else:
                continue    

    print("Expenses by category for this month:")
    for key, amount in amountByCat.items():
        print(f"{key}: ${amount}")

    total_spent = sum([ex.amount for ex in expensesList])
    print(f"Total spent this month: ${total_spent: .2f}")

    budgetLeft = budget - total_spent
    print(f"Budget remaining for this month: ${budgetLeft :.2f}")

    

    dailyBudget = budgetLeft / remaining_days
    print(f"Budget per day for the rest of this month: ${dailyBudget:.2f}")

def main():
    print("Hello! Welcome to Expense Tracker App!")
    fileName = input("Please enter the CSV file's location: ")
    option = input("Would you like to enter an expense or see a summary of your expenses? Enter 1 to add expenses, enter 2 for summary: ")
    if option == "1":
        # Get user input for expense
        expense = get_user_input()
        print(expense)

        # Write their expenses to a file
        write_expenses_toFile(fileName, expense)

        # add another expense
        repeat = input("Would you like to add another expense? If yes, enter 'Y'. If not, enter any other key: ")
        while repeat.lower() == 'y':
            expense = get_user_input()
            print(expense)
            write_expenses_toFile(fileName, expense)
            repeat = input("Would you like to add another expense? If yes, enter 'Y'. If not, enter any other key: ")    
    elif option != "2":
        print("Invalid input. Try again")
        main()

    # Read file and summarize all expenses
    budget = int(input("What would you like to set as your budget for this month? "))
    summarize_expenses(fileName, budget)

main()