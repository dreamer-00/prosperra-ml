# Kubyra ML Engine

The intelligence layer behind Kubyra's investment allocation system.
Replaces static hardcoded allocations with personalized splits 
driven by real user spending behavior.

---

## What this does

Most micro-investing apps give every user the same allocation.
Kubyra's ML engine analyzes how you actually spend money and 
builds a risk profile unique to you.

Someone who spends mostly on groceries and bills gets a 
conservative portfolio.
Someone spending on dining, travel, and entertainment gets 
an aggressive one.

---

## Pipeline

```
UPI Transaction
      ↓
Categorizer        → classifies merchant into spending category
      ↓
Round-up Engine    → calculates spare change to nearest ₹10
      ↓
Behavior Aggregator → tracks luxury ratio, frequency, total spare change
      ↓
Risk Profiler      → K-means clustering → Conservative / Balanced / Aggressive
      ↓
Allocation Engine  → personalized split across Equity ETF, Digital Gold, Liquid Debt
```

---

## Built so far

**Week 1**
- Transaction categorizer — rule-based merchant to category mapping
- Round-up engine — nearest ₹10 logic with edge case handling
- K-means risk profiler — clusters users into behavioral profiles
- Dynamic allocation engine — personalized investment split
- Full pipeline — transactions in, allocation out

**Coming Week 2**
- Flask REST API wrapper
- Endpoints: /categorize, /roundup, /allocate, /risk-profile
- Integration with Kubyra Node.js backend

**Coming Week 3**
- Replace rule-based categorizer with trained scikit-learn classifier
- Transaction dataset from Kaggle for training
- Model persistence and versioning

**Coming later**
- C++ implementation for production-scale processing
- Real-time transaction stream handling
- 100k+ transactions per second target

---

## Project Structure

```
kubyra-ml/
├── main.py                    # entry point
├── requirements.txt
├── data/
│   └── sample_transactions.csv
├── src/
│   ├── categorizer.py         # merchant → category
│   ├── risk_profiler.py       # K-means clustering
│   └── pipeline.py            # connects everything
├── models/                    # saved trained models
└── docs/
    └── cpp_architecture.md    # production C++ design
```

---

## Running

```bash
pip install -r requirements.txt
python main.py
```

---

## Sample Output

```
KUBYRA — TRANSACTION ANALYSIS
Zomato    | ₹342.50 | Food     | Round-up: ₹7.50
Uber      | ₹187.00 | Travel   | Round-up: ₹3.00
Amazon    | ₹1245.75| Shopping | Round-up: ₹4.25
Swiggy    | ₹89.30  | Food     | Round-up: ₹0.70

RISK PROFILE & ALLOCATION
Risk Profile: Balanced
Investable Capital: ₹41.95
  Equity ETF   : ₹20.98 (50%)
  Digital Gold : ₹12.59 (30%)
  Liquid Debt  : ₹8.39  (20%)
```

---

## Stack

- Python 3.9+
- scikit-learn — K-means clustering, feature scaling
- pandas — data manipulation
- numpy — numerical operations
- Flask — REST API (Week 2)
- C++ with std::async — production pipeline (coming)

---

## Why two approaches

**Rule-based categorizer** for transaction classification —
we know the merchant categories, no need to discover them.
Fast, explainable, accurate for known merchants.

**K-means clustering** for risk profiling —
we're discovering behavioral patterns, not classifying 
into predefined labels. Unsupervised learning is the 
right tool here.

Two different problems. Two different approaches. 
One connected pipeline.
```

---