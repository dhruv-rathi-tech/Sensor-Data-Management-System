import pandas as pd
import numpy as np
import oracledb
import os

class DataProcessor:
    def __init__(self, csv_file_path="dataset.csv", processed_file_path="processed_dataset.csv"):
        self.csv_file_path = csv_file_path
        self.processed_file_path = processed_file_path
        self.raw_data = None
        self.processed_data = None

    def load_raw_data(self):
        """Load raw CSV into memory."""
        try:
            self.raw_data = pd.read_csv(self.csv_file_path)
            print(f"✅ Loaded {len(self.raw_data)} rows, {len(self.raw_data.columns)} columns from {self.csv_file_path}")
            return True
        except Exception as e:
            print(f"❌ Error loading CSV '{self.csv_file_path}': {e}")
            return False

# preprocessing
    def process_data(self):
        """Process:
           - keep first 6 columns
           - remove rows containing null values
           - remove rows that have any data in columns after the 6th
           - drop duplicate rows
           - save processed CSV
        """
        if self.raw_data is None:
            print("⚠️ raw_data is None — call load_raw_data() first")
            return False

        df_full = self.raw_data
        n_cols = df_full.shape[1]

        if n_cols < 6:
            df_first6 = df_full.copy()
            if n_cols == 6:
                df_first6.columns = ["Date", "Time", "Sensor_ID", "State", "Temp", "Humidity"]
        else:
            df_first6 = df_full.iloc[:, :6].copy()
            df_first6.columns = ["Date", "Time", "Sensor_ID", "State", "Temp", "Humidity"]

        rows_removed_for_extras = 0
        if n_cols > 6:
            extras = df_full.iloc[:, 6:].copy()
            extras_replace = extras.replace(r'^\s*$', np.nan, regex=True)
            mask_rows_with_extra_data = extras_replace.notna().any(axis=1)

            rows_with_extra = mask_rows_with_extra_data.sum()
            if rows_with_extra > 0:
                df_first6 = df_first6.loc[~mask_rows_with_extra_data].reset_index(drop=True)
                rows_removed_for_extras = int(rows_with_extra)

        before_dup = len(df_first6)
        df_first6 = df_first6.drop_duplicates().reset_index(drop=True)
        duplicates_removed = before_dup - len(df_first6)

        try:
            df_first6.to_csv(self.processed_file_path, index=False)
            print(f"💾 Processed dataset saved as '{self.processed_file_path}'")
        except PermissionError:
            alt = "processed_dataset_clean.csv"
            df_first6.to_csv(alt, index=False)
            print(f"⚠️ PermissionError writing '{self.processed_file_path}'. Saved to '{alt}' instead.")

        self.processed_data = df_first6

        print("📊 Processing summary:")
        print(f"  - Original rows: {len(self.raw_data)}")
        if n_cols > 6:
            print(f"  - Rows removed because extras (col>6) had data: {rows_removed_for_extras}")
        print(f"  - Duplicate rows removed: {duplicates_removed}")
        print(f"  - Final rows saved: {len(self.processed_data)}")
        return True

    def get_processed_data(self):
        return self.processed_data


def load_into_oracle(processed_csv):
    """Load processed dataset into Oracle DB."""
    oracledb.init_oracle_client(
        lib_dir=r"C:\oraclexe\instantclient-basic-windows.x64-23.9.0.25.07\instantclient_23_9"
    )

    try:
        connection = oracledb.connect(
            user="system",
            password="dhruv",
            dsn="localhost/XE"
        )
        print("✅ Connected to Oracle Database")
    except Exception as e:
        print("❌ Connection failed:", e)
        return

    cursor = connection.cursor()

    df = pd.read_csv(processed_csv)
    df = df.dropna(how="all")
    df = df[~(df.astype(str).apply(lambda x: x.str.strip() == '').all(axis=1))]

    print("✅ Dataset loaded and cleaned")
    print(df.head())

    df["Date"] = df["Date"].astype(str)
    df["Time"] = df["Time"].astype(str)
    df["Sensor_ID"] = df["Sensor_ID"].astype(str)
    df["State"] = df["State"].astype(str)
    df["Temp"] = df["Temp"].fillna(0).astype(int)
    df["Humidity"] = df["Humidity"].fillna(0).astype(int)

    try:
        cursor.execute("DROP TABLE processed_data PURGE")
    except:
        print("ℹ️ No existing table found")

    cursor.execute("""
        CREATE TABLE processed_data (
            Date_Col   VARCHAR2(20),
            Time_Col   VARCHAR2(30),
            Sensor_ID  VARCHAR2(20),
            State      VARCHAR2(20),
            Temp       NUMBER,
            Humidity   NUMBER
        )
    """)
    print("✅ Table created: processed_data")

    cursor.executemany("""
        INSERT INTO processed_data (Date_Col, Time_Col, Sensor_ID, State, Temp, Humidity)
        VALUES (:1, :2, :3, :4, :5, :6)
    """, df.values.tolist())

    connection.commit()
    print("✅ Data inserted successfully")

    cursor.execute("SELECT COUNT(*) FROM processed_data")
    count = cursor.fetchone()[0]
    print(f"📊 Total rows inserted: {count}")

    cursor.close()
    connection.close()
    print("🔒 Connection closed")


if __name__ == "__main__":
    raw_file = os.path.join("D:\\dbms_project_2\\data", "dataset.csv")
    processed_file = os.path.join("D:\\dbms_project_2\\data", "processed_dataset.csv")

    processor = DataProcessor(csv_file_path=raw_file, processed_file_path=processed_file)

    if processor.load_raw_data() and processor.process_data():
        load_into_oracle(processed_file)
