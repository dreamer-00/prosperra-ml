# Kubyra ML Engine

The intelligence layer behind Kubyra's allocation system.

## What this does
Allocation with personalized investment splits based on real spending behavior.

## Pipeline
Transaction → Categorizer → Round-up → 
Pattern Analysis → Risk Profile → Dynamic Allocation

## Built so far
- Transaction categorizer (merchant → category)
- Round-up engine (nearest ₹10 logic)
- Investment mapper (category → asset class)

## Running
pip install -r requirements.txt
python main.py

## Stack
Python, Flask (coming week 2), scikit-learn (week 3)