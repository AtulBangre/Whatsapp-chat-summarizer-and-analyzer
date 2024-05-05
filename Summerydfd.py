'''import datetime
import streamlit as st
today = datetime.datetime.now().date()
d = st.date_input(
    "Select your vacation for next year",
    (today, today),
    format="MM.DD.YYYY",
)
print(d)'''

import datetime

tuple1 = (datetime.date(2024, 4, 10), datetime.date(2024, 4, 24))

# Converting each element of the tuple to datetime.date format
date1 = tuple1[0]
date2 = tuple1[1]

print(type(date1))  # Output: 2024-04-10
print(type(date2))  # Output: 2024-04-24