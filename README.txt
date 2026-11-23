CATALOGFIX AI - FIRST WORKING DEMO

1. Install Python 3.11+ and VS Code.
2. Unzip this folder and open it in VS Code.
3. Open Terminal > New Terminal.
4. Run: python -m pip install -r requirements.txt
5. Run: python -m streamlit run app.py
6. Browser opens at http://localhost:8501
7. Click Download sample CSV, then upload the downloaded file.
8. Verify the audit finds blank title, blank description, duplicate SKU, invalid prices.
9. Download audit CSV.

If `python` does not work on Windows, try `py` instead.

IMPORTANT:
This is a local prototype, not a deployed SaaS. It does not include AI, accounts,
subscriptions, customer data storage, security review or a production privacy policy.
Use only synthetic or non-confidential demo data.
