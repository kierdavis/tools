from __future__ import print_function


def command(args):
    import os
    from subprocess import check_call
    import sys

    import sr.tools.spending as spending
    from sr.tools.budget import BudgetTree

    root = spending.find_root()
    budget = spending.load_budget_with_spending(root)
    line = budget.path(args.budgetline)

    if isinstance(line, BudgetTree):
        print("Summary for tree", args.budgetline)
        budgeted = sum([x.cost for x in line.walk()])
        spent = sum([x.spent for x in line.walk()])
    else:
        print("Summary for line", args.budgetline)
        budgeted = line.cost
        spent = line.spent

    print("Budgeted:\t", budgeted)
    print("Spent:\t\t", spent)

    if spent > budgeted:
        print("OVER BUDGET")

    print("Transactions:")

    line = args.budgetline.replace("/", ":")
    if line[0] == ":":
        line = account[1:]

    check_call(["ledger",
                "--file", os.path.join(root, "spending.dat"),
                "reg", "Expenses:{0}".format(line)])


def add_subparser(subparsers):
    parser = subparsers.add_parser('sp-line', help='Inspect a spending line.')
    parser.add_argument("budgetline", help="The budget line to inspect")
    parser.set_defaults(func=command)
