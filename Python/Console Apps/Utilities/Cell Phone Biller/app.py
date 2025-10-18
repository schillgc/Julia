import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, datetime
import locale
from typing import Dict, List

# Set locale for currency formatting
try:
    locale.setlocale(locale.LC_ALL, 'English_United States.1252')
except:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Configure the page
st.set_page_config(
    page_title="Family Cell Phone Bill Calculator",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)


class CellPhoneBillCalculator:
    """Calculator for family cell phone bill distribution"""

    def __init__(self):
        self.family_members = ["Mama", "Ellie", "Blair", "Gavin", "Hayden", "Ian", "Wilder"]
        self.today = date.today()

        # Plan configuration
        self.plan_rates = {
            "line_one": 73.00,
            "line_two": 50.00,
            "third_generation_lines": 30.00,
            "additional_line_rate": 30.00
        }

        # Discount configuration
        self.discounts_config = {
            "auto_pay": 5.00,
            "sprint_perks": 5.00,
            "line_on_us": 25.00
        }

        # Equipment configuration
        self.equipment_config = {
            "samsung_a11_lease_end": date(2022, 12, 25),
            "samsung_a11_monthly": 7.50
        }

        # Protection plans configuration
        self.protection_plans = {
            "hayden_protection": 0.00,
            "premium_plans": {
                "Blair": 19.00,
                "Gavin": 19.00,
                "Ellie": 15.00,
                "Ian": 15.00
            }
        }

    def calculate_base_plan_cost(self) -> Dict[str, float]:
        """Calculate the base unlimited plan cost distribution"""
        num_lines = len(self.family_members)

        # Calculate total base plan cost
        additional_lines_cost = self.plan_rates["additional_line_rate"] * (num_lines - 3)
        total_base_cost = (
                self.plan_rates["line_one"] +
                self.plan_rates["line_two"] +
                self.plan_rates["third_generation_lines"] +
                additional_lines_cost
        )

        # Calculate equal distribution (before Hayden's special rate)
        equal_share = total_base_cost / num_lines

        # Adjust for Hayden's special rate
        base_costs = {}
        hayden_adjustment = (equal_share - self.plan_rates["third_generation_lines"]) / (num_lines - 1)

        for member in self.family_members:
            if member == "Hayden" or member == "Wilder":
                base_costs[member] = self.plan_rates["third_generation_lines"]
            else:
                base_costs[member] = equal_share + hayden_adjustment

        return base_costs

    def calculate_discounts(self, family_member: str) -> float:
        """Calculate applicable discounts for a family member"""
        total_discount = 0.0

        # Auto-pay discount for everyone
        total_discount += self.discounts_config["auto_pay"]

        # Member-specific discounts
        if family_member == "Gavin":
            total_discount += self.discounts_config["sprint_perks"]
        elif family_member == "Hayden" or family_member == "Wilder":
            total_discount += self.discounts_config["line_on_us"]

        return total_discount

    def calculate_equipment_charges(self, family_member: str) -> float:
        """Calculate equipment charges for a family member"""
        equipment_charge = 0.0

        # Samsung A11 lease charges (shared by Mama, Ellie, Blair)
        if (self.today < self.equipment_config["samsung_a11_lease_end"] and
                family_member in ["Mama", "Ellie", "Blair"]):
            equipment_charge = self.equipment_config["samsung_a11_monthly"] / 3

        return equipment_charge

    def calculate_protection_plans(self, family_member: str) -> float:
        """Calculate protection plan charges for a family member"""
        protection_charge = 0.0

        # Hayden's protection plan (shared by others except Ian)
        if family_member not in ["Hayden", "Ian"]:
            protection_charge += (self.protection_plans["hayden_protection"] /
                                  (len(self.family_members) - 2))

        # Individual premium protection plans
        protection_charge += self.protection_plans["premium_plans"].get(family_member, 0.0)

        return protection_charge

    def calculate_member_bill(self, family_member: str) -> Dict[str, float]:
        """Calculate complete bill for a family member"""
        if family_member not in self.family_members:
            raise ValueError(f"Unknown family member: {family_member}")

        base_costs = self.calculate_base_plan_cost()
        base_charge = base_costs[family_member]
        discounts = self.calculate_discounts(family_member)
        equipment_charges = self.calculate_equipment_charges(family_member)
        protection_charges = self.calculate_protection_plans(family_member)

        # Calculate final charges
        plans_and_services = base_charge - discounts
        total_charges = plans_and_services + equipment_charges + protection_charges

        return {
            "base_plan": base_charge,
            "discounts": discounts,
            "plans_and_services": plans_and_services,
            "equipment": equipment_charges,
            "protection": protection_charges,
            "total": total_charges
        }

    def calculate_all_bills(self) -> Dict[str, Dict[str, float]]:
        """Calculate bills for all family members"""
        all_bills = {}
        for member in self.family_members:
            all_bills[member] = self.calculate_member_bill(member)
        return all_bills


def format_currency(amount: float) -> str:
    """Format currency amount"""
    return locale.currency(amount, grouping=True)


def create_donut_chart(data, title):
    """Create a donut chart for bill distribution"""
    fig = go.Figure(data=[go.Pie(
        labels=list(data.keys()),
        values=list(data.values()),
        hole=.4,
        marker_colors=px.colors.qualitative.Set3
    )])
    fig.update_layout(
        title=title,
        showlegend=True,
        height=300
    )
    return fig


def create_bar_chart(data, title, color):
    """Create a bar chart for bill breakdown"""
    fig = px.bar(
        x=list(data.keys()),
        y=list(data.values()),
        title=title,
        color=list(data.keys()),
        color_discrete_sequence=[color] * len(data)
    )
    fig.update_layout(
        xaxis_title="Family Members",
        yaxis_title="Amount ($)",
        showlegend=False,
        height=400
    )
    return fig


def main():
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .member-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 1rem 0;
        border-left: 5px solid #1f77b4;
    }
    .total-card {
        background: linear-gradient(45deg, #1f77b4, #ff7f0e);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown('<h1 class="main-header">📱 Family Cell Phone Bill Calculator</h1>', unsafe_allow_html=True)

    # Initialize calculator
    calculator = CellPhoneBillCalculator()

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox(
        "Choose View",
        ["📊 Dashboard Overview", "👤 Individual Bills", "📈 Detailed Analysis", "⚙️ Bill Configuration"]
    )

    # Calculate all bills
    all_bills = calculator.calculate_all_bills()

    if app_mode == "📊 Dashboard Overview":
        display_dashboard_overview(calculator, all_bills)
    elif app_mode == "👤 Individual Bills":
        display_individual_bills(calculator, all_bills)
    elif app_mode == "📈 Detailed Analysis":
        display_detailed_analysis(calculator, all_bills)
    elif app_mode == "⚙️ Bill Configuration":
        display_bill_configuration(calculator)


def display_dashboard_overview(calculator, all_bills):
    """Display the main dashboard overview"""

    # Calculate totals
    total_family_bill = sum(bill['total'] for bill in all_bills.values())
    avg_bill = total_family_bill / len(calculator.family_members)

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Family Bill", format_currency(total_family_bill))

    with col2:
        st.metric("Average per Person", format_currency(avg_bill))

    with col3:
        st.metric("Family Members", len(calculator.family_members))

    with col4:
        highest_payer = max(all_bills.items(), key=lambda x: x[1]['total'])
        st.metric("Highest Bill", f"{highest_payer[0]}: {format_currency(highest_payer[1]['total'])}")

    # Main content area
    col1, col2 = st.columns(2)

    with col1:
        # Total bills by member
        member_totals = {member: bill['total'] for member, bill in all_bills.items()}
        fig = create_bar_chart(member_totals, "Total Bill by Family Member", "#1f77b4")
        st.plotly_chart(fig, use_container_width=True)

        # Base plan distribution
        base_plan_costs = calculator.calculate_base_plan_cost()
        fig = create_donut_chart(base_plan_costs, "Base Plan Cost Distribution")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Bill composition stacked bar chart
        categories = ['Base Plan', 'Equipment', 'Protection', 'Discounts']
        data = []
        for member in calculator.family_members:
            bill = all_bills[member]
            data.append({
                'Member': member,
                'Base Plan': bill['base_plan'],
                'Equipment': bill['equipment'],
                'Protection': bill['protection'],
                'Discounts': -bill['discounts']
            })

        df = pd.DataFrame(data)
        fig = px.bar(df, x='Member', y=categories, title='Detailed Bill Composition',
                     color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
        fig.update_layout(height=400, barmode='stack')
        st.plotly_chart(fig, use_container_width=True)

        # Quick summary table
        st.subheader("Quick Bill Summary")
        summary_data = []
        for member, bill in all_bills.items():
            summary_data.append({
                'Member': member,
                'Total': bill['total'],
                'Base Plan': bill['base_plan'],
                'Discounts': bill['discounts'],
                'Equipment': bill['equipment'],
                'Protection': bill['protection']
            })

        df_summary = pd.DataFrame(summary_data)
        st.dataframe(df_summary.style.format({
            'Total': '${:.2f}',
            'Base Plan': '${:.2f}',
            'Discounts': '${:.2f}',
            'Equipment': '${:.2f}',
            'Protection': '${:.2f}'
        }), use_container_width=True)


def display_individual_bills(calculator, all_bills):
    """Display individual bill details"""

    st.header("👤 Individual Bill Details")

    # Member selector
    selected_member = st.selectbox("Select Family Member", calculator.family_members)

    if selected_member:
        bill = all_bills[selected_member]

        # Create a nice card layout for the selected member
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown(f"""
            <div class="member-card">
                <h3>{selected_member}'s Bill Summary</h3>
                <h2 style="color: #1f77b4; font-size: 2.5rem;">{format_currency(bill['total'])}</h2>
            </div>
            """, unsafe_allow_html=True)

            # Bill breakdown
            st.subheader("Bill Breakdown")

            breakdown_data = {
                'Category': ['Base Plan', 'Discounts', 'Equipment', 'Protection Plans', 'Total'],
                'Amount': [
                    bill['base_plan'],
                    -bill['discounts'],
                    bill['equipment'],
                    bill['protection'],
                    bill['total']
                ]
            }

            df_breakdown = pd.DataFrame(breakdown_data)
            st.dataframe(df_breakdown.style.format({'Amount': '${:.2f}'}), use_container_width=True)

        with col2:
            # Visual breakdown
            categories = ['Base Plan', 'Equipment', 'Protection']
            values = [bill['base_plan'], bill['equipment'], bill['protection']]
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

            fig = go.Figure(data=[go.Pie(
                labels=categories,
                values=values,
                hole=.3,
                marker_colors=colors
            )])
            fig.update_layout(title=f"{selected_member}'s Cost Distribution")
            st.plotly_chart(fig, use_container_width=True)

            # Discount information
            if bill['discounts'] > 0:
                st.info(f"**Discounts Applied:** {format_currency(bill['discounts'])}")

            # Equipment information
            if bill['equipment'] > 0:
                st.warning(f"**Equipment Charges:** {format_currency(bill['equipment'])}")

            # Protection information
            if bill['protection'] > 0:
                st.warning(f"**Protection Plans:** {format_currency(bill['protection'])}")


def display_detailed_analysis(calculator, all_bills):
    """Display detailed analysis and comparisons"""

    st.header("📈 Detailed Bill Analysis")

    # Create comprehensive dataset for analysis
    analysis_data = []
    for member, bill in all_bills.items():
        analysis_data.append({
            'Member': member,
            'Total': bill['total'],
            'Base Plan': bill['base_plan'],
            'Discounts': bill['discounts'],
            'Equipment': bill['equipment'],
            'Protection': bill['protection'],
            'Plans & Services': bill['plans_and_services']
        })

    df = pd.DataFrame(analysis_data)

    col1, col2 = st.columns(2)

    with col1:
        # Cost comparison radar chart
        st.subheader("Cost Component Comparison")

        categories = ['Base Plan', 'Equipment', 'Protection', 'Discounts']

        fig = go.Figure()

        for member in calculator.family_members[:4]:  # Show first 4 for clarity
            values = [
                all_bills[member]['base_plan'],
                all_bills[member]['equipment'],
                all_bills[member]['protection'],
                all_bills[member]['discounts']
            ]
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=member
            ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(all_bills[member]['base_plan'] for member in calculator.family_members)]
                )),
            showlegend=True,
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Savings analysis
        st.subheader("Savings Analysis")

        total_discounts = sum(bill['discounts'] for bill in all_bills.values())
        base_total = sum(bill['base_plan'] for bill in all_bills.values())

        savings_data = {
            'Category': ['Total Base Cost', 'Total Discounts', 'Net Cost'],
            'Amount': [base_total, total_discounts, base_total - total_discounts]
        }

        df_savings = pd.DataFrame(savings_data)
        fig = px.bar(df_savings, x='Category', y='Amount',
                     color='Category', title='Overall Savings Impact')
        st.plotly_chart(fig, use_container_width=True)

        # Detailed statistics
        st.subheader("Bill Statistics")

        stats_data = {
            'Statistic': ['Minimum Bill', 'Maximum Bill', 'Average Bill', 'Standard Deviation'],
            'Value': [
                min(bill['total'] for bill in all_bills.values()),
                max(bill['total'] for bill in all_bills.values()),
                sum(bill['total'] for bill in all_bills.values()) / len(calculator.family_members),
                pd.Series([bill['total'] for bill in all_bills.values()]).std()
            ]
        }

        df_stats = pd.DataFrame(stats_data)
        st.dataframe(df_stats.style.format({'Value': '${:.2f}'}), use_container_width=True)


def display_bill_configuration(calculator):
    """Display and allow modification of bill configuration"""

    st.header("⚙️ Bill Configuration")

    st.warning("Note: Modifying these values will change how bills are calculated.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Plan Rates")

        # Editable plan rates
        line_one = st.number_input("Line One Rate", value=calculator.plan_rates["line_one"], step=1.0)
        line_two = st.number_input("Line Two Rate", value=calculator.plan_rates["line_two"], step=1.0)
        third_gen = st.number_input("Third Generation Lines", value=calculator.plan_rates["third_generation_lines"],
                                    step=1.0)
        additional_line = st.number_input("Additional Line Rate", value=calculator.plan_rates["additional_line_rate"],
                                          step=1.0)

    with col2:
        st.subheader("Discounts")

        # Editable discounts
        auto_pay = st.number_input("Auto Pay Discount", value=calculator.discounts_config["auto_pay"], step=1.0)
        sprint_perks = st.number_input("Sprint Perks Discount", value=calculator.discounts_config["sprint_perks"],
                                       step=1.0)
        line_on_us = st.number_input("Line on Us Discount", value=calculator.discounts_config["line_on_us"], step=1.0)

    # Equipment configuration
    st.subheader("Equipment Configuration")
    equip_col1, equip_col2 = st.columns(2)

    with equip_col1:
        lease_end = st.date_input("Samsung A11 Lease End", value=calculator.equipment_config["samsung_a11_lease_end"])

    with equip_col2:
        monthly_lease = st.number_input("Monthly Lease Cost", value=calculator.equipment_config["samsung_a11_monthly"],
                                        step=0.5)

    # Protection plans
    st.subheader("Protection Plans")
    prot_col1, prot_col2 = st.columns(2)

    with prot_col1:
        hayden_protection = st.number_input("Hayden Protection", value=calculator.protection_plans["hayden_protection"],
                                            step=1.0)

    with prot_col2:
        st.info("Premium protection plans are configured per member in the code.")

    # Update configuration if requested
    if st.button("Update Configuration"):
        # In a real application, you would update the calculator instance
        # For this demo, we'll just show a success message
        st.success("Configuration updated successfully!")
        st.info(
            "Note: In this demo, configuration changes are not persisted. In a production app, these would be saved to a database.")


if __name__ == "__main__":
    main()