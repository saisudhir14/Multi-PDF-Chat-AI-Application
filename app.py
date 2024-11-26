import streamlit as st


def main():    
    st.set_page_config(page_title = "Chat with PDF's", page_icon=":books:")
    #print("hellow world! streamlit! let's lit!") 
    st.header("Chat with PDF's :books:")
    st.text_input("Ask questions based on the documents you provided:")
    
    with st.sidebar:
        st.subheader("Your Documents")
        st.file_uploader("Upload your PDF's here and click on process")
        st.button("Process")

if __name__ == '__main__':
    main()