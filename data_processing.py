import pandas as pd
import os

# Set your data folder path
DATA_DIR = "data"  # Put your unzipped CSV files here

# Indicators and the World Bank CSV file names (you can adjust these)
files = {
    "GDP (US$)": "API_NY.GDP.MKTP.CD_DS2_en_csv_v2_5708.csv",
    "GDP per Capita (US$)": "API_NY.GDP.PCAP.CD_DS2_en_csv_v2_5826.csv",
    "Inflation (%)": "API_FP.CPI.TOTL.ZG_DS2_en_csv_v2_5747.csv",
    "Oil Rents (% of GDP)": "API_NY.GDP.PETR.RT.ZS_DS2_en_csv_v2_17224.csv",
    "Population": "API_SP.POP.TOTL_DS2_en_csv_v2_5830.csv"
}


def load_indicator(file_path, indicator_name):
    df = pd.read_csv(file_path, skiprows=4)
    df = df[df["Country Name"] == "Saudi Arabia"]
    df = df.drop(columns=["Country Name", "Country Code",
                 "Indicator Name", "Indicator Code"])
    df = df.melt(var_name="Year", value_name=indicator_name)
    df["Year"] = df["Year"].astype(str)
    return df


def merge_indicators():
    merged_df = None

    for indicator, file_name in files.items():
        file_path = os.path.join(DATA_DIR, file_name)
        indicator_df = load_indicator(file_path, indicator)

        if merged_df is None:
            merged_df = indicator_df
        else:
            merged_df = pd.merge(merged_df, indicator_df,
                                 on="Year", how="outer")

    # Clean
    merged_df = merged_df.dropna()
    merged_df = merged_df.sort_values(by="Year")
    merged_df.to_csv("final_data.csv", index=False)
    print("✅ Data merged and saved to final_data.csv")


if __name__ == "__main__":
    merge_indicators()
