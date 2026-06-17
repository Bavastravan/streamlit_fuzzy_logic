import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Konfigurasi Halaman (Harus di baris paling atas)
st.set_page_config(page_title="Logika Fuzzy - Penilaian", page_icon="🎓", layout="wide")

# --- 1. FUNGSI KEANGGOTAAN ---
def rendah(x):
    if x <= 40: return 1.0
    elif 40 < x < 60: return (60 - x) / 20.0
    else: return 0.0

def sedang(x):
    if 40 < x <= 60: return (x - 40) / 20.0
    elif 60 < x < 80: return (80 - x) / 20.0
    else: return 0.0

def tinggi(x):
    if 60 < x < 80: return (x - 60) / 20.0
    elif x >= 80: return 1.0
    else: return 0.0

# --- 2. ANTARMUKA PENGGUNA (UI) ---
st.title("🎓 Sistem Logika Fuzzy: Penilaian Mahasiswa")
st.markdown("---")

# Sidebar untuk Input
with st.sidebar:
    st.header("⚙️ Panel Input")
    st.info("Geser slider di bawah ini untuk memasukkan nilai ujian mahasiswa.")
    nilai = st.slider("Nilai Ujian (0 - 100)", min_value=0.0, max_value=100.0, value=65.0, step=0.5)

# --- 3. PERHITUNGAN DERAJAT KEANGGOTAAN ---
derajat = {
    "Rendah": rendah(nilai),
    "Sedang": sedang(nilai),
    "Tinggi": tinggi(nilai)
}

# --- 4. TAMPILAN HASIL & INTERPRETASI ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📊 Derajat Keanggotaan")
    st.markdown("Hasil perhitungan nilai fuzzy:")
    
    # Menampilkan metrik dengan warna
    st.metric("Rendah", f"{derajat['Rendah']:.2f}")
    st.metric("Sedang", f"{derajat['Sedang']:.2f}")
    st.metric("Tinggi", f"{derajat['Tinggi']:.2f}")

    # Interpretasi Hasil
    st.subheader("💡 Interpretasi Hasil")
    # Mencari nilai derajat keanggotaan tertinggi
    kategori_dominan = max(derajat, key=derajat.get)
    nilai_dominan = derajat[kategori_dominan]
    
    if nilai_dominan > 0:
        st.success(f"Berdasarkan nilai **{nilai}**, mahasiswa masuk dalam kategori dominan **{kategori_dominan}** dengan tingkat keyakinan **{nilai_dominan:.2f}**.")
    else:
        st.warning("Nilai tidak terdefinisi dalam himpunan fuzzy.")

# --- 5. VISUALISASI GRAFIK ---
with col2:
    st.subheader("📈 Visualisasi Himpunan Fuzzy")
    
    # Membuat figure matplotlib
    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.linspace(0, 100, 500)
    
    y_rendah = [rendah(i) for i in x]
    y_sedang = [sedang(i) for i in x]
    y_tinggi = [tinggi(i) for i in x]

    # Plot garis
    ax.plot(x, y_rendah, label='Rendah', color='blue', linewidth=2)
    ax.plot(x, y_sedang, label='Sedang', color='green', linewidth=2)
    ax.plot(x, y_tinggi, label='Tinggi', color='red', linewidth=2)

    # Arsiran di bawah kurva (Opsional, mempercantik UI)
    ax.fill_between(x, y_rendah, alpha=0.1, color='blue')
    ax.fill_between(x, y_sedang, alpha=0.1, color='green')
    ax.fill_between(x, y_tinggi, alpha=0.1, color='red')

    # Garis penanda input user
    ax.axvline(x=nilai, color='black', linestyle='--', linewidth=2, label=f'Input Nilai: {nilai}')
    ax.scatter(nilai, 0, color='black', zorder=5) # Titik di sumbu x

    # Konfigurasi sumbu dan label
    ax.set_title("Grafik Fungsi Keanggotaan: Penilaian Mahasiswa")
    ax.set_xlabel("Domain Nilai Ujian (0 - 100)")
    ax.set_ylabel("Derajat Keanggotaan \u03BC(x)")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 1.1)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='center right')

    # Menampilkan plot di Streamlit
    st.pyplot(fig)