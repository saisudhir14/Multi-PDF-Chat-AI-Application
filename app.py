import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter # Using this libary so that I can divide the text into chunks/ paragraphs using the class CharacterTextSplitter

#
def get_pdf_text(pdf_docs_store):
    text ="" # initalizing and storing all the text here from PDF
    for pdf in pdf_docs_store:
        pdf_reader = PdfReader(pdf) #creating PDF objects, read each page from PDF, adding this to the text
        for page in pdf_reader.pages:
            text += page.extract_text() #extracts raw text from the PDF -- appending/concat to text ==> read_raw_text
    return text
    
#
def get_the_text_in_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n" ,# single line break
        chunk_size = 1000, #characters
        chunk_overlap = 200 , # avoiding sentence, paragraphs overlap which will avoid the confusion / change in meaning of the text..
        length_function = len #len()
    )
    
    
    
    
    chunks = text_splitter.split_text(text)
    return chunks
    

def main():    
    load_dotenv()
    st.set_page_config(page_title = "Chat with PDF's", page_icon=":books:")
    #print("hellow world! streamlit! let's lit!") 
    st.header("Chat with PDF's :books:")
    st.text_input("Ask questions based on the documents you provided:")
    
    with st.sidebar:
        st.subheader("Your Documents")
        pdf_docs_store = st.file_uploader("Upload your PDF's here and click on 'Process'", accept_multiple_files=True)
        print(pdf_docs_store)
        if st.button("Process"):
            with st.spinner("Processing..."):
                #get the pdf text
                read_raw_text = get_pdf_text(pdf_docs_store)
                #st.write(read_raw_text) #testing by adding my PDF's to get the raw text if it is working by addig multiple PDF's
                
                #get the text chunks
                text_chunks = get_the_text_in_chunks(read_raw_text)
                st.write(text_chunks)
                
                #creating vector store // as a database            

if __name__ == '__main__':
    main()