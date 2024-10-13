if page == "Dashboard":
    st.title("Financial Management Dashboard")
    
    # Introduction Section
    st.write("""
    Welcome to a Streamlit-based personal finance dashboard. This intuitive dashboard is designed to give you a visual representation of your finances over time, empowering you to make informed decisions and achieve your financial goals.
    
    ### What can you see here?
    
    - **Track your income and expenses 📊**: See exactly where your money comes from and goes. Easy-to-read visualizations break down your income streams and spending habits, helping you identify areas for potential savings or growth. Gain a comprehensive understanding of your financial patterns to make informed decisions about budgeting and resource allocation.
    
    - **Monitor your cash flow 💸**: Stay on top of your incoming and outgoing funds. This dashboard provides clear insight into your current financial liquidity, allowing you to plan for upcoming expenses and avoid potential shortfalls. Anticipate cash crunches and optimize your spending timing to maintain a healthy financial balance.
    
    - **View your financial progress 📈**: Charts and graphs track your progress towards your financial goals over time. Whether you're saving for a dream vacation or planning for retirement, this dashboard keeps you motivated and on track. Visualize your long-term financial journey and adjust your strategies based on real-time performance data.
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

elif page == "Records":
    st.title("Financial Summary Records")
    
    # Display financial summaries
    total_income = sum(income['amount'] for income in st.session_state.income_data)
    total_expenses = sum(expense['amount'] for expense in st.session_state.expense_data)
    total_debt = sum(debt['amount'] for debt in st.session_state.debt_data)
    total_savings = sum(saving['amount'] for saving in st.session_state.savings_data)
    
    st.write(f"**Total Income:** ${total_income}")
    st.write(f"**Total Expenses:** ${total_expenses}")
    st.write(f"**Total Debt:** ${total_debt}")
    st.write(f"**Total Savings:** ${total_savings}")
