import pandas as pd
import ast
import re
from ai import ai
import os
# TODO suggestion with ai
# TODO 02 remove 0, not , but . in betrag


# PART0: Load the environment variables
def load_env_variables(env_file):
    with open(env_file) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value


load_env_variables('env_file_template.env')

# Now you can access the environment variables using os.getenv
api_key = os.getenv('API_KEY')
regix_dict = os.getenv('REGIX_DICT')

YOUR_OPENAI_API_KEY = ""  # api_key

REGIX_DICT = ast.literal_eval(regix_dict)


"""

# PART1: Define the data transformation functions
#if you want to add a new category, you can add it to the dictionary like this:
# #{"CATEGORY":"REGIX"} #{"INSURANCE":"AOK"}
HINT: If you want to add "Cash" as a category, you can add it to the dictionary 
like this:#{"to_cash":"*UHR/wSBR*"}
"""


class Parser:
    pd.set_option('display.max_columns', None)  # or number of columns you want
    pd.set_option('display.expand_frame_repr', False)

    pd.set_option('display.max_rows', None)  # verwendung_dict = {"to_cash":"*UHR/wSBR*"}

    def __init__(self, parse_mode="CSV", file_path="to_parser/umsatz.CSV", account_name="Bank", to_csv=True):
        """
                Initialize the Parser object with the given parameters.

                Parameters:
                parse_mode (str): The mode to parse the data. Can be "CSV" or "Google Sheets".
                file_path (str): The path to the CSV file.
                account_name (str): The name of the account.
                to_csv (bool): Whether to save the result to a CSV file.
        """
        self.file_path = file_path
        self.df = pd.read_csv(self.file_path, delimiter=';', encoding='ISO-8859-1')
        self.REGIX_DICT = REGIX_DICT
        self.cashew_headers = ["FormattedDate", "Date", "Amount", "Category", "Title", "Note", "Account"]
        self.parse_mode = parse_mode
        self.to_csv = to_csv
        self.account_name = account_name

    def parse(self):
        """
               Parse the data based on the parse mode.

               Returns:
               DataFrame: The parsed data.

               Raises:
               ValueError: If the parse mode is not "CSV" or "Google Sheets".
               """
        if self.parse_mode == "CSV":
            d = self.refoctoring_to_csv()
            if self.to_csv:
                d.to_csv("to_parser/cashew.csv", index=False)
            return d
        elif self.parse_mode == "Google Sheets":
            d = self.refoctoring_to_google_sheets()
            if self.to_csv:
                d.to_csv("to_parser/cashew.csv", index=False)
            return d
        else:
            raise ValueError("Invalid parse mode. Please use 'CSV' or 'Google Sheets'.")

    @staticmethod
    def classify(row):
        """
            Classify a row of data based on the `REGIX_DICT`.

            This function takes a row of data and classifies it based on the `REGIX_DICT`.
            It returns the matched category.

            Parameters:
            row (Series): A row of data.

            Returns:
            str: The matched category.
        """
        for key, value in REGIX_DICT.items():
            s = str(row['Category_to_rewrite'])
            x = re.search(value, s, re.IGNORECASE)
            if x:
                return key
        return "I don't know"

    @staticmethod
    def classify2(row):
        """
            Classify a row of data based on the `REGIX_DICT` and return the matched group.

            This function takes a row of data and classifies it based on the `REGIX_DICT`. It returns the matched group.

            Parameters:
            row (Series): A row of data.

            Returns:
            str: The matched group.
        """
        for key, value in REGIX_DICT.items():
            s = str(row['Category_to_rewrite'])
            x = re.search(value, s, re.IGNORECASE)
            if x:
                return x.group()
            return ""

    def refoctoring_to_google_sheets(self):
        """
            Transform the DataFrame to match the Cashew format for Google Sheets.

            This function performs various transformations on the DataFrame, such as formatting dates,
            filling NaN values, and classifying data based on the `REGIX_DICT`.

            Returns:
            DataFrame: The transformed DataFrame.
        """
        # Perform any necessary data cleaning or transformation here
        df = self.df
        cashew_df = pd.DataFrame(columns=self.cashew_headers)
        cashew_df["date"] = df["Buchungstag"]
        df["Buchungstag"] = pd.to_datetime(df["Buchungstag"], format='%d.%m.%y')
        df["Buchungstag"] = df["Buchungstag"].dt.strftime('%Y-%m-%d')
        cashew_df["Date"] = df["Buchungstag"]
        cashew_df["Amount"] = df["Betrag"]
        #cashew_df = cashew_df.assign(Category=pd.Series(["I don't know"] * len(cashew_df)))
        cashew_df["Title"] = df["Buchungstext"]
        cashew_df["Note"] = df["Beguenstigter/Zahlungspflichtiger"]
        cashew_df["Account"] = self.account_name
        #swapped_dict = {value: key for key, value in REGIX_DICT.items()}

        cashew_df["Category_to_rewrite"] = df["Beguenstigter/Zahlungspflichtiger"] + " " + df["Verwendungszweck"]


        cashew_df['Category'] = cashew_df.apply(self.classify, axis=1)
        cashew_df['Title'] = cashew_df.apply(self.classify2, axis=1)
        del cashew_df['Category_to_rewrite']
        del cashew_df['date']
        #cashew_df['FormattedDate'] = cashew_df['date'] + " 00:00"
        cashew_df['Date'] = pd.to_datetime(cashew_df['Date'], format='%Y-%m-%d').dt.strftime('%m/%d/%y') + " 00:00"
        print(cashew_df["Date"])
        # Format the datetime object to '23-09-05 00:00')
        return cashew_df


    def refoctoring_to_csv(self):
        """
            Transform the DataFrame to match the Cashew format for CSV files.

            This function performs various transformations on the DataFrame, such as formatting dates, filling NaN values, and classifying data based on the `REGIX_DICT`.

            Returns:
            DataFrame: The transformed DataFrame.
        """
        #headers
        # date column del and date column add
        # df[formatted_date] = df[date] + " 00:00"


        # Perform any necessary data cleaning or transformation here
        df = self.df
        cashew_df = pd.DataFrame(columns=self.cashew_headers[1:-1])
        df["Buchungstag"] = pd.to_datetime(df["Buchungstag"], format='%d.%m.%y')
        df["Buchungstag"] = df["Buchungstag"].dt.strftime('%Y-%m-%d')
        cashew_df["Date"] = df["Buchungstag"]
        cashew_df["Amount"] = df["Betrag"]
        cashew_df = cashew_df.assign(Category=pd.Series(["I don't know"] * len(cashew_df)))
        cashew_df["Title"] = df["Buchungstext"]
        cashew_df["Note"] = df["Beguenstigter/Zahlungspflichtiger"].fillna("No note")
        cashew_df["Account"] = self.account_name
        # swapped_dict = {value: key for key, value in REGIX_DICT.items()}

        cashew_df["Category_to_rewrite"] = df["Beguenstigter/Zahlungspflichtiger"] + " " + df["Verwendungszweck"]


        cashew_df['Category'] = cashew_df.apply(self.classify, axis=1)
        cashew_df['Title'] = cashew_df.apply(self.classify2, axis=1)
        del cashew_df['Category_to_rewrite']
        # cashew_df['FormattedDate'] = cashew_df['date'] + " 00:00"
        cashew_df['Date'] = pd.to_datetime(cashew_df['Date'], format='%Y-%m-%d').dt.strftime('%m/%d/%y %H:%M:%S.%f')[:23]
        print(cashew_df["Date"])
        # Format the datetime object to '23-09-05 00:00')

        return cashew_df


        #cashew_df['Category'] = df['Beguenstigter/Zahlungspflichtiger'].replace(swapped_dict, regex=True)

if __name__ == "__main__":
    custom_prompt = f"Classify each data point from column 'Category_to_rewrite' into one of the following categories: {REGIX_DICT.keys()}. "\
                    "Then, update the data point with the assigned category, " \
                    "based on the information available about the data point." \

    user_message = "Make it a python dict in the following form {category: REGIX TO FIND}. " \
                    "Return only dict, no words more than dict."

    if YOUR_OPENAI_API_KEY:
        categorys = ai(custom_prompt,user_message, api_key=YOUR_OPENAI_API_KEY)
        REGIX_DICT = dict(categorys)

    parser = Parser()
    df = parser.parse()

    print(df.head(40))