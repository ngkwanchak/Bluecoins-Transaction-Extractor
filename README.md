# Bluecoins Transaction Extractor

A Python utility to extract all transactions from a Bluecoins Finance database file (*.fydb) and export them to CSV format.

## Overview

This tool provides a straightforward way to extract all transaction data from your Bluecoins database without any filtering, ensuring you get access to your complete financial history. The script uses LEFT JOINs to preserve all transaction data, regardless of whether related records exist in other tables.

## Features

- Extracts all transactions from the Bluecoins database
- Converts amounts to proper decimal values (Bluecoins stores amounts in millionths)
- Includes account, category, and transaction type information
- Provides status, deleted flag, and transfer metadata
- Includes debugging capabilities to help troubleshoot extraction issues
- Outputs transaction data as a clearly formatted CSV file

## Requirements

- Python 3.6 or higher
- pandas library (`pip install pandas`)

## Usage

### Basic Usage

```bash
python complete-transaction-extractor.py your_database.fydb
```

This will extract all transactions to a file named `all_transactions.csv` in the current directory.

### Specify Output File

```bash
python complete-transaction-extractor.py your_database.fydb custom_filename.csv
```

### Debug Database Structure

If you're experiencing issues or missing transactions, run the debug mode:

```bash
python complete-transaction-extractor.py your_database.fydb debug
```

This will print information about the database tables and sample transaction data to help diagnose problems.

## Output Format

The CSV file includes the following fields:

- `TransactionID`: Unique identifier for each transaction
- `Date`: Transaction date and time
- `Title`: Transaction description / item name
- `Amount`: Transaction amount (in actual decimal format)
- `Currency`: Transaction currency code
- `ConversionRate`: Currency conversion rate
- `Account`: Source account name
- `AccountType`: Type of account (e.g., Cash, Bank, Credit Card)
- `Category`: Transaction category
- `ParentCategory`: Parent category name
- `CategoryGroup`: Category group (e.g., Income, Expense)
- `TransactionType`: Type of transaction (e.g., Expense, Income, Transfer)
- `Notes`: Transaction notes
- `StatusCode`: Numeric status code
- `Status`: Human-readable status (Cleared, Pending, Void)
- `ToAccountID`: Target account ID for transfers
- `ToAccount`: Target account name for transfers
- `DeletedFlag`: Flag indicating if the transaction is deleted
- `TransferPairID`: ID linking paired transfer transactions
- `RecurringFlag`: Flag indicating if this is a recurring transaction
- `CreditCardInstallment`: Credit card installment information

## Locating Your Bluecoins Database

The Bluecoins database file (`.fydb`) is usually located in your device's storage at:

- Android: `/Android/data/com.rammigsoftware.bluecoins/files/`
- For exported backups: Look in your device's Download or Documents folder

## Notes

- The script works with any Bluecoins database version
- The export will include all transactions, including deleted ones (marked with the DeletedFlag)
- If you want to filter out deleted transactions, you can easily do so in a spreadsheet by filtering on `DeletedFlag != 6`
