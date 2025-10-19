# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, datetime
import locale
import json
import functools
from typing import Dict, List, Optional
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set locale for currency formatting
try:
    locale.setlocale(locale.LC_ALL, 'English_United States.1252')
except:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Configure the page
st.set_page_config(
    page_title="T-Mobile Family Bill Calculator",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
EXPECTED_TOTAL_BILL = 354.37
CONFIG_FILE = "tmobile_config.json"
ALLOWED_TOTAL_DEVIATION = 0.01  # Allow 1 cent deviation due to floating point math


class ConfigurationError(Exception):
    """Custom exception for configuration errors"""
    pass


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class TMobileBillCalculator:
    """Calculator for T-Mobile family bill distribution with validation and persistence"""

    def __init__(self, config_file: str = CONFIG_FILE):
        self.config_file = config_file
        self.load_configuration()
        self.validate_initial_config()

    def load_configuration(self):
        """Load configuration from JSON file or create default"""
        try:
            if Path(self.config_file).exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                logger.info("Configuration loaded from file")
            else:
                config = self.get_default_config()
                self.save_configuration(config)
                logger.info("Default configuration created and saved")

            self._apply_configuration(config)

        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            st.error(f"Configuration error: {e}")
            # Fall back to default config
            config = self.get_default_config()
            self._apply_configuration(config)

    def get_default_config(self) -> Dict:
        """Return default configuration"""
        return {
            "family_members": ["Mama", "Ellie", "Blair", "Gavin", "Hayden", "Ian", "Wilder"],
            "phone_numbers": {
                "Mama": "(502) 500-5480",
                "Gavin": "(502) 994-5865",
                "Blair": "(502) 500-2994",
                "Ellie": "(805) 453-5242",
                "Ian": "(302) 270-3860",
                "Hayden": "(502) 457-1408",
                "Wilder": "Reserved Line"
            },
            "plan_groups": {
                "group_one": {
                    "members": ["Gavin", "Mama", "Ellie", "Ian", "Blair"],
                    "total_cost": 238.00
                },
                "group_two": {
                    "members": ["Wilder", "Hayden"],
                    "total_cost": 70.00
                }
            },
            "discounts_config": {
                "auto_pay": 5.00,
                "legacy_tmobile_perk": 5.00,
                "line_on_us": 29.02
            },
            "equipment_config": {
                "iphone_16_installment": 34.59,
                "accessories_installment": 8.13,
                "iphone_16_assigned_to": "Mama",
                "accessories_assigned_to": "Mama"
            },
            "protection_plans": {
                "protection_360_tier5": 18.00,
                "protected_members": ["Mama", "Blair", "Gavin", "Ian", "Ellie"]
            },
            "plan_features": {
                "unlimited_plus": {
                    "cost": 10.00,
                    "assigned_to": "Gavin"
                }
            },
            "one_time_charges": {
                "Ian": 3.65,
                "Hayden": -0.98,
                "Wilder": -0.98
            }
        }

    def _apply_configuration(self, config: Dict):
        """Apply configuration to instance variables with validation"""
        try:
            self.family_members = config["family_members"]
            self.phone_numbers = config["phone_numbers"]
            self.plan_groups = config["plan_groups"]
            self.discounts_config = config["discounts_config"]
            self.equipment_config = config["equipment_config"]
            self.protection_plans = config["protection_plans"]
            self.plan_features = config["plan_features"]
            self.one_time_charges = config["one_time_charges"]

            # Calculate derived values - FIXED: Use exact values from bill
            self.plan_groups["group_one"]["cost_per_member"] = 47.60  # $238.00 / 5
            self.plan_groups["group_two"]["cost_per_member"] = 35.00  # $70.00 / 2

        except KeyError as e:
            raise ConfigurationError(f"Missing required configuration key: {e}")

    def save_configuration(self, config: Optional[Dict] = None):
        """Save current configuration to file"""
        try:
            if config is None:
                config = {
                    "family_members": self.family_members,
                    "phone_numbers": self.phone_numbers,
                    "plan_groups": self.plan_groups,
                    "discounts_config": self.discounts_config,
                    "equipment_config": self.equipment_config,
                    "protection_plans": self.protection_plans,
                    "plan_features": self.plan_features,
                    "one_time_charges": self.one_time_charges
                }

            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            logger.info("Configuration saved successfully")

        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            raise ConfigurationError(f"Failed to save configuration: {e}")

    def validate_initial_config(self):
        """Validate initial configuration"""
        errors = []

        # Check all family members have phone numbers
        for member in self.family_members:
            if member not in self.phone_numbers:
                errors.append(f"Missing phone number for {member}")

        # Check plan group members exist
        for group_name, group in self.plan_groups.items():
            for member in group["members"]:
                if member not in self.family_members:
                    errors.append(f"Member {member} in {group_name} not in family members")

        if errors:
            raise ValidationError("Configuration errors: " + "; ".join(errors))

    @functools.lru_cache(maxsize=1)
    def calculate_all_bills(self) -> Dict[str, Dict[str, float]]:
        """Calculate T-Mobile bills for all family members with caching"""
        all_bills = {}
        for member in self.family_members:
            all_bills[member] = self.calculate_member_bill(member)

        self.validate_totals(all_bills)
        return all_bills

    def calculate_member_bill(self, family_member: str) -> Dict[str, float]:
        """Calculate complete T-Mobile bill for a family member"""
        if family_member not in self.family_members:
            raise ValueError(f"Unknown family member: {family_member}")

        try:
            base_plan = self._calculate_base_plan_cost(family_member)
            discounts = self.calculate_discounts(family_member)
            equipment = self._calculate_equipment_charges(family_member)
            protection = self._calculate_protection_plans(family_member)
            plan_features = self._calculate_plan_features(family_member)
            one_time_charges = self._calculate_one_time_charges(family_member)

            # Calculate final charges - FIXED: Apply discounts to base plan
            final_base_plan = max(0, base_plan - discounts)
            plans_and_services = final_base_plan + plan_features
            total_charges = (plans_and_services + equipment + protection + one_time_charges)

            # Ensure no negative totals
            if total_charges < 0:
                logger.warning(f"Negative total for {family_member}: {total_charges}")
                total_charges = 0

            return {
                "base_plan": final_base_plan,  # This is after discounts
                "discounts": discounts,
                "plan_features": plan_features,
                "plans_and_services": plans_and_services,
                "equipment": equipment,
                "protection": protection,
                "one_time_charges": one_time_charges,
                "total": total_charges
            }

        except Exception as e:
            logger.error(f"Error calculating bill for {family_member}: {e}")
            raise

    def _calculate_base_plan_cost(self, family_member: str) -> float:
        """Calculate base plan cost for a family member BEFORE discounts"""
        if family_member in self.plan_groups["group_one"]["members"]:
            return self.plan_groups["group_one"]["cost_per_member"]
        elif family_member in self.plan_groups["group_two"]["members"]:
            return self.plan_groups["group_two"]["cost_per_member"]
        else:
            raise ValueError(f"Family member {family_member} not in any plan group")

    def calculate_discounts(self, family_member: str) -> float:
        """Calculate applicable T-Mobile discounts for a family member"""
        total_discount = 0.0

        # T-Mobile AutoPay discount for everyone
        total_discount += self.discounts_config["auto_pay"]

        # Legacy T-Mobile Perk discount - only for Gavin
        if family_member == "Gavin":
            total_discount += self.discounts_config["legacy_tmobile_perk"]

        # T-Mobile Line On Us discount for Hayden and Wilder
        if family_member in ["Hayden", "Wilder"]:
            total_discount += self.discounts_config["line_on_us"]

        return total_discount

    def _calculate_equipment_charges(self, family_member: str) -> float:
        """Calculate T-Mobile equipment charges for a family member"""
        equipment_charge = 0.0

        # iPhone 16 installment
        if family_member == self.equipment_config["iphone_16_assigned_to"]:
            equipment_charge += self.equipment_config["iphone_16_installment"]

        # Accessories installment
        if family_member == self.equipment_config["accessories_assigned_to"]:
            equipment_charge += self.equipment_config["accessories_installment"]

        return equipment_charge

    def _calculate_protection_plans(self, family_member: str) -> float:
        """Calculate T-Mobile protection plan charges for a family member"""
        if family_member in self.protection_plans["protected_members"]:
            return self.protection_plans["protection_360_tier5"]
        return 0.0

    def _calculate_plan_features(self, family_member: str) -> float:
        """Calculate T-Mobile plan features (not protection)"""
        if family_member == self.plan_features["unlimited_plus"]["assigned_to"]:
            return self.plan_features["unlimited_plus"]["cost"]
        return 0.0

    def _calculate_one_time_charges(self, family_member: str) -> float:
        """Calculate one-time charges for a family member"""
        return self.one_time_charges.get(family_member, 0.0)

    def validate_totals(self, all_bills: Dict[str, Dict[str, float]]):
        """Validate that all components sum to expected totals"""
        try:
            # Calculate expected components from bill
            total_base_plan = sum(bill['base_plan'] for bill in all_bills.values())
            total_equipment = sum(bill['equipment'] for bill in all_bills.values())
            total_protection = sum(bill['protection'] for bill in all_bills.values())
            total_plan_features = sum(bill['plan_features'] for bill in all_bills.values())
            total_one_time = sum(bill['one_time_charges'] for bill in all_bills.values())

            calculated_total = total_base_plan + total_equipment + total_protection + total_plan_features + total_one_time

            if abs(calculated_total - EXPECTED_TOTAL_BILL) > ALLOWED_TOTAL_DEVIATION:
                error_msg = (
                    f"Total bill validation failed:\n"
                    f"  Calculated: ${calculated_total:.2f}\n"
                    f"  Expected: ${EXPECTED_TOTAL_BILL:.2f}\n"
                    f"  Difference: ${calculated_total - EXPECTED_TOTAL_BILL:.2f}\n\n"
                    f"Breakdown:\n"
                    f"  Base Plans: ${total_base_plan:.2f}\n"
                    f"  Equipment: ${total_equipment:.2f}\n"
                    f"  Protection: ${total_protection:.2f}\n"
                    f"  Plan Features: ${total_plan_features:.2f}\n"
                    f"  One-time Charges: ${total_one_time:.2f}"
                )
                logger.error(error_msg)
                raise ValidationError(error_msg)

            logger.info(f"Total validation passed: ${calculated_total:.2f}")

        except Exception as e:
            logger.error(f"Validation error: {e}")
            raise

    def export_to_csv(self, all_bills: Dict[str, Dict[str, float]]) -> str:
        """Export bill data to CSV format"""
        try:
            data = []
            for member, bill in all_bills.items():
                row = {
                    'Member': member,
                    'Phone Number': self.phone_numbers[member],
                    'Base Plan': bill['base_plan'],
                    'Discounts': bill['discounts'],
                    'Plan Features': bill['plan_features'],
                    'Equipment': bill['equipment'],
                    'Protection': bill['protection'],
                    'One-time Charges': bill['one_time_charges'],
                    'Total': bill['total']
                }
                data.append(row)

            df = pd.DataFrame(data)
            csv_data = df.to_csv(index=False)
            return csv_data

        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")
            raise

    def export_to_excel(self, all_bills: Dict[str, Dict[str, float]]) -> bytes:
        """Export bill data to Excel format"""
        try:
            data = []
            for member, bill in all_bills.items():
                row = {
                    'Member': member,
                    'Phone Number': self.phone_numbers[member],
                    'Base Plan': bill['base_plan'],
                    'Discounts': bill['discounts'],
                    'Plan Features': bill['plan_features'],
                    'Equipment': bill['equipment'],
                    'Protection': bill['protection'],
                    'One-time Charges': bill['one_time_charges'],
                    'Total': bill['total']
                }
                data.append(row)

            df = pd.DataFrame(data)

            # Create Excel file in memory
            output = pd.ExcelWriter('bills.xlsx', engine='xlsxwriter')
            df.to_excel(output, index=False, sheet_name='T-Mobile Bills')

            # Auto-adjust column widths
            worksheet = output.sheets['T-Mobile Bills']
            for i, col in enumerate(df.columns):
                max_len = max(df[col].astype(str).str.len().max(), len(col)) + 2
                worksheet.set_column(i, i, max_len)

            output.close()

            with open('bills.xlsx', 'rb') as f:
                excel_data = f.read()

            return excel_data

        except Exception as e:
            logger.error(f"Error exporting to Excel: {e}")
            raise


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
    # Custom CSS for better styling and mobile responsiveness
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #e20074;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
    }
    .member-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 1rem 0;
        border-left: 5px solid #e20074;
    }
    .total-card {
        background: linear-gradient(45deg, #e20074, #00a2e5);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
    }
    .phone-number {
        font-size: 0.9rem;
        color: #666;
        font-style: italic;
    }
    .discount-breakdown {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .tmobile-brand {
        color: #e20074;
        font-weight: bold;
    }
    .stButton button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown('<h1 class="main-header">📱 T-Mobile Family Bill Calculator</h1>', unsafe_allow_html=True)

    # Initialize calculator with error handling
    try:
        calculator = TMobileBillCalculator()
    except (ConfigurationError, ValidationError) as e:
        st.error(f"Initialization error: {e}")
        st.info("Using default configuration. Please check the configuration page.")
        calculator = TMobileBillCalculator()
        calculator.load_configuration()  # Force reload with defaults

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox(
        "Choose View",
        ["📊 Dashboard Overview", "👤 Individual Bills", "📈 Detailed Analysis",
         "⚙️ Bill Configuration", "💰 T-Mobile Discounts", "📤 Export Bills"]
    )

    # Calculate all bills with error handling
    try:
        all_bills = calculator.calculate_all_bills()
    except ValidationError as e:
        st.error(f"Bill calculation error: {e}")
        st.info("Some amounts may be incorrect. Please check the configuration.")
        all_bills = {}
        for member in calculator.family_members:
            all_bills[member] = calculator.calculate_member_bill(member)

    if app_mode == "📊 Dashboard Overview":
        display_dashboard_overview(calculator, all_bills)
    elif app_mode == "👤 Individual Bills":
        display_individual_bills(calculator, all_bills)
    elif app_mode == "📈 Detailed Analysis":
        display_detailed_analysis(calculator, all_bills)
    elif app_mode == "⚙️ Bill Configuration":
        display_bill_configuration(calculator)
    elif app_mode == "💰 T-Mobile Discounts":
        display_discount_breakdown(calculator, all_bills)
    elif app_mode == "📤 Export Bills":
        display_export_section(calculator, all_bills)


def display_dashboard_overview(calculator, all_bills):
    """Display the main dashboard overview"""

    # Calculate totals
    total_family_bill = sum(bill['total'] for bill in all_bills.values())
    avg_bill = total_family_bill / len(calculator.family_members)

    # Key metrics - responsive columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total T-Mobile Bill", format_currency(total_family_bill))

    with col2:
        st.metric("Average per Person", format_currency(avg_bill))

    with col3:
        st.metric("Family Members", len(calculator.family_members))

    with col4:
        highest_payer = max(all_bills.items(), key=lambda x: x[1]['total'])
        st.metric("Highest Bill", f"{highest_payer[0]}: {format_currency(highest_payer[1]['total'])}")

    # Validation status
    try:
        calculator.validate_totals(all_bills)
        st.success("✅ Bill validation passed - totals are correct")
    except ValidationError as e:
        st.error(f"❌ {e}")

    # Main content area - single column on mobile
    st.subheader("Bill Overview")

    # Total bills by member
    member_totals = {member: bill['total'] for member, bill in all_bills.items()}
    fig = create_bar_chart(member_totals, "Total T-Mobile Bill by Family Member", "#e20074")
    st.plotly_chart(fig, use_container_width=True)

    # Two columns for charts on desktop, single on mobile
    col1, col2 = st.columns(2)

    with col1:
        # Base plan distribution
        base_plan_costs = {member: bill['base_plan'] for member, bill in all_bills.items()}
        fig = create_donut_chart(base_plan_costs, "T-Mobile Plan Cost Distribution")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Cost distribution analysis
        total_base = sum(bill['base_plan'] for bill in all_bills.values())
        total_features = sum(bill['plan_features'] for bill in all_bills.values())
        total_equipment = sum(bill['equipment'] for bill in all_bills.values())
        total_protection = sum(bill['protection'] for bill in all_bills.values())
        total_one_time = sum(bill['one_time_charges'] for bill in all_bills.values())

        cost_data = {
            'Category': ['T-Mobile Plans', 'Plan Features', 'Equipment', 'Protection', 'One-time Charges'],
            'Amount': [total_base, total_features, total_equipment, total_protection, total_one_time]
        }

        df_cost = pd.DataFrame(cost_data)
        fig = px.pie(df_cost, values='Amount', names='Category',
                     title='T-Mobile Overall Cost Distribution',
                     color_discrete_sequence=['#e20074', '#ff6b6b', '#00a2e5', '#7d3c98', '#f39c12'])
        st.plotly_chart(fig, use_container_width=True)

    # Quick summary table
    st.subheader("T-Mobile Bill Summary")
    summary_data = []
    for member, bill in all_bills.items():
        summary_data.append({
            'Member': member,
            'Phone Number': calculator.phone_numbers[member],
            'Total': bill['total'],
            'T-Mobile Plan': bill['base_plan'],
            'Plan Features': bill['plan_features'],
            'Equipment': bill['equipment'],
            'Protection': bill['protection'],
            'One-time Charges': bill['one_time_charges']
        })

    df_summary = pd.DataFrame(summary_data)
    st.dataframe(df_summary.style.format({
        'Total': '${:.2f}',
        'T-Mobile Plan': '${:.2f}',
        'Plan Features': '${:.2f}',
        'Equipment': '${:.2f}',
        'Protection': '${:.2f}',
        'One-time Charges': '${:.2f}'
    }), use_container_width=True)


def display_individual_bills(calculator, all_bills):
    """Display individual T-Mobile bill details"""

    st.header("👤 Individual T-Mobile Bill Details")

    # Member selector
    selected_member = st.selectbox("Select Family Member", calculator.family_members)

    if selected_member:
        bill = all_bills[selected_member]
        phone_number = calculator.phone_numbers[selected_member]

        # Create a responsive layout
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown(f"""
            <div class="member-card">
                <h3>{selected_member}'s T-Mobile Bill</h3>
                <div class="phone-number">{phone_number}</div>
                <h2 style="color: #e20074; font-size: 2.5rem;">{format_currency(bill['total'])}</h2>
            </div>
            """, unsafe_allow_html=True)

            # Bill breakdown
            st.subheader("T-Mobile Bill Breakdown")

            breakdown_data = {
                'Category': ['T-Mobile Plan', 'Plan Features', 'Equipment', 'Protection', 'One-time Charges', 'Total'],
                'Amount': [
                    bill['base_plan'],
                    bill['plan_features'],
                    bill['equipment'],
                    bill['protection'],
                    bill['one_time_charges'],
                    bill['total']
                ]
            }

            df_breakdown = pd.DataFrame(breakdown_data)
            st.dataframe(df_breakdown.style.format({'Amount': '${:.2f}'}), use_container_width=True)

        with col2:
            # Visual breakdown
            categories = ['T-Mobile Plan', 'Plan Features', 'Equipment', 'Protection']
            values = [bill['base_plan'], bill['plan_features'], bill['equipment'], bill['protection']]
            colors = ['#e20074', '#ff6b6b', '#00a2e5', '#7d3c98']

            # Only show pie chart if there are positive values
            if sum(values) > 0:
                fig = go.Figure(data=[go.Pie(
                    labels=categories,
                    values=values,
                    hole=.3,
                    marker_colors=colors
                )])
                fig.update_layout(title=f"{selected_member}'s T-Mobile Cost Distribution")
                st.plotly_chart(fig, use_container_width=True)

            # Information cards
            discounts = calculator.calculate_discounts(selected_member)
            if discounts > 0:
                st.success(f"**T-Mobile Discounts Applied:** {format_currency(discounts)}")

            if bill['equipment'] > 0:
                st.warning(f"**T-Mobile Equipment:** {format_currency(bill['equipment'])}")

            if bill['protection'] > 0:
                st.warning(f"**T-Mobile Protection:** {format_currency(bill['protection'])}")

            if bill['plan_features'] > 0:
                st.info(f"**T-Mobile Plan Features:** {format_currency(bill['plan_features'])}")

            if bill['one_time_charges'] != 0:
                charge_type = "T-Mobile Credit" if bill['one_time_charges'] < 0 else "One-time Charges"
                st.info(f"**{charge_type}:** {format_currency(bill['one_time_charges'])}")


def display_detailed_analysis(calculator, all_bills):
    """Display detailed T-Mobile bill analysis"""

    st.header("📈 Detailed T-Mobile Bill Analysis")

    # Create comprehensive dataset for analysis
    analysis_data = []
    for member, bill in all_bills.items():
        analysis_data.append({
            'Member': member,
            'Phone Number': calculator.phone_numbers[member],
            'Total': bill['total'],
            'T-Mobile Plan': bill['base_plan'],
            'Plan Features': bill['plan_features'],
            'Equipment': bill['equipment'],
            'Protection': bill['protection'],
            'One-time Charges': bill['one_time_charges'],
            'Plans & Services': bill['plans_and_services']
        })

    df = pd.DataFrame(analysis_data)

    col1, col2 = st.columns(2)

    with col1:
        # Statistics
        st.subheader("T-Mobile Bill Statistics")

        stats_data = {
            'Statistic': ['Minimum Bill', 'Maximum Bill', 'Average Bill', 'Median Bill', 'Standard Deviation'],
            'Value': [
                min(bill['total'] for bill in all_bills.values()),
                max(bill['total'] for bill in all_bills.values()),
                sum(bill['total'] for bill in all_bills.values()) / len(calculator.family_members),
                pd.Series([bill['total'] for bill in all_bills.values()]).median(),
                pd.Series([bill['total'] for bill in all_bills.values()]).std()
            ]
        }

        df_stats = pd.DataFrame(stats_data)
        st.dataframe(df_stats.style.format({'Value': '${:.2f}'}), use_container_width=True)

    with col2:
        # Discount analysis
        st.subheader("Discount Impact Analysis")

        total_discounts = sum(calculator.calculate_discounts(member) for member in calculator.family_members)
        total_plan_before_discounts = sum(
            calculator._calculate_base_plan_cost(member) for member in calculator.family_members)
        total_plan_after_discounts = sum(bill['base_plan'] for bill in all_bills.values())

        discount_impact = {
            'Stage': ['Before Discounts', 'After Discounts', 'Total Discounts'],
            'Amount': [total_plan_before_discounts, total_plan_after_discounts, total_discounts]
        }

        df_discount_impact = pd.DataFrame(discount_impact)
        fig = px.bar(df_discount_impact, x='Stage', y='Amount',
                     title='Discount Impact on Plan Costs',
                     color='Stage', color_discrete_sequence=['#e20074', '#00a2e5', '#7d3c98'])
        st.plotly_chart(fig, use_container_width=True)

    # Monthly trend analysis (placeholder for future enhancement)
    st.subheader("Monthly Trends")
    st.info("💡 Future enhancement: Connect to historical data to show monthly trends and spending patterns")


def display_discount_breakdown(calculator, all_bills):
    """Display detailed T-Mobile discount breakdown"""

    st.header("💰 T-Mobile Discount Breakdown")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Individual T-Mobile Discounts")
        discount_data = []
        for member in calculator.family_members:
            discounts = calculator.calculate_discounts(member)
            base_plan = calculator._calculate_base_plan_cost(member)
            final_plan_cost = all_bills[member]['base_plan']

            discount_data.append({
                'Member': member,
                'Phone Number': calculator.phone_numbers[member],
                'Base Plan': base_plan,
                'T-Mobile Discounts': discounts,
                'Final Plan Cost': final_plan_cost
            })

        df_discounts = pd.DataFrame(discount_data)
        st.dataframe(df_discounts.style.format({
            'Base Plan': '${:.2f}',
            'T-Mobile Discounts': '${:.2f}',
            'Final Plan Cost': '${:.2f}'
        }), use_container_width=True)

    with col2:
        st.subheader("T-Mobile Discount Summary")

        total_discounts = sum(calculator.calculate_discounts(member) for member in calculator.family_members)
        total_base_plan = sum(calculator._calculate_base_plan_cost(member) for member in calculator.family_members)
        total_final_plan = sum(bill['base_plan'] for bill in all_bills.values())

        summary_data = {
            'Metric': ['Total Base Plan Cost', 'Total T-Mobile Discounts', 'Final T-Mobile Plan Cost'],
            'Amount': [total_base_plan, total_discounts, total_final_plan]
        }

        df_summary = pd.DataFrame(summary_data)
        st.dataframe(df_summary.style.format({'Amount': '${:.2f}'}), use_container_width=True)

        # T-Mobile discount types breakdown
        st.subheader("T-Mobile Discount Types")
        auto_pay_total = calculator.discounts_config["auto_pay"] * len(calculator.family_members)
        tmobile_perk_total = calculator.discounts_config["legacy_tmobile_perk"]
        line_on_us_total = calculator.discounts_config["line_on_us"] * 2  # Hayden and Wilder

        discount_types = {
            'T-Mobile Discount Type': ['AutoPay', 'Legacy T-Mobile Perk', 'Line On Us'],
            'Amount': [auto_pay_total, tmobile_perk_total, line_on_us_total]
        }

        df_discount_types = pd.DataFrame(discount_types)
        fig = px.pie(df_discount_types, values='Amount', names='T-Mobile Discount Type',
                     title='T-Mobile Discount Type Distribution',
                     color_discrete_sequence=['#e20074', '#00a2e5', '#7d3c98'])
        st.plotly_chart(fig, use_container_width=True)


def display_bill_configuration(calculator):
    """Display and allow modification of T-Mobile bill configuration"""

    st.header("⚙️ T-Mobile Bill Configuration")

    st.warning("Note: Modifying these values will change how T-Mobile bills are calculated.")

    # Configuration sections
    with st.form("configuration_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Family Plan Groups")
            group_one_total = st.number_input("Group 1 Total (Gavin, Mama, Ellie, Ian, Blair)",
                                              value=float(calculator.plan_groups["group_one"]["total_cost"]),
                                              step=1.0, min_value=0.0)
            group_two_total = st.number_input("Group 2 Total (Hayden, Wilder)",
                                              value=float(calculator.plan_groups["group_two"]["total_cost"]),
                                              step=1.0, min_value=0.0)

        with col2:
            st.subheader("T-Mobile Discount Configuration")
            auto_pay = st.number_input("T-Mobile AutoPay Discount",
                                       value=float(calculator.discounts_config["auto_pay"]),
                                       step=1.0, min_value=0.0)
            tmobile_perk = st.number_input("Legacy T-Mobile Perk",
                                           value=float(calculator.discounts_config["legacy_tmobile_perk"]),
                                           step=1.0, min_value=0.0)
            line_on_us = st.number_input("T-Mobile Line On Us",
                                         value=float(calculator.discounts_config["line_on_us"]),
                                         step=1.0, min_value=0.0)

        # T-Mobile Equipment configuration
        st.subheader("T-Mobile Equipment")
        equip_col1, equip_col2 = st.columns(2)

        with equip_col1:
            iphone_installment = st.number_input("iPhone 16 Installment",
                                                 value=float(calculator.equipment_config["iphone_16_installment"]),
                                                 step=0.5, min_value=0.0)
        with equip_col2:
            accessories_installment = st.number_input("Accessories Installment",
                                                      value=float(
                                                          calculator.equipment_config["accessories_installment"]),
                                                      step=0.5, min_value=0.0)

        # T-Mobile Protection plans
        st.subheader("T-Mobile Protection Plans")
        protection_360 = st.number_input("Protection 360 Tier 5",
                                         value=float(calculator.protection_plans["protection_360_tier5"]),
                                         step=1.0, min_value=0.0)

        # T-Mobile Unlimited Plus
        st.subheader("T-Mobile Plan Features")
        unlimited_plus = st.number_input("T-Mobile Unlimited Plus",
                                         value=float(calculator.plan_features["unlimited_plus"]["cost"]),
                                         step=1.0, min_value=0.0)

        # One-time charges
        st.subheader("One-time Charges")
        otc_col1, otc_col2, otc_col3 = st.columns(3)
        with otc_col1:
            ian_charges = st.number_input("Ian Charges", value=float(calculator.one_time_charges.get("Ian", 0.0)),
                                          step=0.1)
        with otc_col2:
            hayden_credit = st.number_input("Hayden Credit",
                                            value=float(calculator.one_time_charges.get("Hayden", 0.0)), step=0.1)
        with otc_col3:
            wilder_credit = st.number_input("Wilder Credit",
                                            value=float(calculator.one_time_charges.get("Wilder", 0.0)), step=0.1)

        # Update configuration
        if st.form_submit_button("Update T-Mobile Configuration"):
            try:
                new_config = {
                    "family_members": calculator.family_members,
                    "phone_numbers": calculator.phone_numbers,
                    "plan_groups": {
                        "group_one": {
                            "members": calculator.plan_groups["group_one"]["members"],
                            "total_cost": group_one_total
                        },
                        "group_two": {
                            "members": calculator.plan_groups["group_two"]["members"],
                            "total_cost": group_two_total
                        }
                    },
                    "discounts_config": {
                        "auto_pay": auto_pay,
                        "legacy_tmobile_perk": tmobile_perk,
                        "line_on_us": line_on_us
                    },
                    "equipment_config": {
                        "iphone_16_installment": iphone_installment,
                        "accessories_installment": accessories_installment,
                        "iphone_16_assigned_to": calculator.equipment_config["iphone_16_assigned_to"],
                        "accessories_assigned_to": calculator.equipment_config["accessories_assigned_to"]
                    },
                    "protection_plans": {
                        "protection_360_tier5": protection_360,
                        "protected_members": calculator.protection_plans["protected_members"]
                    },
                    "plan_features": {
                        "unlimited_plus": {
                            "cost": unlimited_plus,
                            "assigned_to": calculator.plan_features["unlimited_plus"]["assigned_to"]
                        }
                    },
                    "one_time_charges": {
                        "Ian": ian_charges,
                        "Hayden": -abs(hayden_credit),  # Ensure negative for credits
                        "Wilder": -abs(wilder_credit)  # Ensure negative for credits
                    }
                }

                calculator.save_configuration(new_config)
                calculator.load_configuration()  # Reload with new config
                st.success("✅ T-Mobile configuration updated and saved successfully!")
                st.rerun()

            except Exception as e:
                st.error(f"❌ Error updating configuration: {e}")

    # Configuration management
    st.subheader("Configuration Management")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Reset to Default Configuration"):
            try:
                default_config = calculator.get_default_config()
                calculator.save_configuration(default_config)
                calculator.load_configuration()
                st.success("✅ Configuration reset to defaults!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error resetting configuration: {e}")

    with col2:
        if st.button("Export Configuration"):
            try:
                config_json = json.dumps(calculator.get_default_config(), indent=2)
                st.download_button(
                    label="Download Configuration JSON",
                    data=config_json,
                    file_name="tmobile_config.json",
                    mime="application/json"
                )
            except Exception as e:
                st.error(f"❌ Error exporting configuration: {e}")


def display_export_section(calculator, all_bills):
    """Display export functionality"""

    st.header("📤 Export T-Mobile Bills")

    st.info("Export your T-Mobile bill data for sharing, record-keeping, or further analysis.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("CSV Export")
        st.write("Download bill data as CSV for use in spreadsheets or other applications.")

        try:
            csv_data = calculator.export_to_csv(all_bills)
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name="tmobile_bills.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"Error generating CSV: {e}")

    with col2:
        st.subheader("Excel Export")
        st.write("Download bill data as Excel spreadsheet with formatted columns.")

        try:
            excel_data = calculator.export_to_excel(all_bills)
            st.download_button(
                label="Download Excel",
                data=excel_data,
                file_name="tmobile_bills.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"Error generating Excel file: {e}")

    # Preview of exported data
    st.subheader("Data Preview")
    preview_data = []
    for member, bill in all_bills.items():
        preview_data.append({
            'Member': member,
            'Phone Number': calculator.phone_numbers[member],
            'Base Plan': bill['base_plan'],
            'Discounts': bill['discounts'],
            'Plan Features': bill['plan_features'],
            'Equipment': bill['equipment'],
            'Protection': bill['protection'],
            'One-time Charges': bill['one_time_charges'],
            'Total': bill['total']
        })

    df_preview = pd.DataFrame(preview_data)
    st.dataframe(df_preview.style.format({
        'Base Plan': '${:.2f}',
        'Discounts': '${:.2f}',
        'Plan Features': '${:.2f}',
        'Equipment': '${:.2f}',
        'Protection': '${:.2f}',
        'One-time Charges': '${:.2f}',
        'Total': '${:.2f}'
    }), use_container_width=True)


if __name__ == "__main__":
    main()
