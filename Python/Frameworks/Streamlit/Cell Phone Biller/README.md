# 📱 T-Mobile Family Bill Calculator

A comprehensive Streamlit application for calculating and distributing T-Mobile family cell phone bills among family members with complex discount structures and cost sharing arrangements.

## ✨ Features

- **📊 Dashboard Overview**: Visual breakdown of family bill distribution
- **👤 Individual Bills**: Detailed view for each family member
- **📈 Detailed Analysis**: Statistical analysis and cost comparisons
- **⚙️ Bill Configuration**: Customizable plan costs, discounts, and assignments
- **💰 Discount Breakdown**: Detailed discount analysis and impact
- **📤 Export Functionality**: Export bills to CSV and Excel formats
- **✅ Validation**: Automatic bill total validation ($354.37 target)
- **💾 Persistence**: Configuration automatically saved to JSON file

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation

1. **Clone or download the project files**:
   ```
   t-mobile-calculator/
   ├── app.py
   ├── requirements.txt
   └── tmobile_config.json
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** to the displayed URL (typically http://localhost:8501)

## 📋 Usage

### Dashboard Overview
- View total family bill and individual member costs
- See visual charts of cost distribution
- Check validation status to ensure totals match expected bill amount

### Individual Bills
- Select any family member to see their detailed bill breakdown
- View base plan costs, discounts, equipment charges, and protection plans
- See visual cost distribution pie charts

### Configuration
- Modify plan costs, discounts, and assignments in real-time
- Changes are automatically saved to `tmobile_config.json`
- Reset to defaults if needed

### Export Data
- Download bill data as CSV for spreadsheet analysis
- Export to Excel with formatted columns
- Perfect for record-keeping and sharing with family members

## ⚙️ Configuration

The app uses `tmobile_config.json` to store:

- **Family Members**: Names and phone numbers
- **Plan Groups**: Cost splitting arrangements
  - Group 1: Gavin, Mama, Ellie, Ian, Blair ($238.00 total)
  - Group 2: Hayden, Wilder ($70.00 total)
- **Discounts**: AutoPay, Legacy T-Mobile Perk, Line On Us
- **Equipment**: iPhone and accessories assignments
- **Protection Plans**: Protection 360 assignments
- **Plan Features**: Unlimited Plus assignments
- **One-time Charges**: Usage charges and credits

## 🧮 Bill Structure

The calculator handles complex cost distribution:

### Base Plan Costs
- **Group 1**: $47.60 per person ($238.00 ÷ 5)
- **Group 2**: $35.00 per person ($70.00 ÷ 2)

### Discounts Applied
- **AutoPay**: $5.00 for every line
- **Legacy T-Mobile Perk**: $5.00 for Gavin only
- **Line On Us**: $29.02 for Hayden and Wilder

### Additional Charges
- **Equipment**: iPhone 16 installment + accessories
- **Protection**: Protection 360 for 5 lines
- **Plan Features**: Unlimited Plus for Gavin
- **One-time**: Usage charges and credits

## 🔧 Customization

### Modifying Family Members
Edit the `family_members` and `phone_numbers` sections in `tmobile_config.json` or use the configuration page in the app.

### Adjusting Plan Costs
Update the `plan_groups` section to modify cost splitting arrangements.

### Changing Discounts
Modify the `discounts_config` section to reflect current T-Mobile promotions.

## 🐛 Troubleshooting

### Common Issues

**"Total bill validation failed"**
- Check that all cost components sum to $354.37
- Verify discount amounts are correctly applied
- Ensure no negative totals for any family member

**Configuration errors**
- Delete `tmobile_config.json` to regenerate default configuration
- Check file permissions for write access

**Import errors**
- Run `pip install -r requirements.txt` to ensure all dependencies are installed
- Verify Python version is 3.7 or newer

### Validation
The app includes comprehensive validation to ensure:
- Total bill equals $354.37 (± $0.01)
- No family member has negative charges
- All configuration values are valid

## 📁 Project Structure

```
t-mobile-calculator/
├── app.py                 # Main Streamlit application
├── tmobile_config.json    # Configuration file (auto-created)
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔮 Future Enhancements

- **Historical Tracking**: Month-over-month bill comparison
- **Payment Tracking**: Record actual payments from family members
- **Notification System**: Email/SMS reminders for family members
- **Multiple Bill Support**: Handle other recurring family bills
- **Advanced Analytics**: Spending trends and cost optimization suggestions

## 🤝 Contributing

This is a personal family bill calculator, but suggestions are welcome!

## 📄 License

This project is for personal use.

## 💡 Tips

- **Bookmark** the Streamlit URL for easy access
- **Export monthly** to maintain bill history
- **Update configuration** when T-Mobile plans or promotions change
- **Use the validation feature** to catch calculation errors early

## 📞 Support

For issues with the calculator:
1. Check the troubleshooting section above
2. Verify your configuration matches your actual T-Mobile bill
3. Ensure all dependencies are properly installed

---

**Happy Bill Calculating!** 🎉