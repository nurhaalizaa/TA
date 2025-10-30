import streamlit as st
import home, input_data

# Sidebar menu
st.sidebar.image("menu.png",width=700)
st.sidebar.markdown(
    "<h2 style='text-align: center;'>Desa Pangarengan</h2>", 
    unsafe_allow_html=True
)

menu = st.sidebar.selectbox(
    "Menu Aplikasi",
    ["Beranda", "Input Data"],
    label_visibility="collapsed"
)

# Routing ke halaman
if menu == "Beranda":
    home.app()
elif menu == "Input Data":
    input_data.app()



