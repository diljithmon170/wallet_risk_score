# 🛡️ Wallet Risk Scoring From Scratch

This project computes a **risk score (0–1000)** for Ethereum wallet addresses based on their on-chain activity with the **Compound V2** lending protocol. It was developed as part of an assignment to assess lending behavior and wallet creditworthiness using on-chain data.

---

## 📌 Objective

- Fetch historical transaction data for 100 given wallet addresses from the **Compound V2** protocol.
- Engineer meaningful features from on-chain borrow, repay, and liquidation events.
- Use these features to assign a **wallet risk score** from 0 (highest risk) to 1000 (lowest risk).
- Output a final CSV containing each wallet and its corresponding risk score.

---

## 🛠️ Tools & Libraries Used

- [Python 3](https://www.python.org/)
- [The Graph API](https://thegraph.com/) (Compound V2 Subgraph)
- `pandas`
- `requests`
- `tqdm`

---

## 📂 Project Structure

