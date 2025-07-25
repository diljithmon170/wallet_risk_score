import pandas as pd
import requests
from tqdm import tqdm

# === STEP 1: Load wallet addresses from downloaded CSV ===
# Assumes the CSV has a column called 'wallet_id'
wallet_csv_path = "wallets.csv"  # Replace with your actual file path
wallets_df = pd.read_csv(wallet_csv_path)
wallets = wallets_df["wallet_id"].dropna().unique().tolist()

# === STEP 2: Query The Graph for Compound V2 ===
GRAPH_URL = "https://api.thegraph.com/subgraphs/name/graphprotocol/compound-v2"

def fetch_compound_data(wallet):
    query = """
    {
      borrowEvents(where: {borrower: "%s"}, first: 1000) {
        amount
        blockTimestamp
      }
      repayEvents(where: {borrower: "%s"}, first: 1000) {
        amount
        blockTimestamp
      }
      liquidationEvents(where: {borrower: "%s"}, first: 1000) {
        amountRepay
        blockTimestamp
      }
    }
    """ % (wallet.lower(), wallet.lower(), wallet.lower())

    try:
        response = requests.post(GRAPH_URL, json={"query": query})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {wallet}: {e}")
        return None

# === STEP 3: Feature Engineering and Scoring ===
def extract_features(data):
    if data is None or "data" not in data:
        return {"score": 0}

    borrows = data["data"].get("borrowEvents", [])
    repays = data["data"].get("repayEvents", [])
    liquidations = data["data"].get("liquidationEvents", [])

    total_borrow = sum(float(event["amount"]) for event in borrows)
    total_repay = sum(float(event["amount"]) for event in repays)
    liquidation_count = len(liquidations)

    repay_ratio = total_repay / total_borrow if total_borrow > 0 else 1.0

    return {
        "total_borrow": total_borrow,
        "total_repay": total_repay,
        "repay_ratio": repay_ratio,
        "liquidation_count": liquidation_count,
        "score": compute_score(repay_ratio, liquidation_count)
    }

def compute_score(repay_ratio, liquidation_count):
    repay_score = min(repay_ratio, 1.0) * 400  # good repay = high score
    liquidation_score = max(0, (3 - liquidation_count)) / 3 * 300  # fewer liquidations = better
    base_score = 300  # base score for being active

    final_score = repay_score + liquidation_score + base_score
    return min(1000, int(final_score))

# === STEP 4: Run for All Wallets ===
results = []

print("Fetching data and scoring wallets...")

for wallet in tqdm(wallets):
    data = fetch_compound_data(wallet)
    features = extract_features(data)
    results.append({
        "wallet_id": wallet,
        "score": features["score"]
    })

# === STEP 5: Save as CSV ===
output_path = "wallet_risk_scores.csv"
df = pd.DataFrame(results)
df.to_csv(output_path, index=False)

print(f"\n✅ Risk scoring completed. File saved as '{output_path}'.")
