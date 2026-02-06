import streamlit as st
import requests

from config.app_config import PRIMARY_COLOR, SECONDARY_COLOR


# ---------------- GITHUB STARS ---------------- #
@st.cache_data(ttl=3600)
def get_github_stars():
    """Fetch GitHub stars (cached 1 hour)"""
    try:
        response = requests.get(
            "https://api.github.com/repos/adi13apr/AI-Health-Assistant",
            timeout=5
        )
        if response.status_code == 200:
            return response.json().get("stargazers_count", 0)
    except Exception:
        pass
    return None


# ---------------- FOOTER ---------------- #
def show_footer():
    """Safe footer for main page + sidebar"""

    stars_count = get_github_stars()

    stars_html = ""
    if stars_count is not None:
        stars_html = f"""
        <span style="
            display:inline-flex;
            align-items:center;
            gap:4px;
            margin-left:6px;
            color:{SECONDARY_COLOR};
            font-size:11px;
        ">
            ⭐ {stars_count}
        </span>
        """

    footer_html = f"""
    <style>
    .custom-footer {{
        text-align:center;
        padding:12px;
        margin-top:20px;
        background:linear-gradient(
            to right,
            rgba(25,118,210,0.03),
            rgba(100,181,246,0.05),
            rgba(25,118,210,0.03)
        );
        border-top:1px solid rgba(100,181,246,0.15);
        font-size:12px;
        color:{SECONDARY_COLOR};
    }}

    .footer-link {{
        color:{PRIMARY_COLOR};
        text-decoration:none;
        font-weight:500;
    }}

    .footer-link:hover {{
        text-decoration:underline;
        color:{SECONDARY_COLOR};
    }}
    </style>

    <div class="custom-footer">

        <div>
            <a href="https://github.com/adi13apr/AI-Health-Assistant"
               target="_blank"
               class="footer-link">
               Contribute to HIA
            </a>
            {stars_html}
        </div>

        <div style="margin-top:6px;">
            <a href="https://github.com/adi13apr/AI-Health-Assistant"
               target="_blank"
               class="footer-link">
               Created by Aditya Chauhan
            </a>
        </div>

    </div>
    """

    st.markdown(footer_html, unsafe_allow_html=True)
