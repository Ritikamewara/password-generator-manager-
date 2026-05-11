import streamlit as st
import random
import string
import json
import os

FILE = "passwords.json"


# ---------- LOAD ----------
def normalize_password_entry(entry):
    if isinstance(entry, dict):
        return {
            "username": entry.get("username", ""),
            "password": entry.get("password", "")
        }

    return {
        "username": "",
        "password": str(entry)
    }


def load_passwords():
    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r") as f:
        try:
            stored = json.load(f)
        except json.JSONDecodeError:
            return {}

    if isinstance(stored, dict):
        return {
            site: normalize_password_entry(entry)
            for site, entry in stored.items()
        }

    return {}


# ---------- SAVE ----------
def save_passwords(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


# ---------- PASSWORD GENERATOR ----------
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


# ---------- PAGE ----------
st.set_page_config(
    page_title="Password Manager",
    page_icon="🔐"
)

st.title("🔐 Password Manager")

# ---------- MENU ----------
menu = st.sidebar.selectbox(
    "Menu",
    [
        "Generate Password",
        "Save Custom Password",
        "View Saved Passwords",
        "Delete Password"
    ]
)

data = load_passwords()


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

                data[site] = {
                    "username": username,
                    "password": pwd
                }

                save_passwords(data)

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

            data[site] = {
                "username": username,
                "password": custom_pwd
            }

            save_passwords(data)

            st.success("✅ Password Saved Successfully")

        else:
            st.error("⚠️ Please fill all fields")


# =========================================================
# VIEW PASSWORDS
# =========================================================
elif menu == "View Saved Passwords":

    st.subheader("📂 Saved Passwords")

    if not data:
        st.warning("❌ No passwords saved")

    else:

        for site, info in data.items():

            with st.expander(site):

                st.write(
                    f"Username: {info['username']}"
                )

                st.write(
                    f"Password: {info['password']}"
                )


# =========================================================
# DELETE PASSWORD
# =========================================================
elif menu == "Delete Password":

    st.subheader("🗑️ Delete Password")

    site = st.text_input(
        "Enter Website/App Name"
    )

    if st.button("Delete Password"):

        if site in data:

            del data[site]

            save_passwords(data)

            st.success("✅ Password Deleted")

        else:
            st.error("❌ Website not found")