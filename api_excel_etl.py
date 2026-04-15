import pandas as pd
import requests

try:
    # EXTRACT 1: Excel
    df_excel = pd.read_excel("employees.xlsx")
    print("Employee Excel Data")
    print(df_excel)

    # EXTRACT 2: API
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("API request failed")

    data = response.json()
    df_api = pd.DataFrame(data)

    # TRANSFORM API (extract city)
    df_api["city"] = df_api["address"].apply(lambda x: x["city"])

    # Keep only needed columns
    df_api = df_api[["id", "email", "city"]]

    # RENAME for merging
    df_api.rename(columns={"id": "employee_id"}, inplace=True)

    # MERGE (IMPORTANT STEP)
    df_final = pd.merge(df_excel, df_api, on="employee_id", how="left")
    print("Employee Merge Data")
    print(df_final)
    # TRANSFORM FINAL
    df_final["salary"] = df_final["salary"] * 1.10
    df_final["bonus"] = df_final["salary"] * 0.05
    df_final["department"] = df_final["department"].str.upper()

    print("Final Data:")
    print(df_final)

    # LOAD
    df_final.to_csv("final_combined_data.csv", index=False)

    print("\n✅ API + Excel ETL Completed")

except Exception as e:
    print("❌ Error:", e)