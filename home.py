import streamlit as st
#from streamlit_option_menu import option_menu
import base64

#Sidebar


#Homepage
def app():
    # ubah gambar ke base64
    with open("logo.png", "rb") as f:
        data = base64.b64encode(f.read()).decode()

    # render card dengan gambar + teks di dalamnya
    st.markdown(
        f"""
        <div style="
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px 0;
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            ">
            <img src="data:image/png;base64,{data}" width="100">
            <h2 style="text-align: center;">Sistem Penentuan Kelayakan Bansos</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.write('<hr>', unsafe_allow_html=True)  # Add a horizontal line for separation

    # Teks
    st.markdown("""
    Selamat datang di aplikasi **Kelayakan Bansos**.Aplikasi ini membantu menentukan kelayakan keluarga penerima 
    bantuan sosial di tingkat **Desa**
    secara **objektif, transparan, dan tepat sasaran** 
    dengan metode *Fuzzy Tsukamoto* dan *Decision Tree*.
    """)
    # Layout dua kolom
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⚙️ **Cara Menggunakan**")
        st.markdown("""
        1. Buka **Menu Input Data**.  
        2. Pilih salah satu:
            - **Input Manual** → Isi form sesuai data keluarga.  
            - **File (CSV/Excel)** → Unggah file sesuai format template.  
        3. Setelah data dimasukkan, aplikasi akan menampilkan hasil **kelayakan**.   
        """)        

    with col2:
        st.subheader("🎯 Tujuan Aplikasi")
        st.write("""
        - Membantu proses seleksi calon penerima bansos.  
        - Menggunakan **Decision Tree** untuk membentuk aturan.  
        - Menggunakan **Fuzzy Tsukamoto** untuk menghasilkan nilai kelayakan.  
        """)

    st.write("")
    #Manfaat
    '''
    st.markdown("<h3>📑 Panduan Menu</h3>", unsafe_allow_html=True)
    st.success("""
    - **🏠 Beranda**  
    Menampilkan informasi umum, tujuan aplikasi, panduan menu, dan cara menggunakan aplikasi ini.
    
    - **📝 Input Data**  
    Digunakan untuk memasukkan data calon penerima bansos.  
    Tersedia 2 cara:  
        1. **Input Manual** → mengisi form data secara langsung.  
        2. **File (CSV/Excel)** → mengunggah file sesuai format yang sudah ditentukan.
        
    - **📂 Lainnya**  
    Berisi informasi detail model:  
        - **Rules** → Aturan fuzzy yang terbentuk.  
        - **Membership Function** → Fungsi keanggotaan setiap variabel.  
        - **Decision Tree** → Pohon keputusan hasil pelatihan model.
    """)
'''
    st.info("💡 Aplikasi ini merupakan implementasi dari penelitian skripsi 2025.")
    st.write("---")
    st.markdown("<p style='text-align: center;'>© 2025 - Nurhaliza</p>", unsafe_allow_html=True)
