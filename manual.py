import streamlit as st
#import pandas as pd
import pickle
import numpy as np


# =========================
# Load model, encoder, scaler
# =========================
with open("label_mappings.pkl", "rb") as file:
    encoder = pickle.load(file)
# Load scaler
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)
# Load kembali
with open("fuzzy_model.pkl", "rb") as f:
    model_data = pickle.load(f)

parameters = model_data["parameters"]
rules_loaded = model_data["rules"]

# =========================
# Fungsi Keanggotaan & Fuzzy
# =========================
def triangular_mu(x, points):
    a, b, c = points

    # Bahu kiri (naik)
    if a == b:
        if x <= a:
            return 1.0
        elif x >= c:
            return 0.0
        else:
            return (c - x) / (c - a)

    # Bahu kanan (turun)
    elif b == c:
        if x <= a:
            return 0.0
        elif x >= c:
            return 1.0
        else:
            return (x - a) / (b - a)

    # Segitiga normal
    else:
        #if x <= a or x >= c:
         #   return 0.0
        if a < x < b:
            return (x - a) / (b - a)
        elif b < x < c:
            return (c - x) / (c - b)
        else:
            return 1.0
    
# =========================
# Fungsi fuzzy Tsukamoto untuk 1 baris data
# =========================
def fuzzy_tsukamoto(data_row, rules):
    alpha_list, z_list = [], []

    for i, (kondisi, output) in enumerate(rules, start=1):
        alphas = []

        for var, kategori_list in kondisi.items():
            # Pastikan kategori_list berbentuk list
            if not isinstance(kategori_list, list):
                kategori_list = [kategori_list]

            x = data_row[var]
            mu_values = []

            # Hitung µ untuk semua kategori dari variabel tsb
            for kategori in kategori_list:
                mu = triangular_mu(x, parameters[var][kategori])
                mu_values.append(mu)

            # Jika fitur punya lebih dari 1 kategori, ambil max
            # Jika hanya 1 kategori, pakai nilainya langsung
            if len(mu_values) > 1:
                mu_final = max(mu_values)
            else:
                mu_final = mu_values[0] if mu_values else 0

            alphas.append(mu_final)

        # α = min dari semua kondisi dalam rule
        alpha = min(alphas) if alphas else 0

        # Proses perhitungan z (konsekuen)
        if alpha > 0:
            if output.lower() == "layak":
                z = alpha
            else:
                z = 1 - alpha

            alpha_list.append(alpha)
            z_list.append(z)

    # Defuzzifikasi (rata-rata berbobot)
    hasil = (sum(a * z for a, z in zip(alpha_list, z_list)) /
             sum(alpha_list)) if sum(alpha_list) > 0 else 0

    return hasil


# =========================
# Fungsi preprocessing input
# =========================
def preprocess_input(df):
    df_proc = df.copy()
    # lowercase
    for col in df_proc.select_dtypes(include='object').columns:
        df_proc[col] = df_proc[col].str.lower()
    # apply mapping
    for col, mapping in encoder.items():
        if col in df_proc.columns:
            df_proc[col] = df_proc[col].map(mapping)
    # fitur numerik di-scaling
    fitur = ['Usia', 'Pendidikan', 'Jumlah_Keluarga', 
             'Jumlah_Tanggungan_Anak', 'Penghasilan', 'Luas_Bangunan']
    df_proc[fitur] = scaler.transform(df_proc[fitur])
    df_proc[fitur] = np.clip(df_proc[fitur], 0, 1)
    return df_proc

# =========================
# Fungsi hitung kelayakan
# =========================
def hitung_kelayakan(df):
    df_proc = df.copy()
    df_proc['Kelayakan'] = df_proc.apply(lambda row: fuzzy_tsukamoto(row, rules_loaded), axis=1)
    # Kolom keterangan layak/tidak
    df_proc['Keterangan'] = df_proc['Kelayakan'].apply(lambda x: "Layak" if x >= 0.5 else "Tidak Layak")
    return df_proc

# =========================
# Form input manual
# =========================
def input_form():
    # Baris 1: Nama & Usia
    col1, col2 = st.columns(2)
    with col1:
        Nama = st.text_input("Nama Kepala Keluarga", key="nama_kk")
    with col2:
        Usia = st.number_input("Usia", min_value=1, step=1, key="usia_kk")

    # Baris 2: Jumlah Keluarga & Jumlah Tanggungan Anak
    col1, col2 = st.columns(2)
    with col1:
        Jumlah_Keluarga = st.number_input("Jumlah Keluarga", min_value=1, step=1, key="jumlah_keluarga")
    with col2:
        Jumlah_Tanggungan_Anak = st.number_input("Jumlah Tanggungan Anak", min_value=0, step=1, key="jumlah_tanggungan")

    # Baris 3: Penghasilan & Luas Bangunan
    col1, col2 = st.columns(2)
    with col1:
        Penghasilan = st.number_input("Penghasilan per Bulan (Rp)", min_value=0, step=100000, key="penghasilan")
    with col2:
        Luas_Bangunan = st.number_input("Luas Bangunan (m²)", min_value=0, step=1, key="luas_bangunan")

    # Baris 4: Pendidikan & Status Rumah
    col1, col2 = st.columns(2)
    with col1:
        Pendidikan = st.selectbox(
            "Pendidikan Kepala Keluarga",
            ["SD", "SMP", "SMA", "D3", "S1"],
            key="pendidikan"
        )
    with col2:
        Status_Rumah = st.selectbox(
            "Status Rumah",
            ["Milik Sendiri", "Bebas Sewa"],
            key="status_rumah"
        )

    # Baris 5: Kepemilikan Jamban & Jenis Lantai
    col1, col2 = st.columns(2)
    with col1:
        Kepemilikan_Jamban = st.selectbox(
            "Kepemilikan Jamban",
            ["Pribadi", "Umum"],
            key="jamban"
        )
    with col2:
        Jenis_Lantai = st.selectbox(
            "Jenis Lantai",
            ["Semen", "Keramik"],
            key="lantai"
        )

    # Baris 6: Jenis Dinding & Sumber Penerangan
    col1, col2 = st.columns(2)
    with col1:
        Jenis_Dinding = st.selectbox(
            "Jenis Dinding",
            ["Bambu", "Batu Bata"],
            key="dinding"
        )
    with col2:
        Sumber_Penerangan = st.selectbox(
            "Sumber Penerangan",
            ["Listrik 450 VA", "Listrik 900 VA"],
            key="penerangan"
        )

    # Baris 7: Sumber Air Minum & Bahan Bakar Masak
    col1, col2 = st.columns(2)
    with col1:
        Sumber_Air_Minum = st.selectbox(
            "Sumber Air Minum",
            ["Sumur", "air kemasan/isi ulang"],
            key="air_minum"
        )
    with col2:
        Bahan_Bakar_Masak = st.selectbox(
            "Bahan Bakar Memasak",
            ["Gas 3 Kg", "Gas 5,5 Kg"],
            key="bahan_bakar"
        )
    
    if st.button("Prediksi", key="btn_prediksi"):
        return {
            "Nama": Nama,
            "Usia": Usia,
            "Jumlah_Keluarga": Jumlah_Keluarga,
            "Jumlah_Tanggungan_Anak": Jumlah_Tanggungan_Anak,
            "Penghasilan": Penghasilan,
            "Luas_Bangunan": Luas_Bangunan,
            "Pendidikan": Pendidikan,
            "Status_Rumah": Status_Rumah,
            "Kepemilikan_Jamban": Kepemilikan_Jamban,
            "Jenis_Lantai": Jenis_Lantai,
            "Jenis_Dinding": Jenis_Dinding,
            "Sumber_Penerangan": Sumber_Penerangan,
            "Sumber_Air_Minum": Sumber_Air_Minum,
            "Bahan_Bakar_Masak": Bahan_Bakar_Masak
        }
    return None
