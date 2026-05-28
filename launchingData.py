import pandas as pd

# Read history.json and parse timestamps
def load_dataframe():
    df = pd.read_json("history.json")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df.sort_values("timestamp").reset_index(drop=True)

if __name__ == "__main__":
    df = load_dataframe()
    print(df.tail(10).to_string(index=False))
    print(f"\nMean: {df['ram_percent'].mean():.2f}%  "
          f"Min: {df['ram_percent'].min():.2f}%  "
          f"Max: {df['ram_percent'].max():.2f}%")