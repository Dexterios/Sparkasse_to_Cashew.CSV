import re

import pandas as pd
import ast

with open('to_parser/.gitignore', 'a') as f:
    f.write('to_parser/*\n')

REGIX_DICT = {}
"""
REGIX_DICT = {
CATEGORY : REGIXREGIX
CATEGORY : REGIXREGIX
CATEGORY : REGIXREGIX
CATEGORY : REGIXREGIX
CATEGORY : REGIXREGIX
CATEGORY : REGIXREGIX
CATEGORY : REGIXREGIX
CATEGORY : REGIXREGIX
CATEGORY : REGIXREGIX
CATEGORY : REGIXREGIX
CATEGORY : REGIXREGIX
CATEGORY : REGIXREGIX
CATEGORY : REGIXREGIX
CATEGORY : REGIXREGIX
}
"""
'''

# PART1: Define the data transformation functions
#if you want to add a new category, you can add it to the dictionary like this:
# #{"CATEGORY":"REGIX"} #{"INSURANCE":"AOK"}

HINT: If you want to add "Cash" as a category, you can add it to the dictionary 
like this:#{"to_cash":"*UHR/wSBR*"}
'''

cashew_headers = ["FormattedDate","Date","Amount","Category","Title","Note","Account"]
pd.set_option('display.max_columns', None)  # or number of columns you want
pd.set_option('display.expand_frame_repr', False)

pd.set_option('display.max_rows', None)
verwendung_dict = {"to_cash":"*UHR/wSBR*"}
def parse_sparkasse_csv(file_path = "to_parser/umsatz.CSV"):
    # Read the CSV file
    df = pd.read_csv(file_path, delimiter=';', encoding='ISO-8859-1')

    # Perform any necessary data cleaning or transformation here

    return df
"""
WAIT FOR AN UODATE
def categorize(df):
    # Perform any necessary data cleaning or transformation here
    return df"""
def regix_dict_filler(regix_dict = REGIX_DICT):
    REGIX_DICT= regix_dict
    return REGIX_DICT
def refoctoring(df, deposit_name = 'Bank'):
    # Perform any necessary data cleaning or transformation here

    cashew_df = pd.DataFrame(columns=cashew_headers)
    cashew_df["date"] = df["Buchungstag"]
    df["Buchungstag"] = pd.to_datetime(df["Buchungstag"], format='%d.%m.%y')
    df["Buchungstag"] = df["Buchungstag"].dt.strftime('%Y-%m-%d')
    cashew_df["Date"] = df["Buchungstag"]
    cashew_df["Amount"] = df["Betrag"]
    cashew_df = cashew_df.assign(Category=pd.Series(["I don't know"] * len(cashew_df)))
    cashew_df["Title"] = df["Buchungstext"]
    cashew_df["Note"] = df["Beguenstigter/Zahlungspflichtiger"]
    cashew_df["Account"] = deposit_name
    #swapped_dict = {value: key for key, value in REGIX_DICT.items()}

    cashew_df["Category_to_rewrite"] = df["Beguenstigter/Zahlungspflichtiger"] + " " + df["Verwendungszweck"]
    import re
    def classify(row):
        for key, value in REGIX_DICT.items():
            s = str(row['Category_to_rewrite'])
            x = re.search(value, s, re.IGNORECASE)
            if x:
                return key
        return "I don't know"

    def classify2(row):
        for key, value in REGIX_DICT.items():
            s = str(row['Category_to_rewrite'])
            x = re.search(value, s, re.IGNORECASE)
            if x:
                return x.group()
            return ""

    cashew_df['Category'] = cashew_df.apply(classify, axis=1)
    cashew_df['Title'] = cashew_df.apply(classify2, axis=1)
    del cashew_df['Category_to_rewrite']

    cashew_df['FormattedDate'] = pd.to_datetime(cashew_df['date'], format='%d.%m.%y').dt.strftime('%d-%m-%y') + " 00:00"
    #cashew_df['FormattedDate'] = cashew_df['date'] + " 00:00"

    # Format the datetime object to '23-09-05 00:00')

    #cashew_df['Category'] = df['Beguenstigter/Zahlungspflichtiger'].replace(swapped_dict, regex=True)
    return cashew_df
if __name__ == "__main__":
    custom_prompt = (f"Classify each data point from column 'Category_to_rewrite' into one of the following categories: {REGIX_DICT.keys()}. "
                     f"Then, update the data point with the assigned category, "
                     "based on the information available about the data point.")

    df = parse_sparkasse_csv()
    nd = refoctoring(df)

    nd.to_csv("to_parser/cashew.csv", index=False)
    print(nd.head(40))