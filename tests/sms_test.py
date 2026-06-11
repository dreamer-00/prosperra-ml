import os
from dotenv import load_dotenv
load_dotenv()
print("KEY:", os.getenv('GROQ_API_KEY'))
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.sms_parser import SMSParser
parser = SMSParser()
test_messages = [
    "Rs.342.50 debited from a/c XX1234 to ZOMATO on 07-06-26. UPI Ref:123456789",
    "Your a/c XXXX1234 debited by Rs 187.00 on 07-06-26 transfer to OLA UPI/DR/456789",
    "ICICI Bank: Rs.89.30 debited. UPI:SWIGGY@okaxis Ref:789012",
    "Kotak Bank: INR 1245.75 debited from XX5678 to AMAZON PAY via UPI 07Jun26",
    "Rs.560 paid to IRCTC via Paytm UPI. UPI Ref No. 234567890",
    "Rs.5000 credited to your account from SALARY",
    "Rs.2000 sent to Rahul via IMPS",
    #Trying these below for LLM Fallback
    "Txn of INR560.00 done. Merchant: BookMyShow. "
    "Auth code 445566. Call 1800 if not done by you.",
    "UPI txn successful! Paid ₹234 to rapido.upi@ybl "
    "on 11-06-26. NPCI Ref 998877665544",
]
print("SMS PARSER TEST")
for sms in test_messages:
    print(f"\nInput: {sms[:50]}...")
    result = parser.to_json(sms)
    print(result)