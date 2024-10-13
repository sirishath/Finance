import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go


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

# Initialize session state
if 'income_data' not in st.session_state:
    st.session_state.income_data = []
if 'expense_data' not in st.session_state:
    st.session_state.expense_data = []
if 'debt_data' not in st.session_state:
    st.session_state.debt_data = []
if 'savings_data' not in st.session_state:
    st.session_state.savings_data = []
if 'quizzes' not in st.session_state:
    st.session_state.quizzes = []

# Sidebar for navigation
st.sidebar.title("FutureVault")
page = st.sidebar.radio("Select Page", ("Introduction","Dashboard", "Investments", "Quiz", "Financial Literacy Resources", "HSA & FSA Savings Calculator", "Understand your income", ""))

# Dashboard Page
if page == "Introduction":
    st.title("FutureVault")

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
    st.title("Financial Management Dashboard")
    
    # Display financial summaries
    total_income = sum(income['amount'] for income in st.session_state.income_data)
    total_expenses = sum(expense['amount'] for expense in st.session_state.expense_data)
    total_debt = sum(debt['amount'] for debt in st.session_state.debt_data)
    total_savings = sum(saving['amount'] for saving in st.session_state.savings_data)
    
    st.write(f"Total Income: ${total_income}")
    st.write(f"Total Expenses: ${total_expenses}")
    st.write(f"Total Debt: ${total_debt}")
    st.write(f"Total Savings: ${total_savings}")

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

# HSA and FSA Savings Calculator Page
elif page == "HSA & FSA Savings Calculator":
    st.title("HSA and FSA Savings Calculator with Graph")
    st.write("""
    Estimate your potential tax savings when contributing to Health Savings Account (HSA) or Flexible Spending Account (FSA), and see the impact visually.
    """)

    # Layout: side-by-side columns for inputs and graph
    col1, col2 = st.columns(2)

    # Column 1: User Inputs
    with col1:
        account_type = st.selectbox("Choose Account Type", ("HSA", "FSA"))
        contribution = st.number_input("Enter your annual contribution ($):", min_value=0, max_value=10000, step=100)
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

        # Column 2: Display Graph
        with col2:
            # Create the graph using Plotly
            fig = go.Figure(data=[
                go.Bar(name="Contribution", x=["Contribution"], y=[contribution], marker_color='blue'),
                go.Bar(name="Tax Savings", x=["Tax Savings"], y=[savings], marker_color='green')
            ])

            # Customize the layout of the graph
            fig.update_layout(
                title="Contribution vs. Tax Savings",
                xaxis_title="Category",
                yaxis_title="Amount ($)",
                barmode='group'
            )

            # Show the graph in Streamlit
            st.plotly_chart(fig)

        # Display the calculated savings below the inputs
        st.write(f"With an annual contribution of ${contribution:,} to your {account_type}, you could save approximately ${savings:,.2f} in taxes based on a tax rate of {tax_rate}%.")

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
    st.title("Savings Tracker")
    
    with st.form("savings_form"):
        savings_goal = st.text_input("Savings Goal Name")
        savings_amount = st.number_input("Amount", min_value=0.0)
        submitted = st.form_submit_button("Add Savings")
        
        if submitted:
            st.session_state.savings_data.append({'goal': savings_goal, 'amount': savings_amount})
            st.success("Savings Goal Added Successfully!")

    st.write("### Savings Data")
    if st.session_state.savings_data:
        savings_df = pd.DataFrame(st.session_state.savings_data)
        st.dataframe(savings_df)

# Quiz Page
elif page == "Quiz":
    st.title("Financial Literacy Quiz")
    
    quizzes = [
        {"question": "What is a budget?", "options": ["A plan for spending", "A type of investment", "A form of debt"], "answer": "A plan for spending"},
        {"question": "What does an emergency fund do?", "options": ["Helps you invest", "Covers unexpected expenses", "Increases your debt"], "answer": "Covers unexpected expenses"},
        {"question": "What is compounding?", "options": ["Interest on interest", "Debt accumulation", "Investment diversification"], "answer": "Interest on interest"},
    ]
    
    for quiz in quizzes:
        st.write(f"**{quiz['question']}**")
        selected_option = st.radio("Select an option", quiz['options'], key=quiz['question'])
        
        if st.button("Submit", key=quiz['question']):
            if selected_option == quiz['answer']:
                st.success("Correct!")
            else:
                st.error("Incorrect, try again!")

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
    st.title("Tax Calculator")

    # Initialize session state for income and state
    if 'state' not in st.session_state:
        st.session_state['state'] = "-- Select State --"
    if 'income' not in st.session_state:
        st.session_state['income'] = 0.0

    # # User input for state and income
    # state = st.selectbox("Select State", ["-- Select State --"] + list(flat_state_tax_rates.keys()) + list(state_tax_brackets.keys()), index=list(flat_state_tax_rates.keys()).index(st.session_state['state']) if st.session_state['state'] != "-- Select State --" else 0)
    # income = st.number_input("Enter Annual Income", min_value=0.0, step=1000.0, value=st.session_state['income'])
    # User input for state and income
    state_options = ["-- Select State --"] + list(flat_state_tax_rates.keys()) + list(state_tax_brackets.keys())
    state = st.selectbox("Select State", state_options, index=0)
    income = st.number_input("Enter Annual Income", min_value=0.0, step=1000.0, value=st.session_state['income'])
    # Use session state for selectbox and number input

    # Store values in session state
    st.session_state['state'] = state
    st.session_state['income'] = income

    if state != "-- Select State --" and income > 0:
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

        # Display results
        st.subheader("Calculation Results")
        st.write(f"**Federal Tax:** ${federal_tax:,.2f}")
        st.write(f"**State Tax:** ${state_tax:,.2f}")
        st.write(f"**Total Tax:** ${total_tax:,.2f}")
        st.write(f"**After-Tax Income:** ${after_tax_income:,.2f}")
    else:
        st.write("Please enter valid income and select a state.")

    # Reset button (clear session state)
    if st.button('Reset'):
        st.session_state['state'] = "-- Select State --"
        st.session_state['income'] = 0.0
        st.experimental_rerun()
