from pyspark import SparkContext, SQLContext

csv_datafile = "file:///home/schil/Downloads/MOCK_DATA.csv"
column1_header = "stock_symbol"
column2_header = "stock_name"
column3_header = "stock_market"
column4_header = "stock_sector"
column5_header = "stock_industry"
column6_header = "stock_market_cap"

# Initializations
sc = SparkContext("local", "Predictor")
sqlContext = SQLContext(sc)
