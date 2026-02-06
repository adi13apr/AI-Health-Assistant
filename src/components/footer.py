import streamlit as st

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="HIA - Health Insights Agent",
    layout="wide"
)

# ---------------- FOOTER FUNCTION ---------------- #
def show_footer():

    footer_html = """
    <style>
    .footer {
        text-align: center;
        padding: 12px;
        margin-top: 40px;
        background: linear-gradient(
            to right,
            rgba(25,118,210,0.03),
            rgba(100,181,246,0.05),
            rgba(25,118,210,0.03)
        );
        border-top: 1px solid rgba(100,181,246,0.15);
        font-size: 12px;
        color: #64B5F6;
    }

    .footer a {
        color: #1976D2;
        text-decoration: none;
        font-weight: 500;
    }

    .footer a:hover {
        text-decoration: underline;
        color: #64B5F6;
    }
    </style>

    <div class="footer">
        <a href="https://github.com/adi13apr/AI-Health-Assistant" target="_blank">
        </a>
    </div>
    """

    st.markdown(footer_html, unsafe_allow_html=True)


# ---------------- CALL FOOTER ---------------- #
show_footer()
