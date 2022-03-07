from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from io import StringIO
import numpy
import matplotlib.pyplot as plt

"""
@NirajRajPandey
"""

@st.cache
def convert_df(df):
   return df.to_csv().encode('utf-8')


# with st.echo(code_location='below'):
# with st.expander("💬 Open comments"):
column_name = st.text_input(label='Column Name', placeholder='Enter the Column Name and hit enter', key='columnName01')
st.write("We're checking column - '{}' to see if naming convention is accurate".format(column_name))

delimiter = st.text_input(label='Delimiter Sign', placeholder='Enter the Delimiter and hit enter', key='delimiter01')
st.write("We're counting Delimiter - '{}' in column - '{}' to see if naming convention is accurate".format(delimiter, column_name))

correct_delimiter_count = st.text_input(label='Delimiter Count', placeholder='Enter the total no. of delimiter in ideal case and hit enter', key='delimiterCount01')
st.write("In the '{}' column there should be a total of '{}' delimiters. Delimiters: {}".format(column_name, correct_delimiter_count, delimiter))

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)
    dataframe['delimiter_count'] = dataframe[column_name].str.count('\\|')
    correct_df = dataframe[dataframe['delimiter_count']==int(correct_delimiter_count)]
    incorrect_df = dataframe[dataframe['delimiter_count']!=int(correct_delimiter_count)]

    st.write("Below are the '{}' with incorrect Naming Conventions:".format(column_name))
    st.write(incorrect_df[[column_name,'delimiter_count']])
    incorrect_csv = convert_df(incorrect_df)
    st.download_button("Click to Download File with Incorrect {}".format(column_name),incorrect_csv,"Incorrect_{}.csv".format(column_name),"text/csv",key='downloadIncorrect01')

    st.write("Below are the '{}' with correct Naming Conventions:".format(column_name))
    st.write(correct_df[[column_name,'delimiter_count']])
    correct_csv = convert_df(incorrect_df)
    st.download_button("Click to Download File with Correct {}".format(column_name),correct_csv,"Correct_{}.csv".format(column_name),"text/csv",key='downloadCorrect01')

    dataframe['outcome'] = numpy.where(dataframe['delimiter_count']!= int(correct_delimiter_count), 'Incorrect', 'Correct')
    dataframe['dummy'] = 1

    # aggregated = dataframe.groupby('outcome').agg(num_cand_month = ('dummy', 'sum'))
    # aggregated.reset_index().rename({'index':'outcome'}, axis = 'columns')
    # st.write(aggregated)

    pivot_df = numpy.round(pd.pivot_table(dataframe, values=['dummy'], 
                            index=['outcome'], 
                            aggfunc=numpy.sum,
                            fill_value=0),2)
    
    
    pivot_df = pivot_df.reset_index().rename({'index':'outcome'}, axis = 'columns')
    st.write(pivot_df)
    st.altair_chart(alt.Chart(pivot_df, height=500, width=650).mark_arc().encode(theta=alt.Theta(field="dummy", type="quantitative"),color=alt.Color(field="outcome", type="nominal"),))


        # # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        # labels = pivot_df['outcome']
        # sizes = pivot_df['dummy']
        # fig1, ax1 = plt.subplots()
        # cmap = plt.get_cmap("tab20c")
        # outer_colors = cmap(numpy.arange(3)*4)
        # inner_colors = cmap(numpy.array([1, 2, 5, 6, 9, 10]))
        # ax1.pie(sizes, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90, colors=['green', 'red'])
        # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        # st.pyplot(fig1)


    # total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
    # num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

    # Point = namedtuple('Point', 'x y')
    # data = []

    # points_per_turn = total_points / num_turns

    # for curr_point_num in range(total_points):
    #     curr_turn, i = divmod(curr_point_num, points_per_turn)
    #     angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
    #     radius = curr_point_num / total_points
    #     x = radius * math.cos(angle)
    #     y = radius * math.sin(angle)
    #     data.append(Point(x, y))

    # st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
    #     .mark_circle(color='#0068c9', opacity=0.5)
    #     .encode(x='x:Q', y='y:Q'))