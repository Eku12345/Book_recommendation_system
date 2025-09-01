import  streamlit as st
import pickle
import pandas as pd


def Recommendations(book):
    recommended_books = []
    matches = books[books['title'] == book]
    if matches.empty:
        print(f"Book title '{book}' not found in the dataset.")
        return

    book_index = matches.index[0]
    distances = similarity[book_index]
    books_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    for i in books_list:
        rec_index = i[0]
        title = books.iloc[rec_index].title
        isbn = books.iloc[rec_index].isbn13

        recommended_books.append({'title':title,'isbn': isbn})
    return recommended_books

def display_book_cover(title,isbn):

    url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"

    try:
        st.image(url,width=150,caption= title)
    except Exception as e:
        st.write(f"Cover image could not be retrieved  for {title}")



books_dict = pickle.load(open("data.pkl", "rb"))
books = pd.DataFrame(books_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))

st.title('Book Recommender System')
option = st.selectbox("Please select a book to get recommendations for",(books['title'].values))

if st.button("Recommendations"):
    recommends = Recommendations(option)
    cols = st.columns(len(recommends))
    for idx, book in enumerate(recommends):
        with cols[idx]:
            display_book_cover(book['title'],book['isbn'])


