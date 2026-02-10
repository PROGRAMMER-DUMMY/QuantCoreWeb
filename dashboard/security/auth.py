import streamlit as st
import pyotp
import os
import time
from dotenv import load_dotenv

load_dotenv()

MAX_RETRIES = 3
LOCK_TIME = 60  # seconds


def render_login():
    """
    Renders the lock screen.
    Returns True if authenticated, False otherwise.
    """

    # -------------------------------
    # Initialize session state
    # -------------------------------
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "attempts" not in st.session_state:
        st.session_state.attempts = 0

    if "lock_until" not in st.session_state:
        st.session_state.lock_until = 0

    # -------------------------------
    # Already logged in
    # -------------------------------
    if st.session_state.authenticated:
        return True

    # -------------------------------
    # Lock check
    # -------------------------------
    lock_until = st.session_state.get("lock_until", 0)

    if time.time() < lock_until:
        remaining = int(lock_until - time.time())
        st.error(f" Too many attempts. Try again in {remaining}s")
        return False

    # -------------------------------
    # UI
    # -------------------------------
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("## QuantCore Secure Access")

        secret_key = os.getenv("DASHBOARD_2FA_SECRET")
        if not secret_key:
            st.error("Security Error: DASHBOARD_2FA_SECRET missing")
            st.stop()

        code = st.text_input(
            "Enter Google Authenticator Code",
            max_chars=6,
            type="password"
        )

        if st.button("Unlock Dashboard", use_container_width=True):
            totp = pyotp.TOTP(secret_key)

            if totp.verify(code, valid_window=1):
                # -------------------------------
                #  SUCCESS
                # -------------------------------
                st.session_state.authenticated = True
                st.session_state.attempts = 0
                st.session_state.lock_until = 0
                st.success(" Access Granted")
                time.sleep(0.3)
                st.rerun()

            else:
                # -------------------------------
                #    FAILURE
                # -------------------------------
                st.session_state.attempts += 1
                remaining = MAX_RETRIES - st.session_state.attempts

                if remaining <= 0:
                    st.session_state.lock_until = time.time() + LOCK_TIME
                    st.session_state.attempts = 0
                    st.error("Too many attempts. Locked for 60 seconds.")
                else:
                    st.error(f"Invalid code. {remaining} attempts left.")

    return False
