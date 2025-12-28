import streamlit as st
import pickle
import string
import nltk
from password import check_password_strength



# ✅ Set NLTK data path to avoid lookup errors
nltk.data.path = ['C:/Users/neera/nltk_data']
nltk.download('stopwords')
nltk.download('punkt')
nltk.download("punkt_tab")

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# ✅ Initialize stemmer
ps = PorterStemmer()

# ✅ Text preprocessing function
def transform_text(text):
    text = text.lower()
    tokens = text.split()   # ✅ FIXED (no nltk tokenizer)

    words = [word for word in tokens if word.isalnum()]
    filtered = [
        word for word in words
        if word not in stopwords.words('english')
    ]
    stemmed = [ps.stem(word) for word in filtered]

    return " ".join(stemmed)


# ✅ Load vectorizer and model from pickle files
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

st.set_page_config(
    page_title="Cyber Awareness Project",
    page_icon="🔐",
    layout="centered"
)

import base64

def add_bg_from_local(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <style>
        /* Remove Streamlit side padding */
        .block-container {{
            padding-left: 0rem;
            padding-right: 0rem;
            padding-top: 0rem;
        }}

        /* Full-width hero */
        .hero {{
            background-image: url("data:image/webp;base64,{encoded}");
            background-size: cover;
            background-position: center;
            width: 100vw;
            min-height: 70vh;
            margin-left: calc(-50vw + 50%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: white;
            text-align: center;
        }}

        .hero h1 {{
            font-size: 48px;
            font-weight: 800;
            margin-bottom: 10px;
        }}

        .hero p {{
            font-size: 20px;
            max-width: 700px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local("hero.webp")


st.markdown(
    """
    <div class="hero">
        <h1>🔐 Cyber Awareness Project</h1>
        <p>Protecting users from weak passwords and online scams</p>
    </div>
    """,
    unsafe_allow_html=True
)



st.markdown("## 🔐 Password Strength Checker")
st.caption("Check how secure your password is. Passwords are never stored.")


password = st.text_input("Enter your password", type="password")

if st.button("Check Password Strength"):
    if password:
        strength, message = check_password_strength(password)

        if strength == "Weak":
            st.error(message)
        elif strength == "Medium":
            st.warning(message)
        else:
            st.success(message)
    else:
        st.warning("Please enter a password")

st.divider()

st.markdown("## 📩 Email / SMS Spam Detector")
st.caption("Paste any message to check if it is spam or safe.")

# ✅ Streamlit UI

input_sms = st.text_input("Enter your message")

if st.button("Predict"):
    # Preprocess the input
    transformed_text = transform_text(input_sms)

    # Vectorize the transformed input
    vector_input = tfidf.transform([transformed_text])

    # Predict using the trained model
    result = model.predict(vector_input)[0]

    # Display the result
    if result == 1:
        st.error("🚨 Spam")
    else:
        st.success("✅ Not Spam")


st.divider()

st.subheader("📚 Cyber Knowledge Hub")

st.markdown("""
- **Phishing:** Fake messages that steal personal or financial data  
- **OTP Fraud:** Never share OTP, even with bank staff  
- **Strong Password:** Use long, mixed, and unique passwords  
- **Public Wi-Fi:** Avoid banking on open networks  
- **Job Scams:** No real job asks for money  
- **Online Shopping:** Always check HTTPS & reviews  
- **Golden Rule 🚩:** Urgency + Fear = Red Flag
""")

st.divider()

st.subheader("🚨 Emergency & Help Links")

st.markdown("""
👉 [Report Cyber Crime (India)](https://cybercrime.gov.in)  
👉 Contact your bank immediately in case of fraud  
👉 Talk to trusted people before clicking suspicious links  
""")




st.divider()
st.caption("🛡️ Cyber Awareness Project | Built with Python & Streamlit")



