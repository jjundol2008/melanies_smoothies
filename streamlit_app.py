# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session # for Snowflake Streamlit
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:") # emoji https://docs.streamlit.io/develop/quick-reference/release-notes/2019
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

# lession 2에서는 삭제하고 시작한다
# option = st.selectbox(
#     "What is your favorite fruit?",
#     ("Banana", "Strawberries", "Peaches"),
# )

# st.write("You favorite fruit is:", option)

name_on_order = st.text_input('Name on Smoothie')
st.write('The cname on your Smoothie will be:', name_on_order)

# session활성화 및 데이터 가져오기

# session = get_active_session() # for Snowflake Streamlit
cnx = st.connection("snowflake")  # for  Streamlit
session = cnx.session()  # for  Streamlit

# my_dataframe = session.table("smoothies.public.fruit_options") #lesson01
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')) #lesson02
# st.dataframe(data=my_dataframe, use_container_width=True) #lesson02

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
) #lesson02

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # st.write(ingredients_string)

    # my_insert_stmt = """insert into
    # smoothies.public.orders(ingredients)
    # values('""" + ingredients_string + """')"""

    my_insert_stmt = """insert into
    smoothies.public.orders(ingredients, name_on_order)
    values('""" + ingredients_string + """','""" + name_on_order + """')"""

    # st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smootie is ordered,' + name_on_order + '!' , icon="✅")%