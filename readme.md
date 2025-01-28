# CSV Address Processor
This project processes CSV files containing postal codes and retrieves additional address and provider data via API calls. The script is designed to process multiple files in parallel and save the enriched data into new CSV files.

## 📂 Project Structure
```bash
├── done/               # Output folder for processed CSV files
├── split/              # Input folder for split CSV files
│   ├── output_1.csv    # Example input CSV file
│   ├── output_2.csv    # More input CSV files
├── start.sh            # Bash script to run the Python script in parallel
├── split/scape3.py     # Python script for processing
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
```

## 🛠️ Setup
1. Install Python Dependencies:

```bash
pip install -r requirements.txt
```

2. Add Input Files: Place your input CSV files in the split/ folder. Each file should contain a column named Zipcode:
```csv
Zipcode
1234AB
5678CD
```
## ⚙️ Usage
1. Run the Script: Use the start.sh script to process all input files concurrently:
```bash
./start.sh
```
2. View Results: Processed files will appear in the done/ folder.

## 📋Output Format
The output CSV will include:
 - `postal`: Postal code
 - `country`: Country
 - `city`: City
 - `street`: Street
 - `number`: House number
 - `providers`: Provider details (e.g., `Provider1 : Code1 | Provider2 : Code2`)

```csv
postal,country,city,street,number,providers
1234AB,NL,Amsterdam,Main Street,1,Provider1 : Code1 | Provider2 : Code2
```
## 🧹 Cleanup
Remove all output files:
```bash
rm -rf done/*.csv
```

## 📧 Support
For issues or suggestions, feel free to reach out.