from sqlite3 import connect
import csv
import sys
import os
import pandas as pd

def extract_all_transactions(dbname, output_file="all_transactions.csv"):
    """
    Extract ALL transactions from Bluecoins database without any filtering
    """
    if not os.path.isfile(dbname):
        print(f"Error: Database file '{dbname}' does not exist.")
        sys.exit(1)
    
    try:
        with connect(dbname) as conn:
            # Get transaction count first to verify
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM TRANSACTIONSTABLE")
            total_count = cursor.fetchone()[0]
            print(f"Total transactions in database: {total_count}")
            
            # Comprehensive query with LEFT JOINs to prevent data loss
            query = """
            SELECT 
                T.transactionsTableID as TransactionID,
                T.date as Date,
                I.itemName as Title,
                (CAST(T.amount AS float) / 1000000.0) as Amount,
                T.transactionCurrency as Currency,
                T.conversionRateNew as ConversionRate,
                A.accountName as Account,
                AT.accountTypeName as AccountType,
                C.childCategoryName as Category,
                P.parentCategoryName as ParentCategory,
                CG.categoryGroupName as CategoryGroup,
                TT.transactionTypeName as TransactionType,
                T.notes as Notes,
                T.status as StatusCode,
                T.accountReference as ToAccountID,
                A2.accountName as ToAccount,
                T.deletedTransaction as DeletedFlag,
                T.uidPairID as TransferPairID,
                T.reminderTransaction as RecurringFlag,
                T.creditCardInstallment as CreditCardInstallment
            FROM TRANSACTIONSTABLE as T
            LEFT JOIN ITEMTABLE as I ON T.itemID = I.itemTableID
            LEFT JOIN ACCOUNTSTABLE as A ON T.accountID = A.accountsTableID
            LEFT JOIN ACCOUNTTYPETABLE as AT ON A.accountTypeID = AT.accountTypeTableID
            LEFT JOIN CHILDCATEGORYTABLE as C ON T.categoryID = C.categoryTableID
            LEFT JOIN PARENTCATEGORYTABLE as P ON C.parentCategoryID = P.parentCategoryTableID
            LEFT JOIN CATEGORYGROUPTABLE as CG ON P.categoryGroupID = CG.categoryGroupTableID
            LEFT JOIN TRANSACTIONTYPETABLE as TT ON T.transactionTypeID = TT.transactionTypeTableID
            LEFT JOIN ACCOUNTSTABLE as A2 ON T.accountReference = A2.accountsTableID
            ORDER BY T.date DESC
            """
            
            # Execute query and save to CSV
            df = pd.read_sql_query(query, conn)
            
            # Add human-readable status
            df['Status'] = df['StatusCode'].map({
                0: 'Cleared',
                1: 'Pending',
                2: 'Void'
            }).fillna('Unknown')
            
            # Save to CSV
            df.to_csv(output_file, index=False)
            
            # Print verification counts and preview
            print(f"Successfully exported {len(df)} transactions to {output_file}")
            print(f"Filtered by deleted flag: {len(df[df['DeletedFlag'] != 6])} transactions")
            
            print("\nPreview of first 5 transactions:")
            preview_columns = ['TransactionID', 'Date', 'Title', 'Amount', 'Currency', 
                              'Account', 'Category', 'TransactionType', 'Status']
            print(df[preview_columns].head(5).to_string())
            
            print("\nPreview of last 5 transactions:")
            print(df[preview_columns].tail(5).to_string())
            
            # Analysis of potentially missing transactions
            if len(df) < total_count:
                print(f"\nWARNING: Only extracted {len(df)} of {total_count} transactions!")
                
                # Check for NULL values in key fields that might cause joins to fail
                null_counts = df.isnull().sum()
                print("\nNull value counts in key fields:")
                for col in ['Title', 'Account', 'Category', 'TransactionType']:
                    if col in null_counts:
                        print(f"  {col}: {null_counts[col]}")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def debug_database_structure(dbname):
    """
    Function to help debug database structure - prints table counts and sample data
    """
    try:
        with connect(dbname) as conn:
            cursor = conn.cursor()
            
            # Get list of all tables and their row counts
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            print("\n==== DATABASE STRUCTURE DEBUG INFO ====")
            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"{table_name}: {count} rows")
            
            # Sample direct query on transaction table
            print("\nDirect TRANSACTIONSTABLE query (first 3 rows):")
            cursor.execute("SELECT transactionsTableID, date, amount, transactionTypeID, deletedTransaction FROM TRANSACTIONSTABLE LIMIT 3")
            for row in cursor.fetchall():
                print(row)
                
    except Exception as e:
        print(f"Debug error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        dbname = sys.argv[1]
    else:
        dbname = "bluecoins.fydb"
    
    if len(sys.argv) > 2:
        command = sys.argv[2]
        if command == "debug":
            # Run debug function to check database structure
            debug_database_structure(dbname)
        else:
            output_file = sys.argv[2]
            extract_all_transactions(dbname, output_file)
    else:
        # Normal extraction
        extract_all_transactions(dbname)
