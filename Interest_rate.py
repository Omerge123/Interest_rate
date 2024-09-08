##### streamlit #####
import pandas as pd
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from pandas.tseries.offsets import MonthEnd
import numpy as np
import altair as alt

import streamlit as st

x = 'https://github.com/Omerge123/Interest_rate/raw/main/Interest_rate.xlsx'

source = pd.read_excel(x)

# get year
source["year"] = source['x'].dt.year
#Get the list of year for selection
year_choose  = source['year'].drop_duplicates().values.tolist()

st.set_page_config(layout='wide')
start_Year  = st.sidebar.selectbox('start',year_choose)
end_Year    = st.sidebar.selectbox('end',year_choose)

def rate_chart (start, end):
    source = pd.read_excel(x)
    source["year"] = source['x'].dt.year
    
    source = source[source['year'].between(start, end)]
   
    source2 = source[source['category'].isin(['US Treasury 3mth','US Treasury 10yr','Inflation','Fed'])]
    source3 = source[source['category'] == 'Recession (RHS)']
    
    columns = ["US Treasury 3mth", "US Treasury 10yr", "Inflation", "Fed","Recession (RHS)"]
    
    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection_point(nearest=True, on="pointerover",
                                  fields=["x"], empty=False)
    
    # The basic line
    line = alt.Chart(source2).mark_line(interpolate="basis").encode(
        x=alt.X('x:T', title='', axis=alt.Axis(format="%b%y") ), 
        y=alt.Y('y:Q', title='%'),
        color="category:N",
        strokeWidth=alt.value(2)
    )
    
    ##### The second basic line for right axis 
    line2 = alt.Chart(source3).mark_line().encode(
        x=alt.X('x:T', title='', axis=alt.Axis(format="%b%y") ), 
        y=alt.Y('y:Q', title='%'),
        color="category:N",
        strokeWidth=alt.value(2),
        strokeDash=alt.value([5,5])
    )
    
    # Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )
    
    # Draw a rule at the location of the selection
    rules = alt.Chart(source).transform_pivot(
        "category",
        value="y",
        groupby=["x"]
    ).mark_rule(color="gray").encode(
        x="x:T",
        opacity=alt.condition(nearest, alt.value(0.3), alt.value(0)),
        tooltip=[alt.Tooltip(a, type="quantitative", format=",.2f" ) for a in columns],
    
    ).add_params(nearest)
    
    # Put the five layers into a chart and bind the data
    chart = alt.layer(
        line , line2,  rules, #points,
    ).properties(
        width=900, height=450
    ).resolve_scale(y='independent').configure_legend(titleColor='black', 
                                                      titleOpacity=0,
                                                      titleFontSize=15, 
                                                      labelFontSize=15, 
                                                      labelFontWeight='normal' ,
                                                      symbolSize=100,
                                                      symbolStrokeWidth=10, )
    
    #return chart
    st.header("Interest Rate Cycle")
    st.altair_chart(chart, use_container_width=True, theme="streamlit")

rate_chart(start_Year, end_Year)

