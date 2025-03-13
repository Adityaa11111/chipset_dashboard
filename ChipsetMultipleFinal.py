import streamlit as st
import pandas as pd

def load_data(uploaded_file):
    """Loads CSV data and removes unnecessary index columns."""
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed', na=False)]  # Remove unnamed index columns
        if 'S.No' in df.columns:
            df = df.drop(columns=['S.No'])  # Remove 'S.No' if present
        return df
    return None

def add_serial_number(df):
    """Ensures 'Sr. No' column exists, starts from 1, and prevents duplicates."""
    df = df.copy().reset_index(drop=True)
    if "Sr. No" in df.columns:
        df = df.drop(columns=["Sr. No"])
    df.insert(0, "Sr. No", range(1, len(df) + 1))
    return df

def compare_chipsets(data_dict):
    """Compares chipset data across multiple years and ensures correct classification."""
    year_list = sorted(data_dict.keys())  # Sort years in ascending order
    chipset_history = {}  # Store chipsets per year
    added, removed, reappeared = [], [], []

    # Store chipsets for each year
    for year in year_list:
        current_chipsets = set(data_dict[year]['Chipset SP'].dropna().unique())  # Remove NaN values
        chipset_history[year] = current_chipsets

    # Find Added Chipsets (chipsets appearing for the first time in any year)
    all_previous_chipsets = set()
    for year in year_list:
        added_chipsets = chipset_history[year] - all_previous_chipsets  # Chipsets new in this year
        all_previous_chipsets.update(chipset_history[year])  # Update history
        added.extend(data_dict[year][data_dict[year]['Chipset SP'].isin(added_chipsets)].to_dict('records'))

    # Find Removed Chipsets (chipsets present in a year but missing in ALL later years)
    removed_chipsets_set = set()
    for i in range(len(year_list) - 1):  # Stop before the last year
        prev_year = year_list[i]
        later_years_chipsets = set().union(*[chipset_history[y] for y in year_list[i + 1:]])  # All future chipsets
        removed_chipsets = chipset_history[prev_year] - later_years_chipsets  # Only if missing in all later years
        removed_chipsets_set.update(removed_chipsets)
        removed.extend(data_dict[prev_year][data_dict[prev_year]['Chipset SP'].isin(removed_chipsets)].to_dict('records'))

    # Find Reappeared Chipsets (gone in one year, returned in a later year)
    reappeared_chipsets_set = set()
    for year in range(2, len(year_list)):  # Start from 2nd year to compare against two previous ones
        older_year, prev_year, curr_year = year_list[year - 2], year_list[year - 1], year_list[year]
        reappeared_chipsets = (chipset_history[older_year] - chipset_history[prev_year]) & chipset_history[curr_year]
        reappeared_chipsets_set.update(reappeared_chipsets)
        reappeared.extend(data_dict[curr_year][data_dict[curr_year]['Chipset SP'].isin(reappeared_chipsets)].to_dict('records'))

    removed = [entry for entry in removed if entry["Chipset SP"] not in reappeared_chipsets_set]
    removed = [entry for entry in removed if entry["Chipset SP"] in chipset_history[year_list[0]]]

    return add_serial_number(pd.DataFrame(added)), add_serial_number(pd.DataFrame(removed)), add_serial_number(pd.DataFrame(reappeared))

def main():
    st.title("📊 Multi-Year Chipset Sales Comparison")
    st.sidebar.header("📂 Upload CSV Files")
    uploaded_files = st.sidebar.file_uploader("Upload CSV Files (Multiple Years)", type=["csv"], accept_multiple_files=True)
    
    data_dict = {}
    if uploaded_files:
        for file in uploaded_files:
            year = file.name.split('.')[0][-4:]  # Extracting year from filename (Assuming format includes year)
            data_dict[year] = load_data(file)
    
    # Ensure all files have been assigned valid years
    years = sorted(data_dict.keys())
    
    if len(years) > 0:
        # Manual Data Entry
        st.sidebar.header("➕ Manually Add Chipset Data")
        selected_year = st.sidebar.selectbox("Select Year", years)
        new_chipset = st.sidebar.text_input("Chipset SP Code")
        new_customer = st.sidebar.text_input("Customer Details")
        new_pdm = st.sidebar.text_input("PDM Name")
        
        if "manual_entries" not in st.session_state:
            st.session_state.manual_entries = {year: pd.DataFrame(columns=["Chipset SP", "Customer", "PDM Name"]) for year in years}
        
        if st.sidebar.button("Add Entry"):
            new_entry = pd.DataFrame({
                "Chipset SP": [new_chipset], 
                "Customer": [new_customer],
                "PDM Name": [new_pdm]
            })
            st.session_state.manual_entries[selected_year] = pd.concat([st.session_state.manual_entries[selected_year], new_entry], ignore_index=True)
            st.sidebar.success("✅ Entry Added!")
            st.rerun()
        
        # Merge manual entries
        for year in years:
            data_dict[year] = pd.concat([data_dict[year], st.session_state.manual_entries[year]], ignore_index=True)
        
        # Display Data Preview
        st.subheader("📌 Data Preview")
        cols = st.columns(len(years)) if len(years) > 1 else [st]
        
        for i, year in enumerate(years):
            with cols[i]:
                st.write(f"### 📆 {year} Data")
                st.dataframe(add_serial_number(data_dict[year]).set_index("Sr. No"))
        
        # Compare Data
        added, removed, reappeared = compare_chipsets(data_dict)
        
        st.subheader("📊 Chipset Changes Across Years")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("### ✅ Added Chipsets")
            st.dataframe(added.set_index("Sr. No"))
        
        with col2:
            st.write("### ❌ Removed Chipsets")
            st.dataframe(removed.set_index("Sr. No"))
        
        with col3:
            st.write("### 🔄 Reappeared Chipsets")
            st.dataframe(reappeared.set_index("Sr. No"))
    else:
        st.error("Please upload at least one CSV file.")
        
if __name__ == "__main__":
    main()
