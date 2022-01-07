import streamlit as st
from datetime import date
from pymongo import MongoClient

client = pymongo.MongoClient("mongodb+srv://Shiva:Namachivaya@cluster0.trwfg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

def update_category(str1):
        cate.insert_one({'category':str1})

def update_sub_category(str1,str2):
        scate.insert_one({'category': str1,'sub-category':str2})


db = client.get_database('study_db')
cate = db['category']
scate=db['sub-category']
description = db['description']
x=[i['category'] for i in cate.find()]
y=[i['category'] for i in scate.find()]
st.title("Hi Karthikeyan :smile: {}".format(str(date.today())))
selected_date=st.date_input("Enter date")
categories=st.selectbox("Select a category",x)

with st.expander("Couldn't found a category? To add one click '+'"):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("")
        add_categoty = st.text_input('Add a category')
    with col2:
        st.write("")
        st.write("")
        st.write("")
        if st.button("Add to category","add_category_button","Press to add category"):
            update_category(add_categoty)
sub_categories=st.selectbox("Select a sub-category",y)
with st.expander("Couldn't found a sub-category? To add one click '+'"):
    sub_col1, sub_col2= st.columns([3,1])
    with sub_col1:
        add_sub_categoty = st.text_input('Add a sub-category')
    with sub_col2:
        st.write("")
        st.write("")
        st.write("")
        if st.button("Add to sub-category","add_sub-category_button","Press to add sub-category"):
            update_sub_category(categories,add_sub_categoty)
txt = st.text_area('Topics Learnt Today')
percentage_completed=st.number_input("Percentage completed",0,100,0)
notes = st.text_area('Note')
reference=st.text_input("Put reference here for future use")
dictionary={'Date':str(selected_date),"Category":categories,"Sub_Category":sub_categories,"Topics":str(txt.split('\n')),'Percentage_Completed':percentage_completed,"Notes":notes,"Reference":reference}
if st.button("Add item to cloud"):
    description.insert_one(dictionary)
client.close()
