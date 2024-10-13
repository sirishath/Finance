import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

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
st.sidebar.title("Financial Management App")
page = st.sidebar.radio("Select Page", ("Dashboard", "Income Tracker", "Expense Tracker", "Debt Tracker", "Savings Tracker", "Quiz", "Financial Literacy Resources", "HSA & FSA Savings Calculator"))

# Dashboard Page
if page == "Dashboard":
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

# Income Tracker Page
elif page == "Income Tracker":
    st.title("Income Tracker")
    
    with st.form("income_form"):
        income_source = st.text_input("Income Source")
        income_amount = st.number_input("Amount", min_value=0.0)
        submitted = st.form_submit_button("Add Income")
        
        if submitted:
            st.session_state.income_data.append({'source': income_source, 'amount': income_amount})
            st.success("Income Added Successfully!")

    st.write("### Income Data")
    if st.session_state.income_data:
        income_df = pd.DataFrame(st.session_state.income_data)
        st.dataframe(income_df)

# Expense Tracker Page
elif page == "Expense Tracker":
    st.title("Expense Tracker")
    
    with st.form("expense_form"):
        expense_name = st.text_input("Expense Name")
        expense_amount = st.number_input("Amount", min_value=0.0)
        submitted = st.form_submit_button("Add Expense")
        
        if submitted:
            st.session_state.expense_data.append({'name': expense_name, 'amount': expense_amount})
            st.success("Expense Added Successfully!")

    st.write("### Expense Data")
    if st.session_state.expense_data:
        expense_df = pd.DataFrame(st.session_state.expense_data)
        st.dataframe(expense_df)

# Debt Tracker Page
elif page == "Debt Tracker":
    st.title("Debt Tracker")
    
    with st.form("debt_form"):
        debt_name = st.text_input("Debt Name")
        debt_amount = st.number_input("Amount", min_value=0.0)
        debt_interest = st.number_input("Interest Rate (%)", min_value=0.0)
        submitted = st.form_submit_button("Add Debt")
        
        if submitted:
            st.session_state.debt_data.append({'name': debt_name, 'amount': debt_amount, 'interest': debt_interest})
            st.success("Debt Added Successfully!")

    st.write("### Debt Data")
    if st.session_state.debt_data:
        debt_df = pd.DataFrame(st.session_state.debt_data)
        st.dataframe(debt_df)

# Savings Tracker Page
elif page == "Savings Tracker":
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

