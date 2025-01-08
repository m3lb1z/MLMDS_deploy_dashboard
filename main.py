import streamlit as st # type: ignore
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt # type: ignore

URL = "https://raw.githubusercontent.com/marcopeix/MachineLearningModelDeploymentwithStreamlit/master/12_dashboard_capstone/data/quarterly_canada_population.csv"

@st.cache_data
def read_data():
	return pd.read_csv('data/canada_population.csv', dtype={'Quarter': str, 
								'Canada': np.int32,
								'Newfoundland and Labrador': np.int32,
								'Prince Edward Island': np.int32,
								'Nova Scotia': np.int32,
								'New Brunswick': np.int32,
								'Quebec': np.int32,
								'Ontario': np.int32,
								'Manitoba': np.int32,
								'Saskatchewan': np.int32,
								'Alberta': np.int32,
								'British Columbia': np.int32,
								'Yukon': np.int32,
								'Northwest Territories': np.int32,
								'Nunavut': np.int32})

@st.cache_data
def format_date_for_comparison(date):
    if date[1] == 2:
        return float(date[2:]) + 0.25
    elif date[1] == 3:
        return float(date[2:]) + 0.5
    elif date[1] == 4:
        return float(date[2:]) + 0.75
    else:
        return float(date[2:])

@st.cache_data
def end_before_start(start_date, end_date):
    num_start_date = format_date_for_comparison(start_date)
    num_end_date = format_date_for_comparison(end_date)

    if num_start_date > num_end_date:
        return True
    else:
        return False

def display_dashboard(start_date, end_date, target):
    tab1, tab2 = st.tabs(["Line Chart", "Second Chart"])

    with tab1:
        st.subheader(f"Population change {target} from {start_date} to {end_date}")
        col1, col2 = st.columns(2)

        with col1:
            initial = df.loc[df['Quarter'] == start_date, target].item()
            final = df.loc[df['Quarter'] == end_date, target].item()

            percentage_diff = round((final - initial) / initial * 100, 2)
            delta = f"{percentage_diff}%"
            st.metric(start_date, value=initial)
            st.metric(end_date, value=final, delta=delta)
        with col2:
            start_idx = df.loc[df['Quarter'] == start_date].index.item()
            end_idx = df.loc[df['Quarter'] == end_date].index.item()

            filtered_df = df.iloc[start_idx:end_idx+1]

            fig, ax = plt.subplots()
            ax.plot(filtered_df['Quarter'], filtered_df[target])
            ax.set_xlabel("Time")
            ax.set_ylabel("Population")
            ax.set_xticks([filtered_df['Quarter'].iloc[0], filtered_df['Quarter'].iloc[-1]])
            fig.autofmt_xdate()
            st.pyplot(fig)

    with tab2:
        st.subheader("Compare with other locations")
        all_targets = st.multiselect("Choose other locations", options=df.columns[1:], default=[target])

        fig, ax = plt.subplots()
        for each in all_targets:
            ax.plot(filtered_df['Quarter'], filtered_df[each])
        ax.set_xlabel("Time")
        ax.set_ylabel("Population")
        ax.set_xticks([filtered_df['Quarter'].iloc[0], filtered_df['Quarter'].iloc[-1]])
        st.pyplot(fig)



if __name__ == "__main__":
	df = read_data()
     
	st.title("Population of Canada")
	st.markdown("Source table can be found [here](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901)")


	with st.expander("Ver todos los datos en una tabla"):
		st.dataframe(df)
	
	with st.form("filter_form"):
		col1, col2, col3 = st.columns(3)
		with col1:
			start_quarter = st.selectbox("Choose a starting date", ["Q1", "Q2", "Q3", "Q4"], index=0, key="start_quarter")
			start_year = st.slider("Start Year", min_value=1991, max_value=2023, value=1991, step=1, key="start_year")
		with col2:
			end_quarter = st.selectbox("Choose a ending date", ["Q1", "Q2", "Q3", "Q4"], index=0, key="end_quarter")
			end_year = st.slider("End Year", min_value=1991, max_value=2023, value=2023, step=1, key="end_year")
		with col3:
			target = st.selectbox("Choose a location", df.columns[1:], index=0, key="target")
		submitted = st.form_submit_button("Analyze", type="primary")
		
	start_date = f"{start_quarter} {start_year}"
	end_date = f"{end_quarter} {end_year}"
    
	if start_date not in df['Quarter'].tolist() or end_date not in df['Quarter'].tolist():
		st.error("No data available. Check you quarter and year selection.")
	elif end_before_start(start_date, end_date):
		st.error("Dates don't work. Start date must come before end date.")
	else:
		display_dashboard(start_date, end_date, target)


