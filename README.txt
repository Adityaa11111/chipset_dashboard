Multi-Year Chipset Sales Comparison Dashboard
A Streamlit-based web application that allows users to compare chipset sales data across multiple financial years. This interactive dashboard helps in identifying added, removed, and reappeared chipsets with detailed customer insights.

Features
Upload multiple CSV files to analyze chipset trends across years
Manual data entry to add additional chipset details
Visual comparison of:

Added Chipsets → Newly introduced chipsets in the selected year
Removed Chipsets → Chipsets that no longer appear in later years
Reappeared Chipsets → Chipsets that were missing in a year but returned later
Automatic serial number assignment for easy tracking
Dynamic data previews with a user-friendly UI
CSV File Format
Ensure your dataset follows this structure:

Chipset SP	Customer	PDM Name
QCS600.LA.2.3.c25	ABC Corp	John Doe
QCS500.LA.2.3.c26	XYZ Ltd	Jane Smith
File Naming Convention: Your file names should end with the year (e.g., chipsets_2022.csv, chipsets_2023.csv).

Installation & Running the App
1️⃣ Clone the Repository
bash
git clone https://github.com/Adityaa11111/chipset_dashboard
cd chipset-comparison-dashboard
2️⃣ Install Dependencies
bash
pip install -r requirements.txt
3️⃣ Run the Streamlit App
bash
streamlit run ChipsetMultipleFinal.py

Technologies Used
Python 
Pandas 
Streamlit 

License
This project is licensed under the MIT License.

Contributing
Feel free to fork the repo, raise issues, or submit PRs to improve the app!

Author:
Aditya Choudhury| 📧 adityachoudhury170@gmail.com

