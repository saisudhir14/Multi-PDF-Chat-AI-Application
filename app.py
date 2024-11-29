import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter # Using this libary so that I can divide the text into chunks/ paragraphs using the class CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings #, HuggingFaceInstructEmbeddings
#you can also try using other embeddings.. such as instructor_base/large -- find this on huggingFace  https://huggingface.co/spaces/mteb/leaderboard   -- search here
from langchain.vectorstores import FAISS # try using Pinecone / Chroma / -- i'm using FAISS to just store my numberic representations of the text chunks
#I'm using FAISS as my vector store, I was looking for a vector store which runs locally, trying to store all my generative embeddings in my own machine.. instead of using cloud / other platform
#For now, I'm not using any persistent database, the data will however be erased when you close this application
#from sentence_transformers import SentenceTransformer

import os

#model = SentenceTransformer("hkunlp/instructor-xl")
#print("Model loaded successfully!")

def load_api_key():
    load_dotenv()  # Load from a .env file if available
    api_key = os.getenv("OPENAI_API_KEY")  # Check environment variables
    if not api_key:
        st.error("OpenAI API key not found. Set it as an environment variable or in the .env file.")
    return api_key


def get_vectorStore(text_chunks):
    try:
        embeddings = OpenAIEmbeddings()
        #embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    except Exception as e:
        st.error(f"Error initializing embeddings: {e}")
        return None  # or handle fallback logic
    vectorStore = FAISS.from_texts(texts=text_chunks, embedding=embeddings) #creating the database and generating from text
    return vectorStore
    



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
            if pdf_docs_store:  # Trying to check if PDFs are uploaded..
                print("test-- debug")
                with st.spinner("Processing..."):
                    #get the pdf text
                    read_raw_text = get_pdf_text(pdf_docs_store)
                    #st.write(read_raw_text) #testing by adding my PDF's to get the raw text if it is working by addig multiple PDF's
                    
                    #get the text chunks
                    text_chunks = get_the_text_in_chunks(read_raw_text)
                    st.write(text_chunks)
                    
                    #creating vector store // as a database    
                    vectorStore = get_vectorStore(text_chunks)
                    
                    st.success("Processing Complete. You can now query the documents..")
            else:
                #st.info("Upload your PDFs and click 'Process' to get started.")
                st.error("No PDFs uploaded. Please upload PDFs to proceed.")
                    
           

if __name__ == '__main__':
    main()