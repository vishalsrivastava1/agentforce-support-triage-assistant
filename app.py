import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Agentforce Support Triage Assistant",
    page_icon="🤖",
    layout="wide"
)


def classify_priority(message, customer_tier):
    message_lower = message.lower()

    high_keywords = [
        "down", "outage", "production", "urgent", "critical",
        "cannot access", "security", "unusual login", "latency"
    ]

    medium_keywords = [
        "slow", "overheating", "charged twice", "login",
        "not working", "performance", "billing"
    ]

    if any(keyword in message_lower for keyword in high_keywords):
        return "High"

    if customer_tier == "Enterprise" and any(keyword in message_lower for keyword in medium_keywords):
        return "High"

    if any(keyword in message_lower for keyword in medium_keywords):
        return "Medium"

    return "Low"


def classify_category(message, product_area):
    message_lower = message.lower()

    if "invoice" in message_lower or "charged" in message_lower or "billing" in message_lower:
        return "Billing"
    elif "login" in message_lower or "password" in message_lower or "portal" in message_lower:
        return "Portal Access"
    elif "down" in message_lower or "latency" in message_lower or "network" in message_lower:
        return "Network / Connectivity"
    elif "security" in message_lower or "unusual login" in message_lower or "access activity" in message_lower:
        return "Security"
    elif "overheating" in message_lower or "device" in message_lower or "hardware" in message_lower:
        return "Hardware"
    else:
        return product_area


def generate_summary(message):
    message_lower = message.lower()

    if "down" in message_lower or "outage" in message_lower:
        return "Customer is reporting a service-impacting connectivity issue that may affect production operations."
    elif "charged twice" in message_lower or "invoice" in message_lower:
        return "Customer is requesting support for a billing or invoice discrepancy."
    elif "login" in message_lower or "password" in message_lower:
        return "Customer is experiencing access issues with the support portal or account login."
    elif "latency" in message_lower or "slow" in message_lower:
        return "Customer is reporting performance degradation or increased latency."
    elif "security" in message_lower or "unusual login" in message_lower:
        return "Customer is reporting a possible security or account access concern."
    elif "overheating" in message_lower:
        return "Customer is reporting a hardware reliability issue involving overheating or shutdowns."
    else:
        return "Customer is requesting support and the case requires review by the support team."


def recommend_knowledge_article(category):
    articles = {
        "Billing": "Billing Dispute and Invoice Review Guide",
        "Portal Access": "Customer Portal Login Troubleshooting Guide",
        "Network / Connectivity": "Connectivity Outage Initial Triage Checklist",
        "Security": "Account Security Review and Access Activity Guide",
        "Hardware": "Hardware Overheating and Device Shutdown Troubleshooting",
        "Account": "Account Administration Update Guide",
        "General": "General Support Case Handling SOP"
    }

    return articles.get(category, "General Support Case Handling SOP")


def recommend_next_best_action(priority, category, customer_tier):
    if priority == "High" and category == "Network / Connectivity":
        return "Create urgent escalation, notify network operations, and request customer impact details."
    elif priority == "High" and category == "Security":
        return "Escalate to security support, review access logs, and confirm affected users."
    elif priority == "High":
        return "Escalate to senior support team and provide immediate customer follow-up."
    elif category == "Billing":
        return "Route to billing support and request invoice number, billing period, and payment confirmation."
    elif category == "Portal Access":
        return "Guide customer through password reset, verify account status, and check admin permissions."
    elif category == "Hardware":
        return "Collect device details, error symptoms, and usage conditions before routing to hardware support."
    else:
        return "Assign to standard support queue and request any missing details from the customer."


def should_escalate(priority, customer_tier, category):
    if priority == "High":
        return "Yes"
    if customer_tier == "Enterprise" and category in ["Network / Connectivity", "Security"]:
        return "Yes"
    return "No"


def business_impact(priority, escalate):
    if priority == "High" and escalate == "Yes":
        return "Reduces response delay for urgent cases and helps support teams prioritize customer-impacting incidents."
    elif priority == "Medium":
        return "Improves routing consistency and reduces manual review effort for common support cases."
    else:
        return "Automates low-complexity triage so support teams can focus on higher-value customer issues."


st.title("🤖 Agentforce-Inspired Customer Support Triage Assistant")

st.write(
    "This prototype simulates how Salesforce Agentforce could support customer service teams "
    "by summarizing cases, classifying priority, recommending knowledge articles, and suggesting next-best actions."
)

df = pd.read_csv("support_cases.csv")

st.sidebar.header("Select a Support Case")

case_id = st.sidebar.selectbox("Choose a case:", df["case_id"].tolist())

selected_case = df[df["case_id"] == case_id].iloc[0]

customer_tier = selected_case["customer_tier"]
product_area = selected_case["product_area"]
customer_message = selected_case["customer_message"]

st.subheader("Original Customer Case")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Case ID", case_id)

with col2:
    st.metric("Customer Tier", customer_tier)

with col3:
    st.metric("Product Area", product_area)

st.text_area("Customer Message", customer_message, height=120)

summary = generate_summary(customer_message)
category = classify_category(customer_message, product_area)
priority = classify_priority(customer_message, customer_tier)
knowledge_article = recommend_knowledge_article(category)
next_action = recommend_next_best_action(priority, category, customer_tier)
escalate = should_escalate(priority, customer_tier, category)
impact = business_impact(priority, escalate)

st.subheader("Agentforce-Style Recommendation")

col4, col5, col6 = st.columns(3)

with col4:
    st.metric("Priority", priority)

with col5:
    st.metric("Category", category)

with col6:
    st.metric("Escalate?", escalate)

st.write("### Case Summary")
st.success(summary)

st.write("### Recommended Knowledge Article")
st.info(knowledge_article)

st.write("### Next-Best Action")
st.warning(next_action)

st.write("### Business Impact")
st.write(impact)

st.divider()

st.write("### Workflow Logic")
st.write(
    """
    1. Read incoming customer case  
    2. Summarize the issue  
    3. Classify category and priority  
    4. Recommend knowledge article  
    5. Suggest next-best action  
    6. Flag escalation if needed  
    """
)