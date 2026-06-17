import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Konfigurasi Halaman
st.set_page_config(page_title="Logika Fuzzy - Beasiswa", page_icon="🎁", layout="wide")

# --- 1. FUNGSI KEANGGOTAAN ---
def tidak_layak(x):
    if x <= 1.5: return 1.0
    elif 1.5 < x < 2.5: return (2.5 - x) / 1.0
    else: return 0.0

def dipertimbangkan(x):
    if 1.5 < x < 2.5: return (x - 1.5) / 1.0
    elif 2.5 <= x < 3.5: return (3.5 - x) / 1.0
    else: return 0.0

def layak(x):
    if 2.5 < x < 3.5: return (x - 2.5) / 1.0
    elif x >= 3.5: return 1.0
    else: return 0.0

# --- 2. ANTARMUKA PENGGUNA (UI) ---
st.title("🎁 Sistem Logika Fuzzy: Kelayakan Beasiswa")
st.markdown("---")

# Sidebar untuk Input
with st.sidebar:
    st.header("⚙️ Panel Input")
    st.info("Geser slider di bawah ini untuk memasukkan nilai IPK Mahasiswa.")
    ipk = st.slider("Nilai IPK (0.0 - 4.0)", min_value=0.0, max_value=4.0, value=3.1, step=0.05)

# --- 3. PERHITUNGAN DERAJAT KEANGGOTAAN ---
derajat = {
    "Tidak Layak": tidak_layak(ipk),
    "Dipertimbangkan": dipertimbangkan(ipk),
    "Layak": layak(ipk)
}

# --- 4. TAMPILAN HASIL & INTERPRETASI ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📊 Derajat Keanggotaan")
    st.markdown("Hasil perhitungan nilai fuzzy untuk IPK:")
    
    # Menampilkan metrik
    st.metric("Tidak Layak", f"{derajat['Tidak Layak']:.2f}")
    st.metric("Dipertimbangkan", f"{derajat['Dipertimbangkan']:.2f}")
    st.metric("Layak", f"{derajat['Layak']:.2f}")

    # Interpretasi Hasil
    st.subheader("💡 Interpretasi Hasil")
    # Mencari nilai derajat keanggotaan tertinggi
    kategori_dominan = max(derajat, key=derajat.get)
    nilai_dominan = derajat[kategori_dominan]
    
    if nilai_dominan > 0:
        st.success(f"Berdasarkan IPK **{ipk}**, status mahasiswa masuk dalam kategori **{kategori_dominan}** dengan tingkat keyakinan **{nilai_dominan:.2f}**.")
    else:
        st.warning("Nilai tidak terdefinisi dalam himpunan fuzzy.")

# --- 5. VISUALISASI GRAFIK ---
with col2:
    st.subheader("📈 Visualisasi Himpunan Fuzzy")
    
    # Membuat figure matplotlib
    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.linspace(0, 4, 500)
    
    y_tidak = [tidak_layak(i) for i in x]
    y_dipertimbangkan = [dipertimbangkan(i) for i in x]
    y_layak = [layak(i) for i in x]

    # Plot garis
    ax.plot(x, y_tidak, label='Tidak Layak', color='blue', linewidth=2)
    ax.plot(x, y_dipertimbangkan, label='Dipertimbangkan', color='green', linewidth=2)
    ax.plot(x, y_layak, label='Layak', color='red', linewidth=2)

    # Arsiran di bawah kurva
    ax.fill_between(x, y_tidak, alpha=0.1, color='blue')
    ax.fill_between(x, y_dipertimbangkan, alpha=0.1, color='green')
    ax.fill_between(x, y_layak, alpha=0.1, color='red')

    # Garis penanda input user
    ax.axvline(x=ipk, color='black', linestyle='--', linewidth=2, label=f'Input IPK: {ipk}')
    ax.scatter(ipk, 0, color='black', zorder=5)

    # Konfigurasi sumbu dan label
    ax.set_title("Grafik Fungsi Keanggotaan: Kelayakan Beasiswa")
    ax.set_xlabel("Domain IPK (0.0 - 4.0)")
    ax.set_ylabel("Derajat Keanggotaan \u03BC(x)")
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 1.1)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='center right')

    # Menampilkan plot di Streamlit
    st.pyplot(fig)