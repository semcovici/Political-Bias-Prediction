FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["streamlit", "run", "interface.py", "--theme.primaryColor", "#000000", "--theme.backgroundColor", "#EEEEEE", "--theme.secondaryBackgroundColor", "#FFE8C0", "--theme.textColor", "#000000", "--theme.font", "sans serif", "--server.enableCORS", "false", "--browser.serverAddress", "0.0.0.0", "--browser.gatherUsageStats", "false", "--server.port", "8080"]

