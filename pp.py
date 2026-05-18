import streamlit as st
import random
import string
from firebase_config import db

# =========================================================
# PASSWORD GENERATOR
# =========================================================

def generate_password(length, use_upper, use_lower, use_digits, use_symbols):

    chars = ""

    if use_upper:
        chars += string.ascii_uppercase

    if use_lower:
        chars += string.ascii_lowercase

    if use_digits:
        chars += string.digits

    if use_symbols:
        chars += string.punctuation

    if chars == "":
        return None

    return "".join(random.choice(chars) for _ in range(length))


# =========================================================
# SAVE PASSWORD TO FIREBASE
# =========================================================

def save_password(site, username, password):

    data = {
        "site": site,
        "username": username,
        "password": password
    }

    db.collection("passwords").add(data)


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Password Manager",
    page_icon="🔐"
)

st.title("🔐 Password Manager")


# =========================================================
# MENU
# =========================================================

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Generate Password",
        "Save Custom Password",
        "View Saved Passwords",
        "Delete Password"
    ]
)


# =========================================================
# GENERATE PASSWORD
# =========================================================

if menu == "Generate Password":

    st.subheader("🔐 Generate Password")

    site = st.text_input("Website/App Name")
    username = st.text_input("Username / Email")

    length = st.slider(
        "Password Length",
        4,
        30,
        12
    )

    st.write("Select Password Options")

    use_upper = st.checkbox("Uppercase Letters (A-Z)", value=True)
    use_lower = st.checkbox("Lowercase Letters (a-z)", value=True)
    use_digits = st.checkbox("Numbers (0-9)", value=True)
    use_symbols = st.checkbox("Symbols (!@#$)", value=True)

    if st.button("Generate & Save Password"):

        if site and username:

            pwd = generate_password(
                length,
                use_upper,
                use_lower,
                use_digits,
                use_symbols
            )

            if pwd:

                save_password(site, username, pwd)

                st.success("✅ Password Generated & Saved")
                st.code(pwd)

            else:
                st.error("⚠️ Select at least one option")

        else:
            st.error("⚠️ Please fill all fields")


# =========================================================
# SAVE CUSTOM PASSWORD
# =========================================================

elif menu == "Save Custom Password":

    st.subheader("💾 Save Your Own Password")

    site = st.text_input("Website/App Name")
    username = st.text_input("Username / Email")

    custom_pwd = st.text_input(
        "Enter Password",
        type="password"
    )

    if st.button("Save Password"):

        if site and username and custom_pwd:

            save_password(site, username, custom_pwd)

            st.success("✅ Password Saved Successfully")

        else:
            st.error("⚠️ Please fill all fields")


# =========================================================
# VIEW SAVED PASSWORDS
# =========================================================

elif menu == "View Saved Passwords":

    st.subheader("📂 Saved Passwords")

    docs = db.collection("passwords").stream()

    found = False

    for doc in docs:

        found = True

        data = doc.to_dict()

        with st.expander(data["site"]):

            st.write(f"Username: {data['username']}")
            st.write(f"Password: {data['password']}")

    if not found:
        st.warning("❌ No passwords saved")


# =========================================================
# DELETE PASSWORD
# =========================================================

elif menu == "Delete Password":

    st.subheader("🗑️ Delete Password")

    site = st.text_input("Enter Website/App Name")

    if st.button("Delete Password"):

        docs = db.collection("passwords").stream()

        deleted = False

        for doc in docs:

            data = doc.to_dict()

            if data["site"] == site:

                db.collection("passwords").document(doc.id).delete()

                deleted = True

        if deleted:
            st.success("✅ Password Deleted")

        else:
            st.error("❌ Website not found")