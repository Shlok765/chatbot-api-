from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# In-memory storage for chat messages (in production, use a database)
chat_messages = []

# Predefined responses for the chatbot - Finance & Banking focused
BOT_RESPONSES = {
    # Greetings
    "hello": "Hello! I'm your Finance & Banking Assistant. How can I help you with your financial questions today?",
    "hi": "Hi there! Ready to help you with banking, loans, investments, or any other finance topics.",
    "hey": "Hey! I specialize in finance and banking questions. What would you like to know?",
    "good morning": "Good morning! How can I assist you with your financial needs today?",
    "good afternoon": "Good afternoon! What financial topic would you like to discuss?",
    "good evening": "Good evening! I'm here to help with your banking and finance questions.",

    # Basic banking
    "what is a bank": "A bank is a financial institution licensed to receive deposits and make loans. Banks may also provide financial services such as wealth management, currency exchange, and safe deposit boxes.",
    "types of bank accounts": "Common types of bank accounts include: Checking accounts (for daily transactions), Savings accounts (for earning interest), Money market accounts (higher interest with limited transactions), CDs (Certificates of Deposit with fixed terms), and Retirement accounts (IRAs, 401(k)s).",
    "difference between checking and savings": "Checking accounts are designed for frequent transactions like bill payments and purchases, usually with little or no interest. Savings accounts are meant for storing money and earning interest, with limited withdrawals per month.",
    "how to open a bank account": "To open a bank account, you typically need: Government-issued ID (driver's license, passport), Social Security number or Tax ID, Proof of address (utility bill, lease agreement), and an initial deposit (amount varies by bank). Many banks now allow online account opening.",
    "what is routing number": "A routing number is a 9-digit code that identifies the financial institution where your account is held. It's used for direct deposits, wire transfers, and electronic payments like ACH.",
    "what is account number": "Your account number is a unique identifier for your specific bank account, usually 10-12 digits. It works with the routing number to direct money to and from your account.",

    # Loans and credit
    "what is a loan": "A loan is money borrowed from a lender that must be repaid with interest over a set period. Common types include personal loans, auto loans, mortgages, and student loans.",
    "difference between secured and unsecured loan": "A secured loan requires collateral (like a house for a mortgage or car for an auto loan) that the lender can claim if you default. An unsecured loan (like most personal loans or credit cards) doesn't require collateral but usually has higher interest rates.",
    "what is interest rate": "Interest rate is the percentage charged by a lender for borrowing money, or paid to you for keeping money in an account. It's the cost of borrowing or the reward for saving.",
    "what is apr": "APR (Annual Percentage Rate) represents the yearly cost of borrowing money, including interest and fees. It gives a more complete picture than just the interest rate alone.",
    "what is credit score": "A credit score is a numerical representation (typically 300-850) of your creditworthiness based on your credit history. Higher scores indicate lower risk to lenders and can qualify you for better interest rates.",
    "how to improve credit score": "To improve your credit score: Pay bills on time, keep credit card balances low (under 30% of limit), don't close old accounts, limit new credit applications, check your credit report for errors, and maintain a mix of credit types.",
    "what is a mortgage": "A mortgage is a loan used to purchase real estate, where the property itself serves as collateral. Mortgages typically have terms of 15-30 years and can have fixed or adjustable interest rates.",
    "what is a personal loan": "A personal loan is an unsecured loan that can be used for various purposes like debt consolidation, home improvements, or major purchases. They typically have fixed interest rates and set repayment terms.",
    "what is an auto loan": "An auto loan is a secured loan used to purchase a vehicle, where the car serves as collateral. Terms usually range from 36-72 months.",

    # Credit cards
    "what is a credit card": "A credit card is a payment card that allows you to borrow funds up to a certain limit to pay for goods and services. You must repay the borrowed amount, plus any interest, according to the card's terms.",
    "how does credit card interest work": "If you don't pay your full balance by the due date, interest is charged on the remaining balance. Interest is typically calculated daily based on your average daily balance and the card's APR.",
    "what is minimum payment": "The minimum payment is the smallest amount you must pay each month to keep your credit card account in good standing. Paying only the minimum will result in interest charges and take longer to pay off the balance.",
    "what is cash advance": "A cash advance allows you to withdraw cash against your credit card limit. It usually comes with higher interest rates than purchases and often has additional fees.",
    "what is balance transfer": "A balance transfer moves debt from one credit card to another, often to take advantage of a lower introductory interest rate. There's usually a transfer fee (3-5% of the amount transferred).",

    # Investments
    "what is investing": "Investing is the act of allocating resources (usually money) with the expectation of generating income or profit. Common investments include stocks, bonds, mutual funds, ETFs, real estate, and commodities.",
    "difference between stocks and bonds": "Stocks represent ownership in a company and may provide dividends and capital appreciation. Bonds are debt instruments where you lend money to an issuer (government or corporation) in exchange for periodic interest payments and return of principal.",
    "what are mutual funds": "Mutual funds pool money from many investors to buy a diversified portfolio of stocks, bonds, or other securities. They're managed by professional fund managers and offer instant diversification.",
    "what are etfs": "ETFs (Exchange-Traded Funds) are similar to mutual funds but trade on stock exchanges like individual stocks. They typically have lower fees and offer intraday trading.",
    "what is diversification": "Diversification is spreading investments across different asset classes, sectors, or geographic regions to reduce risk. The idea is 'don't put all your eggs in one basket'.",
    "what is compound interest": "Compound interest is earning interest on both your initial principal and the accumulated interest from previous periods. It's often called 'interest on interest' and can significantly grow wealth over time.",
    "what is risk tolerance": "Risk tolerance is your ability and willingness to lose some or all of an investment in exchange for greater potential returns. It helps determine your appropriate investment strategy.",
    "what is asset allocation": "Asset allocation is dividing your investment portfolio among different asset categories (stocks, bonds, cash, etc.) based on your goals, risk tolerance, and time horizon.",
    "what is a dividend": "A dividend is a distribution of a portion of a company's earnings to its shareholders, usually paid quarterly. Not all stocks pay dividends.",
    "what is an index fund": "An index fund is a type of mutual fund or ETF designed to track the performance of a specific market index (like the S&P 500). They offer broad market exposure with low fees.",

    # Personal finance
    "what is budgeting": "Budgeting is creating a plan for how you'll spend your money each month. It helps you track income vs expenses, identify savings opportunities, and work toward financial goals.",
    "how to create a budget": "To create a budget: 1) List all income sources, 2) Track all expenses for a month, 3) Categorize expenses (housing, food, transport, etc.), 4) Set spending limits for each category, 5) Review and adjust regularly.",
    "what is emergency fund": "An emergency fund is money set aside to cover unexpected expenses like medical bills, car repairs, or job loss. Financial experts typically recommend saving 3-6 months of living expenses.",
    "what is net worth": "Net worth is the difference between what you own (assets) and what you owe (liabilities). It's a snapshot of your financial health at a specific point in time.",
    "what is debt snowball": "The debt snowball method involves paying off debts from smallest to largest balance, gaining momentum as each balance is paid off. You pay minimums on all debts except the smallest, which you attack with extra payments.",
    "what is debt avalanche": "The debt avalanche method involves paying off debts from highest to lowest interest rate, which saves the most money on interest over time.",
    "what is insurance": "Insurance is a contract (policy) where you pay premiums to an insurer in exchange for financial protection against specific losses (like accidents, illness, or property damage).",
    "types of insurance": "Common types include: Health insurance, Life insurance, Auto insurance, Homeowners/renters insurance, Disability insurance, and Long-term care insurance.",

    # Banking services
    "what is online banking": "Online banking allows you to perform banking transactions over the internet through a bank's website or mobile app. You can check balances, transfer funds, pay bills, deposit checks, and more.",
    "what is mobile banking": "Mobile banking is accessing banking services through a smartphone or tablet app, offering convenience for transactions on the go.",
    "what is an atm": "An ATM (Automated Teller Machine) is an electronic banking outlet that allows customers to complete basic transactions without the aid of a teller, such as cash withdrawals, deposits, and transfers.",
    "what is direct deposit": "Direct deposit is an electronic transfer of payment (like a paycheck) directly into your bank account, eliminating the need for paper checks.",
    "what is automatic bill pay": "Automatic bill pay is a service that allows you to schedule recurring payments from your bank account to pay bills like utilities, subscriptions, or loans on their due dates.",
    "what is overdraft protection": "Overdraft protection is a service that covers transactions when you don't have enough funds in your account, typically by transferring money from a linked account or line of credit (often for a fee).",
    "what is wire transfer": "A wire transfer is an electronic transfer of funds across a network of banks or transfer agencies around the world.",
    "default": "I'm not sure I understand that finance question. Could you rephrase it or ask something else about banking, loans, investments, or personal finance?"
}

def get_bot_response(user_message):
    """Get a response from the chatbot based on user input"""
    user_message = user_message.lower().strip()
    print(f"DEBUG: User message: '{user_message}'")  # Debug line

    # Check for exact matches first
    if user_message in BOT_RESPONSES:
        print(f"DEBUG: Exact match found for '{user_message}'")
        return BOT_RESPONSES[user_message]

    # Check for partial matches
    for key, response in BOT_RESPONSES.items():
        if key in user_message and key != "default":
            print(f"DEBUG: Partial match found for key '{key}'")
            return response

    # Return default response if no match found
    print(f"DEBUG: No match found, returning default")
    return BOT_RESPONSES["default"]

@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    """Handle sending a message and getting a bot response"""
    user_message = request.json.get('message', '').strip()

    if not user_message:
        return jsonify({'error': 'Message cannot be empty'}), 400

    # Add user message to chat history
    user_msg = {
        'type': 'user',
        'message': user_message,
        'timestamp': datetime.now().strftime('%H:%M')
    }
    chat_messages.append(user_msg)

    # Get bot response
    bot_response = get_bot_response(user_message)

    # Add bot message to chat history
    bot_msg = {
        'type': 'bot',
        'message': bot_response,
        'timestamp': datetime.now().strftime('%H:%M')
    }
    chat_messages.append(bot_msg)

    # Return both messages
    return jsonify({
        'user_message': user_msg,
        'bot_message': bot_msg
    })

@app.route('/get_messages')
def get_messages():
    """Retrieve all chat messages"""
    return jsonify({'messages': chat_messages})

@app.route('/clear_chat', methods=['POST'])
def clear_chat():
    """Clear the chat history"""
    global chat_messages
    chat_messages = []
    return jsonify({'status': 'cleared'})

if __name__ == '__main__':
    # Get local IP address for network access
    import socket
    try:
        # Create a socket to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        local_ip = "127.0.0.1"

    print(f"""
    ChatBot is running!
    Local access: http://127.0.0.1:5000
    Network access: http://{local_ip}:5000
    Share the network address with other devices on your Wi-Fi
    """)

    # Run on all network interfaces so other devices can access it
    app.run(host='0.0.0.0', port=5000, debug=True)