import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Konfigurasi Halaman
st.set_page_config(page_title="Logika Fuzzy - Kemacetan", page_icon="🚗", layout="wide")

# --- 1. FUNGSI KEANGGOTAAN ---
# Perbaikan: Menggunakan domain 0 - 1000 sesuai gambar instruksi
def lancar(x):
    if x <= 300: return 1.0
    elif 300 < x < 500: return (500 - x) / 200.0
    else: return 0.0

def padat(x):
    if 300 < x <= 500: return (x - 300) / 200.0
    elif 500 < x < 700: return (700 - x) / 200.0
    else: return 0.0

def macet(x):
    if 500 < x < 700: return (x - 500) / 200.0
    elif x >= 700: return 1.0
    else: return 0.0

# --- 2. ANTARMUKA PENGGUNA (UI) ---
st.title("🚗 Sistem Logika Fuzzy: Tingkat Kemacetan")
st.markdown("---")

# Sidebar untuk Input
with st.sidebar:
    st.header("⚙️ Panel Input")
    st.info("Geser slider di bawah ini untuk memasukkan jumlah kendaraan di jalan.")
    kendaraan = st.slider("Jumlah Kendaraan (0 - 1000)", min_value=0, max_value=1000, value=450, step=10)

# --- 3. PERHITUNGAN DERAJAT KEANGGOTAAN ---
derajat = {
    "Lancar": lancar(kendaraan),
    "Padat": padat(kendaraan),
    "Macet": macet(kendaraan)
}

# --- 4. TAMPILAN HASIL & INTERPRETASI ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📊 Derajat Keanggotaan")
    st.markdown("Hasil perhitungan nilai fuzzy:")
    
    # Menampilkan metrik (dibagi menjadi 3 kolom kecil agar sejajar)
    m1, m2, m3 = st.columns(3)
    m1.metric("Lancar", f"{derajat['Lancar']:.2f}")
    m2.metric("Padat", f"{derajat['Padat']:.2f}")
    m3.metric("Macet", f"{derajat['Macet']:.2f}")

    st.markdown("<br>", unsafe_allow_html=True) # Memberi sedikit jarak spasi

    # --- TAMBAHAN TABEL DERAJAT KEANGGOTAAN ---
    st.markdown("**Tabel Rincian Derajat Keanggotaan:**")
    tabel_data = {
        "Himpunan Fuzzy": ["Lancar", "Padat", "Macet"],
        "Nilai Derajat (μ)": [f"{derajat['Lancar']:.2f}", f"{derajat['Padat']:.2f}", f"{derajat['Macet']:.2f}"]
    }
    st.table(tabel_data)
    # ----------------------------------------

    # Interpretasi Hasil
    st.subheader("💡 Interpretasi Hasil")
    # Mencari nilai derajat keanggotaan tertinggi
    kategori_dominan = max(derajat, key=derajat.get)
    nilai_dominan = derajat[kategori_dominan]
    
    if nilai_dominan > 0:
        st.success(f"Berdasarkan volume **{kendaraan} kendaraan**, kondisi lalu lintas didominasi oleh kategori **{kategori_dominan}** dengan tingkat keyakinan **{nilai_dominan:.2f}**.")
    else:
        st.warning("Nilai tidak terdefinisi dalam himpunan fuzzy.")

# --- 5. VISUALISASI GRAFIK ---
with col2:
    st.subheader("📈 Visualisasi Himpunan Fuzzy")
    
    # Membuat figure matplotlib
    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.linspace(0, 1000, 500)
    
    y_lancar = [lancar(i) for i in x]
    y_padat = [padat(i) for i in x]
    y_macet = [macet(i) for i in x]

    # Plot garis
    ax.plot(x, y_lancar, label='Lancar', color='blue', linewidth=2)
    ax.plot(x, y_padat, label='Padat', color='green', linewidth=2)
    ax.plot(x, y_macet, label='Macet', color='red', linewidth=2)

    # Arsiran di bawah kurva
    ax.fill_between(x, y_lancar, alpha=0.1, color='blue')
    ax.fill_between(x, y_padat, alpha=0.1, color='green')
    ax.fill_between(x, y_macet, alpha=0.1, color='red')

    # Garis penanda input user
    ax.axvline(x=kendaraan, color='black', linestyle='--', linewidth=2, label=f'Input: {kendaraan}')
    ax.scatter(kendaraan, 0, color='black', zorder=5)

    # Konfigurasi sumbu dan label
    ax.set_title("Grafik Fungsi Keanggotaan: Tingkat Kemacetan")
    ax.set_xlabel("Domain Jumlah Kendaraan (0 - 1000)")
    ax.set_ylabel("Derajat Keanggotaan \u03BC(x)")
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 1.1)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='center right')

    # Menampilkan plot di Streamlit
    st.pyplot(fig)