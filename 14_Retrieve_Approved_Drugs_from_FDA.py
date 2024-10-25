import pandas as pd
import streamlit as st

st.title("Retrieve FDA Approved Drugs")

start_year = st.number_input("Enter Start Year", min_value=2000, max_value=2024, value=2021)
end_year = st.number_input("Enter End Year", min_value=2000, max_value=2024, value=2023)

if start_year > end_year:
    st.error("Start year must be less than or equal to the end year.")
else:
    years = range(start_year, end_year + 1)
    combined_data = pd.DataFrame()

    progress_bar = st.progress(0)
    total_years = len(years)

    for i, year in enumerate(years):
        year_str = str(year)
        url = f"https://www.fda.gov/drugs/new-drugs-fda-cders-new-molecular-entities-and-new-therapeutic-biological-products/novel-drug-approvals-{year_str}"

        try:
            df = pd.read_html(url)
            df1 = df[0]
            df1['Approval Year'] = year_str
            combined_data = pd.concat([combined_data, df1], ignore_index=True)
            st.success(f"Data for {year_str} retrieved successfully.")
        except Exception as e:
            st.warning(f"Failed to retrieve data for {year_str}: {e}")

        progress_bar.progress((i + 1) / total_years)

    if not combined_data.empty:
        combined_data.to_excel("FDA_Approved_Novel_Drug_All_Years.xlsx", index=False)
        st.success("All data combined into 'FDA_Approved_Novel_Drug_All_Years.xlsx'.")
        st.dataframe(combined_data)

