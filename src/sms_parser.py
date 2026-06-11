import re
import json
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
class SMSParser:
    def __init__(self):
        self.patterns = [
            {
                "bank": "HDFC",
                "pattern": r"Rs\.?([\d,]+\.?\d*)\s+debited.*?to\s+([A-Z][A-Z\s]+?)\s+on\s+([\d-]+).*?UPI\s*Ref:?(\d+)",
                "groups": ["amount", "merchant", "date", "upi_ref"]
            },
            {
                "bank": "SBI", 
                "pattern": r"debited by Rs\.?\s*([\d,]+\.?\d*).*?transfer to\s+([A-Z][A-Z\s]+?)\s+UPI.*?(\d{6,})",
                "groups": ["amount", "merchant", "upi_ref"]
            },
            {
                "bank": "ICICI",
                "pattern": r"Rs\.?([\d,]+\.?\d*)\s+debited.*?UPI:([A-Z]+)@.*?Ref:(\d+)",
                "groups": ["amount", "merchant", "upi_ref"]
            },
            {
                "bank": "GENERIC",
                "pattern": r"(?:Rs\.?|INR)\s*([\d,]+\.?\d*).*?(?:to|paid to)\s+([A-Z][A-Z\s]{2,20}?)(?:\s+(?:UPI|via|on))",
                "groups": ["amount", "merchant"]
            }
        ]
    def clean_amount(self, amount_str):
        return float(amount_str.replace(',', ''))
    def clean_merchant(self, merchant_str):
        return merchant_str.strip().title()
    def parse_with_llm(self, sms_text):
        import requests
        import json
        import os
        prompt = f"""Extract transaction details from this UPI SMS message.
                Return ONLY a JSON object with exactly these keys:
                - amount: the transaction amount as a number (null if not found)
                - merchant: the merchant or receiver name as a string (null if not found)
                - upi_ref: the UPI reference number as a string (null if not found)
                - date: the transaction date as a string (null if not found)
                No explanation. No markdown. Just the JSON object.
                SMS: {sms_text}"""
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"
                },
                json={
                    "model": "llama-3.1-8b-instant",
                    "max_tokens": 200,
                    "temperature": 0,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You extract structured data from UPI SMS messages. Return only valid JSON. No markdown. No explanation."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                }
            )
            raw = response.json()
            content = raw['choices'][0]['message']['content']
            content = content.replace('```json', '').replace('```', '').strip() 
            parsed = json.loads(content)
            return {
                "raw_sms": sms_text,
                "bank_detected": "GROQ_LLAMA_PARSED",
                "parsed_at": datetime.now().isoformat(),
                "amount": float(parsed.get("amount")) if parsed.get("amount") else None,
                "merchant": parsed.get("merchant"),
                "upi_ref": parsed.get("upi_ref"),
                "date": parsed.get("date"),
                "parse_failed": False
            }
        except Exception as e:
            return {
                "raw_sms": sms_text,
                "bank_detected": "UNKNOWN",
                "parsed_at": datetime.now().isoformat(),
                "amount": None,
                "merchant": None,
                "upi_ref": None,
                "parse_failed": True,
                "error": str(e)
            }
    def parse(self, sms_text):
        sms_upper = sms_text.upper()
        if any(word in sms_upper for word in ['CREDITED', 'RECEIVED', 'ADDED', 'DEPOSIT']):
            return None
        if any(word in sms_upper for word in ['IMPS', 'NEFT', 'SENT TO', 'TRANSFERRED TO']):
            return None
        for pattern_config in self.patterns:
            match = re.search(
                pattern_config['pattern'],
                sms_text,
                re.IGNORECASE
            )
            if match:
                groups=match.groups()
                group_names = pattern_config["groups"]
                result = {
                    "raw_sms": sms_text,
                    "bank_detected": pattern_config["bank"],
                    "parsed_at": datetime.now().isoformat(),
                    "amount": None,
                    "merchant": None,
                    "upi_ref": None,
                    "date": None
                }
                for i, name in enumerate(group_names):
                    if i < len(groups) and groups[i]:
                        if name=='amount':
                            result['amount']=self.clean_amount(groups[i])
                        elif name == "merchant":
                            result["merchant"]=self.clean_merchant(groups[i])
                        else:
                            result[name]=groups[i]
                    if result["amount"] and result["merchant"]:
                        return result
        return self.parse_with_llm(sms_text)
    def parse_batch(self, sms_list):
        results = []
        failed = []
        for sms in sms_list:
            parsed = self.parse(sms)
            if parsed and not parsed.get('parse_failed'):
                results.append(parsed)
            else:
                failed.append(sms)
        return {
            "parsed": results,
            "failed": failed,
            "success_rate": f"{len(results)/len(sms_list)*100:.1f}%"
        }
    def to_json(self, sms_text):
        result = self.parse(sms_text)
        return json.dumps(result, indent=2)


