from numpy.core.fromnumeric import size
import streamlit as st
import plotly.express as px
from datetime import date, datetime
import pymongo
import pandas as pd
import time

if 'client' not in st.session_state:
    st.session_state.client=pymongo.MongoClient(f"mongodb+srv://{st.secrets['uname']}:{st.secrets['pwd']}@cluster0.trwfg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
if 'db' not in st.session_state:
    st.session_state.db = st.session_state.client.get_database('study_db')
if 'cate' not in st.session_state:
    st.session_state.cate = st.session_state.db['category']
if 'scate' not in st.session_state:
    st.session_state.scate=st.session_state.db['sub-category']
if 'description' not in st.session_state:
    st.session_state.description = st.session_state.db['description']


def update_category(str1,str2):
    st.session_state.cate.insert_one({'category':str1,'logo-ref': str2})
def update_sub_category(str1,str2,str3):
    st.session_state.scate.insert_one({'category': str1,'sub-category':str2,'logo-ref': str3})

st.set_page_config(
        page_title="Learning Tracker",
        page_icon="books",
        layout="wide",
    )

def add_learning():
    x=[i['category'] for i in st.session_state.cate.find()]
    st.title("Hello Karthikeyan :smile:")
    st.header(f'Date: {datetime.date(datetime.now())}      Day: {datetime.date(datetime.now()).strftime("%A")}')
    selected_date=st.date_input("Enter date")
    col1, col2 = st.columns([3, 1])
    with col1:
        categories=st.selectbox("Select a category",x)
    with col2:
        val=[i['logo-ref'] for i in st.session_state.cate.find({'category':categories})]
        st.image(val,use_column_width=True)
        
    with st.expander("Couldn't found a category? To add one click '+'"):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write("")
            add_categoty = st.text_input('Add a category')
            add_categoty_ref = st.text_input('Add a category icon reference')
        with col2:
            st.write("")
            st.write("")
            st.write("")
            if st.button("Add to category","add_category_button","Press to add category"):
                update_category(add_categoty,add_categoty_ref)
                
    
    y=[i['sub-category'] for i in st.session_state.scate.find({'category' : categories})]
    col1, col2 = st.columns([1, 3])
    with col2:
        sub_categories=st.selectbox("Select a sub-category",y)
    with col1:
        sub_img=[i['logo-ref'] for i in st.session_state.scate.find({'sub-category':sub_categories})]
        st.image(sub_img,use_column_width=True)
    
    with st.expander("Couldn't found a sub-category? To add one click '+'"):
        sub_col1, sub_col2= st.columns([3,1])
        with sub_col1:
            add_sub_categoty = st.text_input('Add a sub-category')
            add_sub_categoty_ref = st.text_input('Add a sub-category icon reference')
        with sub_col2:
            st.write("")
            st.write("")
            st.write("")
            if st.button("Add to sub-category","add_sub-category_button","Press to add sub-category"):
                update_sub_category(categories,add_sub_categoty,add_sub_categoty_ref)
    
    txt = st.text_area('Topics Learnt Today')
    time=st.number_input("Enter time spent in learning(minutes))",0,1440,0,5)
    notes = st.text_area('Notes')
    reference=st.text_area("Put reference here for future use")
    dictionary={'Date':str(selected_date),'Time':time ,"Category":categories,"Sub_Category":sub_categories,"Topics":txt.splitlines(),"Notes":notes.splitlines(),"Reference":reference.splitlines()}
    if st.button("Add item to cloud"):
        st.session_state.description.insert_one(dictionary)

my_button = st.sidebar.radio("select a page", ('Add learning','Visualize learning')) 
if my_button=="Add learning":
    add_learning()
else:
    start_date=st.date_input('Start date')
    end_date=st.date_input('End date')
    if st.button("start visualizing"):
        l=[[i['Date'],i['Time'],i['Category'],i['Sub_Category'],i['Topics'],len(i['Topics']),i['Notes'],i['Reference']] for i in st.session_state.description.find({"Date": {"$gte": str(start_date), "$lte": str(end_date)}})]
        df=pd.DataFrame(l,columns=['Date','Time_Spent','Category','Sub_Category','Topics','num_of_topics','Notes','Reference'])
        #st.dataframe(df)
        fig=px.scatter(df,x='Date',y='Time_Spent',color='Sub_Category',size='num_of_topics',hover_name='Category',text='num_of_topics')
        st.plotly_chart(fig)
        s="{:<30} {:<75}\n".format("Title: "+'Monthly report',"Month: "+start_date.strftime("%B"))
        s+="{:<30} {:<75}\n\n\n".format("Start date: "+str(start_date),"End date: "+str(end_date))
        for i in l:
            s+=('_'*75)+'\n'
            s+="{:<30} {:<75}\n".format("Category: "+i[2],"Date: "+i[0])
            s+="{:<30} {:<75}\n".format("Sub-Category: "+i[3],"Time: "+str(i[1])+" minutes")
            s+=("Topics\n")
            for n,j in enumerate(i[4]):
                s+=f"{n+1}) {j}\n"
            s+=("Notes\n")
            for n,j in enumerate(i[6]):
                s+=f"{n+1}) {j}\n"
            s+=("References\n")
            for n,k in enumerate(i[7]):
                s+=f"{n+1}) {k}\n"
            s+=('_'*75)+'\n'
            s+=f"\n"
            s+=f"\n"
        st.title("Click to download monthly report")
        st.caption('Make sure you entered full range of month')
        st.download_button(label="DOWNLOAD!",data=s,file_name=f"{start_date.strftime('%B')}-{start_date.today().year}.txt",mime="text/plain")


