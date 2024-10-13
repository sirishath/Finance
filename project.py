import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf
import pandas as pd



user_after_tax_income = 0


# Define federal tax brackets and rates
federal_tax_brackets = [
    {"taxRate": 0.10, "maxIncome": 9950},
    {"taxRate": 0.12, "maxIncome": 40525},
    {"taxRate": 0.22, "maxIncome": 86375},
    {"taxRate": 0.24, "maxIncome": 164925},
    {"taxRate": 0.32, "maxIncome": 209425},
    {"taxRate": 0.35, "maxIncome": 523600},
    {"taxRate": 0.37, "maxIncome": float('inf')}
]

# Define the state tax rates and brackets
state_tax_brackets = {
    "California": [
        {"taxRate": 0.01, "maxIncome": 9325},
        {"taxRate": 0.02, "maxIncome": 22107},
        {"taxRate": 0.04, "maxIncome": 34892},
        {"taxRate": 0.06, "maxIncome": 48435},
        {"taxRate": 0.08, "maxIncome": 61214},
        {"taxRate": 0.093, "maxIncome": 312686},
        {"taxRate": 0.103, "maxIncome": 375221},
        {"taxRate": 0.113, "maxIncome": 625369},
        {"taxRate": 0.123, "maxIncome": float('inf')}
    ],
    "New York": [
        {"taxRate": 0.04, "maxIncome": 8500},
        {"taxRate": 0.045, "maxIncome": 11700},
        {"taxRate": 0.0525, "maxIncome": 13900},
        {"taxRate": 0.0585, "maxIncome": 21400},
        {"taxRate": 0.0625, "maxIncome": 80650},
        {"taxRate": 0.0685, "maxIncome": 215400},
        {"taxRate": 0.0882, "maxIncome": 1077550},
        {"taxRate": 0.103, "maxIncome": float('inf')}
    ],
    "Illinois": [
        {"taxRate": 0.04, "maxIncome": 10000},
        {"taxRate": 0.045, "maxIncome": 20000},
        {"taxRate": 0.05, "maxIncome": 75000},
        {"taxRate": 0.062, "maxIncome": 150000},
        {"taxRate": 0.0685, "maxIncome": 250000},
        {"taxRate": 0.0725, "maxIncome": float('inf')}
    ],
    "New Jersey": [
        {"taxRate": 0.014, "maxIncome": 20000},
        {"taxRate": 0.017, "maxIncome": 35000},
        {"taxRate": 0.035, "maxIncome": 40000},
        {"taxRate": 0.055, "maxIncome": 75000},
        {"taxRate": 0.0637, "maxIncome": 500000},
        {"taxRate": 0.0897, "maxIncome": float('inf')}
    ],
    "Massachusetts": [
        {"taxRate": 0.05, "maxIncome": 10000},
        {"taxRate": 0.06, "maxIncome": 40000},
        {"taxRate": 0.0725, "maxIncome": 100000},
        {"taxRate": 0.0875, "maxIncome": float('inf')}
    ],

    # Connecticut
    "Connecticut": [
    {"taxRate": 0.03, "maxIncome": 10000},
    {"taxRate": 0.05, "maxIncome": 50000},
    {"taxRate": 0.065, "maxIncome": 100000},
    {"taxRate": 0.069, "maxIncome": float('inf')}
    ],

    # Delaware
    "Delaware": [
    {"taxRate": 0.022, "maxIncome": 2000},
    {"taxRate": 0.039, "maxIncome": 5000},
    {"taxRate": 0.048, "maxIncome": 10000},
    {"taxRate": 0.052, "maxIncome": 20000},
    {"taxRate": 0.0555, "maxIncome": 60000},
    {"taxRate": 0.066, "maxIncome": float('inf')}
    ],

    # Hawaii
    "Hawaii": [
    {"taxRate": 0.014, "maxIncome": 2400},
    {"taxRate": 0.032, "maxIncome": 4800},
    {"taxRate": 0.055, "maxIncome": 9600},
    {"taxRate": 0.064, "maxIncome": 19200},
    {"taxRate": 0.068, "maxIncome": 36000},
    {"taxRate": 0.072, "maxIncome": 48000},
    {"taxRate": 0.076, "maxIncome": 72000},
    {"taxRate": 0.079, "maxIncome": 96000},
    {"taxRate": 0.0825, "maxIncome": 144000},
    {"taxRate": 0.09, "maxIncome": 200000},
    {"taxRate": 0.11, "maxIncome": float('inf')}
    ],

    # Idaho
    "Idaho": [
    {"taxRate": 0.01, "maxIncome": 1600},
    {"taxRate": 0.03, "maxIncome": 3200},
    {"taxRate": 0.045, "maxIncome": 4840},
    {"taxRate": 0.055, "maxIncome": 7260},
    {"taxRate": 0.065, "maxIncome": 10890},
    {"taxRate": 0.069, "maxIncome": float('inf')}
    ],

    # Iowa
    "Iowa": [
    {"taxRate": 0.0033, "maxIncome": 1638},
    {"taxRate": 0.0067, "maxIncome": 3276},
    {"taxRate": 0.0225, "maxIncome": 6552},
    {"taxRate": 0.0414, "maxIncome": 14742},
    {"taxRate": 0.0563, "maxIncome": 24570},
    {"taxRate": 0.0596, "maxIncome": 32760},
    {"taxRate": 0.0625, "maxIncome": 49140},
    {"taxRate": 0.0744, "maxIncome": 73710},
    {"taxRate": 0.0853, "maxIncome": float('inf')}
    ],

    # Kansas
    "Kansas": [
    {"taxRate": 0.031, "maxIncome": 15000},
    {"taxRate": 0.0525, "maxIncome": 30000},
    {"taxRate": 0.057, "maxIncome": float('inf')}
    ],

    # Maine
    "Maine": [
    {"taxRate": 0.058, "maxIncome": 23900},
    {"taxRate": 0.0675, "maxIncome": 56350},
    {"taxRate": 0.0715, "maxIncome": float('inf')}
    ],

    # Maryland
    "Maryland": [
    {"taxRate": 0.02, "maxIncome": 1000},
    {"taxRate": 0.03, "maxIncome": 2000},
    {"taxRate": 0.04, "maxIncome": 3000},
    {"taxRate": 0.0475, "maxIncome": 100000},
    {"taxRate": 0.05, "maxIncome": 125000},
    {"taxRate": 0.0525, "maxIncome": 150000},
    {"taxRate": 0.055, "maxIncome": 250000},
    {"taxRate": 0.0575, "maxIncome": float('inf')}
    ],

    # Minnesota
    "Minnesota": [
    {"taxRate": 0.0535, "maxIncome": 28080},
    {"taxRate": 0.068, "maxIncome": 92230},
    {"taxRate": 0.0785, "maxIncome": 171220},
    {"taxRate": 0.0985, "maxIncome": float('inf')}
    ],

    # Nebraska
    "Nebraska": [
    {"taxRate": 0.0246, "maxIncome": 3540},
    {"taxRate": 0.0351, "maxIncome": 21160},
    {"taxRate": 0.0501, "maxIncome": 34000},
    {"taxRate": 0.0684, "maxIncome": float('inf')}
    ],

    # New Mexico
    "New Mexico": [
    {"taxRate": 0.017, "maxIncome": 5500},
    {"taxRate": 0.032, "maxIncome": 11000},
    {"taxRate": 0.047, "maxIncome": 16000},
    {"taxRate": 0.049, "maxIncome": float('inf')}
    ],

    # Oregon
    "Oregon": [
    {"taxRate": 0.0475, "maxIncome": 3650},
    {"taxRate": 0.0675, "maxIncome": 9200},
    {"taxRate": 0.0875, "maxIncome": 125000},
    {"taxRate": 0.099, "maxIncome": float('inf')}
    ],

    # Rhode Island
    "Rhode Island": [
    {"taxRate": 0.0375, "maxIncome": 68200},
    {"taxRate": 0.0475, "maxIncome": 155050},
    {"taxRate": 0.0599, "maxIncome": float('inf')}
    ],

    # South Carolina
    "South Carolina": [
    {"taxRate": 0, "maxIncome": 3220},
    {"taxRate": 0.03, "maxIncome": 6440},
    {"taxRate": 0.04, "maxIncome": 9660},
    {"taxRate": 0.05, "maxIncome": 12880},
    {"taxRate": 0.06, "maxIncome": 16100},
    {"taxRate": 0.07, "maxIncome": float('inf')}
    ],

    # Vermont
    "Vermont": [
    {"taxRate": 0.0355, "maxIncome": 43150},
    {"taxRate": 0.068, "maxIncome": 174400},
    {"taxRate": 0.078, "maxIncome": 209400},
    {"taxRate": 0.0875, "maxIncome": float('inf')}
    ],

    # Virginia
    "Virginia": [
    {"taxRate": 0.02, "maxIncome": 3000},
    {"taxRate": 0.03, "maxIncome": 5000},
    {"taxRate": 0.05, "maxIncome": 17000},
    {"taxRate": 0.0575, "maxIncome": float('inf')}
    ],

    # Wisconsin
    "Wisconsin": [
    {"taxRate": 0.032, "maxIncome": 13810},
    {"taxRate": 0.0465, "maxIncome": 27630},
    {"taxRate": 0.0627, "maxIncome": 30420},
    {"taxRate": 0.0765, "maxIncome": float('inf')}
    ],

    "Alabama": [
        {"taxRate": 0.02, "maxIncome": 500},
        {"taxRate": 0.04, "maxIncome": 3000},
        {"taxRate": 0.05, "maxIncome": float('inf')}
    ],

    # Arkansas
    "Arkansas": [
        {"taxRate": 0.02, "maxIncome": 4299},
        {"taxRate": 0.04, "maxIncome": 8499},
        {"taxRate": 0.059, "maxIncome": 90999},
        {"taxRate": 0.065, "maxIncome": float('inf')}
    ],

    # Louisiana
    "Louisiana": [
        {"taxRate": 0.0185, "maxIncome": 12500},
        {"taxRate": 0.035, "maxIncome": 50000},
        {"taxRate": 0.045, "maxIncome": float('inf')}
    ],

    # Missouri
    "Missouri": [
        {"taxRate": 0.015, "maxIncome": 1000},
        {"taxRate": 0.02, "maxIncome": 2000},
        {"taxRate": 0.025, "maxIncome": 3000},
        {"taxRate": 0.03, "maxIncome": 4000},
        {"taxRate": 0.035, "maxIncome": 5000},
        {"taxRate": 0.04, "maxIncome": 6000},
        {"taxRate": 0.045, "maxIncome": 7000},
        {"taxRate": 0.05, "maxIncome": float('inf')}
    ],

    # Montana
    "Montana": [
        {"taxRate": 0.01, "maxIncome": 3100},
        {"taxRate": 0.02, "maxIncome": 5400},
        {"taxRate": 0.03, "maxIncome": 8200},
        {"taxRate": 0.04, "maxIncome": 11100},
        {"taxRate": 0.05, "maxIncome": 14100},
        {"taxRate": 0.06, "maxIncome": 18100},
        {"taxRate": 0.069, "maxIncome": float('inf')}
    ],

    # North Dakota
    "North Dakota": [
        {"taxRate": 0.011, "maxIncome": 40525},
        {"taxRate": 0.02, "maxIncome": 98050},
        {"taxRate": 0.0227, "maxIncome": 204675},
        {"taxRate": 0.0264, "maxIncome": 445000},
        {"taxRate": 0.029, "maxIncome": float('inf')}
    ],

    # Ohio
    "Ohio": [
        {"taxRate": 0.00285, "maxIncome": 2500},
        {"taxRate": 0.03326, "maxIncome": 5000},
        {"taxRate": 0.03688, "maxIncome": 10000},
        {"taxRate": 0.0464, "maxIncome": 15000},
        {"taxRate": 0.04997, "maxIncome": 25000},
        {"taxRate": 0.05201, "maxIncome": 50000},
        {"taxRate": 0.0597, "maxIncome": 100000},
        {"taxRate": 0.0690, "maxIncome": float('inf')}
    ],

    # Oklahoma
    "Oklahoma": [
        {"taxRate": 0.005, "maxIncome": 1000},
        {"taxRate": 0.01, "maxIncome": 2500},
        {"taxRate": 0.02, "maxIncome": 3750},
        {"taxRate": 0.03, "maxIncome": 4900},
        {"taxRate": 0.04, "maxIncome": 7200},
        {"taxRate": 0.05, "maxIncome": float('inf')}
    ],

    # West Virginia
    "West Virginia": [
        {"taxRate": 0.03, "maxIncome": 10000},
        {"taxRate": 0.04, "maxIncome": 25000},
        {"taxRate": 0.045, "maxIncome": 40000},
        {"taxRate": 0.06, "maxIncome": float('inf')}
    ],
}

# Flat tax rates for states with a simple flat tax system
flat_state_tax_rates = {
    "Alaska": 0,       # No income tax
    "Colorado": 0.045,
    "Florida": 0,      # No income tax
    "Georgia": 0.0575,
    "Illinois": 0.0495,
    "Indiana": 0.0323,
    "Kentucky": 0.05,
    "Massachusetts": 0.05,
    "Michigan": 0.0425,
    "Mississippi": 0.05,
    "Missouri": 0.054,
    "Montana": 0.0675,
    "North Carolina": 0.0499,
    "Pennsylvania": 0.0307,
    "Tennessee": 0,     # No income tax
    "Texas": 0,         # No income tax
    "Utah": 0.0495,
    "Washington": 0,    # No income tax
    "Wyoming": 0,       # No income tax
    "Nevada": 0,        # No income tax
    # Add more flat tax states here...
}

# Sidebar for navigation
st.sidebar.title("FutureVault")
page = st.sidebar.radio("Select Page", ("Introduction","Understand your income", "Investments", "Dashboard", "Health Savings", "401k Retirement Plan", "Financial Literacy Resources"))


if page == "Introduction":
    st.title("FutureVault")

    # Introduction Section
    st.write("""
    First step into getting familiar with your money. Our goal is to empower you to make informed decisions and achieve your financial goals.
    
    ### What can you see here?
    
    - **Understand your income📊** 
                 
    - **Health Insurance 📊**
                      
    - **Build Emergency Funds 💸**
    
    - **Start Investing 📈**
                 """)

    # FAQ Section
    st.write("## Frequently Asked Questions (FAQs)")
    faqs = [
        {"question": "What is a budget?", 
         "answer": "A budget is a plan that outlines your expected income and expenses over a period, helping you manage your finances effectively."},
        
        {"question": "What does an emergency fund do?", 
         "answer": "An emergency fund is a financial safety net for unexpected expenses or financial emergencies."},
        
        {"question": "What is compounding?", 
         "answer": "Compounding is the process where the interest earned on an investment also earns interest, resulting in exponential growth over time."}
    ]
    
    for faq in faqs:
        with st.expander(faq['question']):
            st.write(faq['answer'])


# Dashboard Page
elif page == "Dashboard":
    st.title("Build Your Emergency Fund")

    # Explanation of Emergency Funds
    st.write("""
    ## What is an Emergency Fund?
    An emergency fund is essential to cover unexpected expenses like medical emergencies, car repairs, or sudden job loss. 
    Financial experts recommend having an emergency fund that can cover at least 6 months' worth of living expenses.
    This provides a safety net to avoid falling into debt during tough times.
    """)

    # Prompt the user for their average living expenses
    avg_living_expense = st.number_input("Enter your average monthly living expenses ($):", min_value=0.0, step=100.0)

    # Calculate the required emergency fund size (6 months of living expenses)
    emergency_fund_size = avg_living_expense * 6
    st.write(f"### Your recommended emergency fund size: ${emergency_fund_size}")

    # Ask user how much time they want to save the emergency fund
    time_to_save_months = st.number_input("In how many months would you like to save this emergency fund?", min_value=1, step=1)

    # Calculate monthly savings goal
    if time_to_save_months > 0:
        monthly_savings_goal = emergency_fund_size / time_to_save_months
        st.write(f"### You need to save ${monthly_savings_goal:.2f} per month to build your emergency fund in {time_to_save_months} months.")
    
    yearly_income = st.number_input("Enter your after-tax yearly income ($):", min_value=0.0, step=1000.0)

    monthly_income = yearly_income / 12

    if monthly_income > 0:
        if monthly_savings_goal > monthly_income:
            st.warning(f"Your savings goal of \\${monthly_savings_goal:.2f} per month is higher than your available income of \\(${monthly_income:.2f}). Consider extending the time to save or reducing monthly expenses.")
        else:
            st.success(f"Your savings goal of \\${monthly_savings_goal:.2f} per month is achievable based on your monthly income of \\${monthly_income:.2f}.")


           
elif page == "Health Savings":
    st.title("Health Savings")
    st.write("""
    Estimate your potential tax savings when contributing to Health Savings Account (HSA) or Flexible Spending Account (FSA).
    """)

    faqs = [
    {"question": "What is a Health Savings Account (HSA)?", 
     "answer": "An HSA is a tax-advantaged savings account designed for individuals with high-deductible health plans to save money for medical expenses."},
    
    {"question": "What is a Flexible Spending Account (FSA)?", 
     "answer": "An FSA is an employer-sponsored benefit that allows employees to set aside pre-tax dollars for specific health care and dependent care expenses."},
    
    {"question": "What are the main differences between HSA and FSA?", 
     "answer": "HSAs are only available with high-deductible health plans, have no use-it-or-lose-it rule, and the funds can be invested. FSAs are available with any health plan, typically have a use-it-or-lose-it rule, and funds cannot be invested."},
    
    {"question": "Can I have both an HSA and FSA?", 
     "answer": "Generally, you cannot contribute to both an HSA and a general-purpose FSA in the same year. However, you may be able to have an HSA and a limited-purpose FSA for dental and vision expenses."},

    {"question": "What are the tax advantages of HSAs and FSAs?", 
     "answer": "Both HSAs and FSAs offer tax benefits. contributions to both HSAs and FSAs are typically made with pre-tax dollars, reducing your taxable income for the year, and withdrawals for qualified medical expenses are tax-free."}
]

    for faq in faqs:
        with st.expander(faq['question']):
            st.write(faq['answer'])

    st.subheader("Let's estimate your HSA/FSA savings for the year")

    # User Inputs
    account_type = st.selectbox("Choose Account Type", ("HSA", "FSA"))
    if account_type == "HSA":
        max = 4150
    else:
        max = 3200
    contribution = st.number_input("Enter your annual contribution ($):", min_value=0, max_value=max, step=100)
    income = st.number_input("Enter your annual income ($):", min_value=0, step=1000)
    tax_rate = st.slider("Enter your estimated tax rate (%):", 0, 50, 20)
    
    # Button to calculate
    calculate = st.button("Calculate")

    # Function to calculate tax savings
    def calculate_tax_savings(contribution, tax_rate):
        return contribution * (tax_rate / 100)

    # Only calculate and display results when button is clicked
    if calculate:
        # Calculate potential savings
        savings = calculate_tax_savings(contribution, tax_rate)

        # Display the calculated savings
        st.markdown(f"<h1 style='text-align: center;'> Tax Savings </h1>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center; color: green;'>${savings:,.2f}</h1>", unsafe_allow_html=True)
        st.write(f"Based on an annual contribution of ${contribution:,} to your {account_type} and a tax rate of {tax_rate}%.")

    # Provide a reminder about contribution limits
    st.subheader("Contribution Limits (2024):")
    st.write("- **HSA**: Up to $4,150 (self-only) or $8,300 (family)")
    st.write("- **FSA**: Up to $3,200 (health care) or $5,000 (dependent care)")

# Financial Literacy Resources Page
elif page == "Financial Literacy Resources":
    st.title("Financial Literacy Resources")
    
    st.write("## Recommended Videos")
    videos = [
        {"title": "How to Create a Budget | Step-by-Step Guide", "link": "https://www.youtube.com/watch?v=1pH4TN48Kqs"},
        {"title": "What is Compound Interest?", "link": "https://www.youtube.com/watch?v=6f1A-DdkdFE"},
        {"title": "Emergency Fund: What It Is and Why You Need One", "link": "https://www.youtube.com/watch?v=7bk6mJZcbSw"}
    ]
    
    for video in videos:
        st.write(f"[{video['title']}]({video['link']})")

    st.write("## Recommended Blogs")
    blogs = [
        {"title": "The Importance of Budgeting", "link": "https://www.thebalance.com/the-importance-of-budgeting-1289581"},
        {"title": "What Is Compound Interest? A Beginner's Guide", "link": "https://www.investopedia.com/terms/c/compoundinterest.asp"},
        {"title": "Why You Need an Emergency Fund", "link": "https://www.nerdwallet.com/article/saving/emergency-fund"},
    ]
    
    for blog in blogs:
        st.write(f"[{blog['title']}]({blog['link']})")

# Savings Tracker Page
elif page == "Investments":
    # Title of the app
    st.title("Investment Dashboard")

    st.write("Investing in stocks can offer the potential for significant long-term returns, outpacing inflation and helping you build wealth. However, it's important to remember that investing also involves risk, and there's no guarantee of profits.")
    st.subheader("**If you're a beginner, it's generally recommended to prioritize paying off high-interest debt before investing.**")

    # FAQs
    faqs = [
        {"question": "What are stocks?",
        "answer": "Stocks represent ownership shares in a company. When you invest in stocks, you're essentially becoming a part-owner of the company."},

        {"question": "What are bonds?",
        "answer": "Bonds are essentially loans made to corporations or governments. When you invest in bonds, you're lending money to these entities in exchange for interest payments."},

        {"question": "What are ETFs (Exchange-Traded Funds)?",
        "answer": "ETFs are similar to mutual funds but are traded on stock exchanges like individual stocks. They offer a way to invest in a basket of assets, such as stocks or bonds, in a single trade."},

        {"question": "What is the difference between stocks and bonds?",
        "answer": "Stocks generally offer higher potential returns but also come with higher risk. Bonds typically provide more stable returns but may not grow as much in value over time."},

        {"question": "What is diversification and why is it important?",
        "answer": "Diversification means spreading your investments across different asset classes to reduce risk. By diversifying, you're less likely to lose a significant portion of your portfolio if one investment performs poorly."}
    ]

    for faq in faqs:
        with st.expander(faq['question']):
            st.write(faq['answer'])

    # Stock information section
    st.header("Stock Information")
    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, GOOGL):", "AAPL")

    if ticker:
        stock_data = yf.Ticker(ticker)
        
        # Fetch historical market data for the past year
        hist = stock_data.history(period="1y")  # Get last year's data
        
        # Display stock information
        st.subheader(f"Stock Data for {ticker}")
        # st.write(hist)

        # Display stock info
        info = stock_data.info
        st.write(f"**Company Name:** {info.get('longName', 'N/A')}")
        st.write(f"**Market Cap:** {info.get('marketCap', 'N/A')}")
        st.write(f"**P/E Ratio:** {info.get('trailingPE', 'N/A')}")

        # Plotting stock price for the past year using Plotly
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name='Close Price'))

        # Add layout details
        fig.update_layout(title=f'{ticker} Stock Price Over the Last Year',
                        xaxis_title='Date',
                        yaxis_title='Stock Price (USD)',
                        xaxis_rangeslider_visible=True)

        # Display the Plotly chart
        st.plotly_chart(fig)

    # Additional resources section
    st.header("Additional Resources")
    st.write("""
    - [Investopedia](https://www.investopedia.com): A great resource for learning about investing.
    - [Yahoo Finance](https://finance.yahoo.com): For real-time stock market news and data.
    """)

elif page == "Understand your income":

    def calculate_federal_tax(income):
        """Calculates federal tax using progressive tax brackets"""
        tax = 0
        remaining_income = income

        for bracket in federal_tax_brackets:
            if remaining_income <= bracket['maxIncome']:
                tax += remaining_income * bracket['taxRate']
                break
            else:
                tax += bracket['maxIncome'] * bracket['taxRate']
                remaining_income -= bracket['maxIncome']

        return tax

    def calculate_progressive_state_tax(income, brackets):
        """Calculates progressive state tax based on given brackets"""
        tax = 0
        remaining_income = income

        for bracket in brackets:
            if remaining_income <= bracket['maxIncome']:
                tax += remaining_income * bracket['taxRate']
                break
            else:
                tax += bracket['maxIncome'] * bracket['taxRate']
                remaining_income -= bracket['maxIncome']

        return tax

    def calculate_flat_state_tax(income, tax_rate):
        """Calculates flat state tax"""
        return income * tax_rate

    # Streamlit UI
    st.title("Understanding your Income")

    st.subheader("""Before we calculate your income, it's essential to understand the deductions that will be applied:""")

    faqs = [
        {
            "question": "What are Federal Taxes?",
            "answer": "Federal taxes are imposed by the federal government on your income. The rates can vary based on your income level and filing status."
        },
        {
            "question": "What are State Taxes?",
            "answer": "Similar to federal taxes, these are taxes imposed by your state government. The rates and regulations vary widely between states."
        },
        {
            "question": "What is Social Security?",
            "answer": "Social Security is a federal program that provides benefits for retirees, the disabled, and survivors of deceased workers. A portion of your income is deducted for this program."
        },
        {
            "question": "What is Medicare?",
            "answer": "Medicare is a federal program that provides health coverage for individuals over 65 and some younger people with disabilities. Like Social Security, a portion of your income is deducted for Medicare."
        }
    ]

    for faq in faqs:
        with st.expander(faq['question']):
            st.write(faq['answer'])
    st.subheader("""Let's now understand our income and manage our finances.""")
    
    faqs = [
        {
            "question": "What is the 50/30/20 Rule?",
            "answer": "The 50/30/20 rule is a budgeting guideline that suggests allocating your after-tax income as follows:\n\n- 50% for Needs: Essential expenses such as housing, utilities, and groceries.\n- 30% for Wants: Non-essential expenses like dining out, entertainment, and vacations.\n- 20% for Savings: Money set aside for future goals, such as retirement savings or an emergency fund."
        }]
    
    for faq in faqs:
        with st.expander(faq['question']):
            st.write(faq['answer'])
    
    # Initialize session state for income and state
    if 'state' not in st.session_state:
        st.session_state['state'] = "-- Select State --"
    if 'income' not in st.session_state:
        st.session_state['income'] = 0.0
    if 'pay_period' not in st.session_state:
        st.session_state['pay_period'] = "Monthly"

    # User input for state and income
    state_options = ["-- Select State --"] + list(flat_state_tax_rates.keys()) + list(state_tax_brackets.keys())
    state = st.selectbox("Select State", state_options, index=0)
    income = st.number_input("Enter Annual Income", min_value=0.0, step=1000.0, value=st.session_state['income'])
    pay_period = st.selectbox("How often do you get paid?", ["Monthly", "Biweekly"])
    # Use session state for selectbox and number input

    # Store values in session state
    st.session_state['state'] = state
    st.session_state['income'] = income
    st.session_state['pay_period'] = pay_period

    if state != "-- Select State --" and income > 0 and pay_period:
        # Federal tax calculation
        federal_tax = calculate_federal_tax(income)

        # State tax calculation based on progressive or flat rate
        if state in state_tax_brackets:
            state_tax = calculate_progressive_state_tax(income, state_tax_brackets[state])
        elif state in flat_state_tax_rates:
            state_tax = calculate_flat_state_tax(income, flat_state_tax_rates[state])
        else:
            state_tax = 0  # Default for states with no tax

        total_tax = federal_tax + state_tax
        after_tax_income = income - total_tax
        user_after_tax_income = after_tax_income

        # Calculate available income for savings
        if pay_period == "Monthly":
            monthly_income = after_tax_income / 12
        else:  # Biweekly
            monthly_income = after_tax_income / 26  # Assuming 52 weeks in a year

        # Calculate savings based on the 50/30/20 rule
        savings = monthly_income * 0.20
        needs = monthly_income * 0.50
        wants = monthly_income * 0.30

        # Display results
        st.subheader("Income Analysis Report")
        # st.write(f"**Federal Tax:** ${federal_tax:,.2f}")
        # st.write(f"**State Tax:** ${state_tax:,.2f}")
        # st.write(f"**Total Tax:** ${total_tax:,.2f}")
        # st.write(f"**After-Tax Income:** ${after_tax_income:,.2f}")
        # st.write(f"**Monthly Income After Tax:** ${monthly_income:,.2f}")
        # st.write(f"**Savings (20%):** ${savings:,.2f}")
        # st.write(f"**Needs (50%):** ${needs:,.2f}")
        # st.write(f"**Wants (30%):** ${wants:,.2f}")

        # Pie chart for total taxed amount vs after-tax income
        labels1 = ['Total Tax', 'After-Tax Income']
        sizes1 = [total_tax, after_tax_income]
        colors1 = ['#ff9999', '#66b3ff']  # Light Coral and Light Blue

        fig1 = go.Figure(data=[go.Pie(labels=labels1, values=sizes1, hole=.2, 
                                        marker=dict(colors=colors1), 
                                        texttemplate='%{label}:  $%{value}',
                                        textposition='outside',  # Labels outside the pie chart
                                        hoverinfo='label', textfont=dict(size=16))])


        fig1.update_layout(title_text='Total Tax vs After-Tax Income', title_font_size=20, legend=dict(font=dict(size=20)))
        st.plotly_chart(fig1)

        # Pie chart for savings, needs, and wants
        labels2 = ['Needs', 'Wants', 'Savings']
        sizes2 = [round(needs, 2), round(wants, 2), round(savings,2)]
        colors2 = ['#ff7f0e', '#2ca02c', '#1f77b4']  # Blue, Orange, Green

        fig2 = go.Figure(data=[go.Pie(labels=labels2, values=sizes2, hole=.2, 
                                        marker=dict(colors=colors2), 
                                        texttemplate='%{label}:  $%{value}',  # Show label and percent
                                        textposition='outside',  # Labels outside the pie chart
                                        hoverinfo='percent', textfont=dict(size=16))
                                        ])

        if pay_period == "Monthly":
            fig2.update_layout(title_text='Monthly Income Allocation', title_font_size=20, legend=dict(font=dict(size=20)))
        else:  # Biweekly
            fig2.update_layout(title_text='Biweekly Income Allocation', title_font_size=20, legend=dict(font=dict(size=20)))
        st.plotly_chart(fig2)
    else:
        st.write("Please enter valid income and select a state.")
    
        # Reset button (clear session state)
    if st.button('Reset'):
        st.session_state['state'] = "-- Select State --"
        st.session_state['income'] = 0.0
        st.experimental_rerun()

elif page == "401k Retirement Plan":

    st.title("401(k) Retirement Plan")

    st.write("""
    A **401(k)** is a retirement savings plan sponsored by an employer that allows employees to save a portion of their paycheck before taxes are taken out. This means you can save money on taxes today and enjoy tax-deferred growth until you withdraw funds during retirement. Many employers offer matching contributions, which can significantly boost your retirement savings.

    This section allows you to estimate the growth of your 401(k) retirement plan based on your contributions and a specified interest rate.
    """)

    # User Inputs
    with st.form("401k_form"):
        initial_investment = st.number_input("Initial Investment ($):", min_value=0.0, value=5000.0)
        
        # Contribution frequency: Monthly or Biweekly
        contribution_frequency = st.selectbox("How are you contributing?", ["Monthly", "Biweekly"])
        
        # Input based on the frequency
        if contribution_frequency == "Monthly":
            contribution_per_paycheck = st.number_input("Contribution per Month ($):", min_value=0.0, value=500.0)
            contributions_per_year = 12  # 12 months in a year
            periods_in_a_year = 12  # Monthly compounding
        else:
            contribution_per_paycheck = st.number_input("Contribution per Biweekly Paycheck ($):", min_value=0.0, value=500.0)
            contributions_per_year = 26  # 26 biweekly paychecks in a year
            periods_in_a_year = 26  # Biweekly contributions

        # Automatically calculate the total annual contribution
        annual_contribution = contribution_per_paycheck * contributions_per_year

        years = st.number_input("Number of Years until Retirement:", min_value=1, max_value=50, value=30)
        annual_interest_rate = st.slider("Estimated Annual Interest Rate (%):", 0.0, 15.0, 5.0)

        # Calculate the estimated 401(k) balance
        calculate_401k = st.form_submit_button("Calculate 401(k) Balance")

        if calculate_401k:
            # Contribution per period based on the frequency
            future_value = initial_investment
            interest_rate_decimal = annual_interest_rate / 100

            # Interest is compounded monthly for simplicity (12 periods per year for monthly, 26 for biweekly)
            interest_rate_per_period = (1 + interest_rate_decimal) ** (1 / periods_in_a_year) - 1
            
            # Calculate future value with contributions and compound interest
            total_periods = years * periods_in_a_year  # Total number of contribution periods (12 for monthly, 26 for biweekly)

            for period in range(total_periods):
                future_value *= (1 + interest_rate_per_period)  # Apply interest first
                future_value += contribution_per_paycheck  # Add contribution every period, regardless of frequency

            st.write(f"**Estimated 401(k) Balance After {years} Years:** ${future_value:,.2f}")

            # Create the line graph for future value growth
            x_values = list(range(1, total_periods + 1))
            y_values = [initial_investment]
            for period in range(total_periods):
                y_values.append(y_values[-1] * (1 + interest_rate_per_period) + contribution_per_paycheck)

            # Create a line chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_values, y=y_values[1:], mode='lines+markers', name='401(k) Growth'))
            fig.update_layout(title="401(k) Growth Over Time", xaxis_title="Periods", yaxis_title="Balance ($)")
            st.plotly_chart(fig)

