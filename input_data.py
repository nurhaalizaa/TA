import streamlit as st
import pandas as pd
import manual
from io import BytesIO
from manual import preprocess_input, hitung_kelayakan
#Input Data
def app():
    st.title("Input Data")
    tab1, tab2 = st.tabs(["📝 Manual", "📂 File"])
    #Manual
    with tab1:
        st.markdown("### Masukkan data keluarga calon penerima **Bansos**:")
        # Panggil form input manual
        new_data = manual.input_form()
        if new_data:
            df_raw = pd.DataFrame([new_data])
            df_preprocessed = preprocess_input(df_raw.copy())
            df_result = hitung_kelayakan(df_preprocessed)
            df_result["Keterangan"] = df_result["Kelayakan"].apply(
                lambda x: "Layak" if x > 0.5 else "Tidak Layak"
            )

            # Simpan di session_state khusus manual
            if "data_manual" not in st.session_state:
                st.session_state.data_manual = pd.DataFrame()
            st.session_state.data_manual = pd.concat(
                [st.session_state.data_manual, df_result], ignore_index=True
            )
            st.session_state.data_manual = st.session_state.data_manual.sort_values(
                by="Kelayakan", ascending=False
            ).reset_index(drop=True)

            # === Tampilkan hasil per tahap ===
            st.subheader("Data Calon Penerima Bansos")
            st.dataframe(df_raw)

            st.subheader("Data Setelah Preprocessing")
            st.dataframe(df_preprocessed)

            st.subheader("Hasil Kelayakan")
            st.dataframe(df_result[["Nama", "Kelayakan", "Keterangan"]])

        # Tampilkan tabel
        if "data_manual" in st.session_state and not st.session_state.data_manual.empty:
            st.subheader("Data Terkumpul")
            st.dataframe(st.session_state.data_manual[["Nama", "Kelayakan", "Keterangan"]])

            # Tombol hapus data manual
            if st.button("🗑️ Hapus Semua Data"):
                del st.session_state["data_manual"]
                st.success("Data berhasil dihapus!")

    #FILE
    with tab2:
        st.markdown("### Unggah Data File Calon Penerima Bansos")
        st.write("Silakan unggah file sesuai format yang telah ditentukan. "
                "Pastikan kolom input sudah sesuai agar dapat diproses dengan benar, untuk mempermudah proses silahkan menggunakan template dibawah.")
        # ==== 1. Download Template ====
        st.subheader("Unduh Template Input Data")
        template_df = pd.DataFrame(columns=[
            "Nama","NoKK","Dusun", "Usia", "Pendidikan", "Jumlah_Keluarga", "Jumlah_Tanggungan_Anak",
            "Penghasilan", "Status_Rumah", "Luas_Bangunan", "Kepemilikan_Jamban",  "Jenis_Lantai",
            "Jenis_Dinding", "Sumber_Penerangan", "Sumber_Air_Minum", "Bahan_Bakar_Masak"
        ])
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            template_df.to_excel(writer, index=False, sheet_name="Template")

        st.download_button(
            label="📥 Download Template Excel",
            data=buffer.getvalue(),
            file_name="template_input_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        uploaded_file = st.file_uploader("Pilih file", type=["csv", "xlsx", "xls"])
        if uploaded_file is not None:
            # === 1. Baca file sesuai format ===
            if uploaded_file.name.endswith(".csv"):
                df_raw = pd.read_csv(uploaded_file)
            else:
                df_raw = pd.read_excel(uploaded_file)

            # Baca&tampilkan CSV pakai pandas
            #df_raw = pd.read_csv(uploaded_file)
            st.subheader("Data Calon Penerima Bansos")
            st.dataframe(df_raw)
            st.write("Jumlah baris:", df_raw.shape[0])
            st.write("Jumlah kolom:", df_raw.shape[1])

            # preprocessing
            df = preprocess_input(df_raw.copy())
            kolom_identitas = ["Nama", "NoKK", "Dusun"]
            kolom_preprocessed = [col for col in df.columns if col not in kolom_identitas]
            st.subheader("Data Setelah Preprocessing")
            st.dataframe(df[kolom_preprocessed])

            #Menghitung kelayakan
            df = hitung_kelayakan(df)
            df["Keterangan"] = df["Kelayakan"].apply(
                lambda x: "Layak" if x > 0.5 else "Tidak Layak"
            )

            # Simpan di session_state khusus file
            if "data_file" not in st.session_state:
                st.session_state.data_file = pd.DataFrame()
            st.session_state.data_file = pd.concat(
                [st.session_state.data_file, df], ignore_index=True
            )
            st.session_state.data_file = st.session_state.data_file.sort_values(
                by="Kelayakan", ascending=False
            ).reset_index(drop=True)
            st.subheader("Hasil Kelayakan")
            st.dataframe(st.session_state.data_file[["Nama", "Dusun", "Kelayakan", "Keterangan"]])
        # Tombol hapus data file
        if "data_file" in st.session_state and not st.session_state.data_file.empty:
            if st.button("🗑️ Hapus Data"):
                del st.session_state["data_file"]
                st.success("Data berhasil dihapus!")