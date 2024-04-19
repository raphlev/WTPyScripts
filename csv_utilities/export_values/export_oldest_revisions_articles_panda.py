import pandas as pd
import argparse
from datetime import datetime

def parse_date(date_str):
    """Parse the date using datetime.strptime, return None if parsing fails."""
    try:
        return datetime.strptime(date_str, "%d-%b-%Y %H:%M:%S")
    except ValueError:
        return None

def main(input_file, output_file):
    df = pd.read_csv(input_file, delimiter="|", encoding="utf-8", dtype={"Revision": str})
    
    # Convert "Date Validation" column to datetime, handling errors with 'coerce'
    # df["Date Validation"] = pd.to_datetime(df["Date Validation"], errors='coerce', format="%d-%b-%Y %H:%M:%S")
    # Year Support in pandas: pandas relies on NumPy for dates and times, which typically handles dates in the range [1677-09-21, 2262-04-11], due to its use of 64-bit integers to represent nanosecond timestamps. A date like "11-MAY-1017" is far outside this range, leading to the NaT result because it cannot be represented as a pandas datetime64 type.    
    # Apply the custom parse_date function to the "Date Validation" column
    df["Date Validation"] = df["Date Validation"].apply(lambda x: parse_date(x) if pd.notnull(x) else None)
    
    # Filter out rows where "Date Validation" could not be parsed (i.e., is None)
    df = df.dropna(subset=["Date Validation"])
    
    # Now that dates are parsed, sort by "Reference" and "Date Validation"
    df.sort_values(by=["Reference", "Date Validation"], inplace=True)
    
    # Select the first (oldest) entry per "Reference"
    df_oldest = df.drop_duplicates(subset="Reference", keep='first')
    
    # Extract unique revisions, ensuring no duplicates, and sort
    unique_revisions = df_oldest["Revision"].drop_duplicates().sort_values()

    # Export the revisions to a CSV file
    unique_revisions.to_frame(name="Revision").to_csv(output_file, index=False, encoding="utf-8", header=True)

    print(f"Exported unique, oldest revisions to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export unique, oldest revisions based on the oldest 'Date Validation'.")
    parser.add_argument('-i', '--input_file', required=True, help="Path to the input CSV file.", type=str)
    parser.add_argument('-o', '--output_file', required=True, help="Path to the output CSV file.", type=str)
    args = parser.parse_args()

    main(args.input_file, args.output_file)
