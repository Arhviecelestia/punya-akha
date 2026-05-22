import os
import pandas as pd
import streamlit as st
import urllib.parse

# ==========================================
# 1. KONFIGURASI HALAMAN & VISUAL PREMIUM VIBES
# ==========================================
st.set_page_config(
    page_title="The Vault | Premium Sneakers", layout="wide", initial_sidebar_state="collapsed"
)

# Kustomisasi CSS Tingkat Lanjut untuk Estetika Butik Mewah & Ketinggian Seragam
st.markdown(
    """
    <style>
    /* Background Angled Gradient: Kiri Atas Putih, Kanan Bawah Abu-Abu */
    .stApp {
        background: linear-gradient(135deg, #FFFFFF 30%, #ECECEC 70%, #C8C8CC 100%);
    }
    
    /* Header Typo ala Luxury Brand */
    .luxury-header {
        font-family: 'Playfair Display', 'Didot', 'Georgia', serif;
        font-size: 3.2rem;
        font-weight: 300;
        letter-spacing: 6px;
        color: #111111;
        text-align: center;
        margin-bottom: 0px;
        padding-top: 20px;
    }
    
    .luxury-subtitle {
        font-family: 'Montserrat', 'Helvetica Neue', sans-serif;
        font-size: 0.95rem;
        font-weight: 400;
        letter-spacing: 4px;
        color: #666666;
        text-align: center;
        text-transform: uppercase;
        margin-top: 5px;
        margin-bottom: 30px;
    }
    
    /* Memaksa elemen kolom Streamlit agar kontennya berada di tengah (Center-Aligned) */
    [data-testid="stColumn"] {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    
    /* Efek Kartu Minimalis: Tinggi Dikunci Seragam */
    .premium-card {
        background-color: rgba(255, 255, 255, 0.85);
        border: 1px solid rgba(0, 0, 0, 0.08);
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03);
        
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        
        /* Mengunci tinggi kotak agar semua katalog seragam sempurna */
        height: 380px; 
        justify-content: space-between;
        width: 100%;
        margin-top: 15px;
    }
    
    /* Tombol Blackout Sleek Centered */
    .stButton>button {
        width: 90% !important;
        margin: 15px auto 0 auto !important;
        display: block !important;
        border-radius: 4px !important;
        background-color: #000000 !important;
        color: #FFFFFF !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        letter-spacing: 2px !important;
        border: 1px solid #000000 !important;
        padding: 12px 0px !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border-color: #000000 !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# 2. PENGATURAN MULTI-BAHASA & DICTIONARY
# ==========================================
col_blank, col_lang = st.columns([6, 1])
with col_lang:
    bahasa = st.selectbox("🌐 Language", ["Indonesia", "English"], index=0)

txt = {
    "Indonesia": {
        "sub_title": "Kurasi Siluet Legendaris & Autentisitas Mutlak",
        "search_holder": "Cari koleksi siluet eksklusif Anda di sini...",
        "order_btn": "REQUEST ACQUISITION",
        "pop_title": "📦 Private Order Manifest",
        "harga_satuan": "Nilai Investasi:",
        "biodata": "📝 Lembar Identitas Klien",
        "nama_label": "Nama Lengkap",
        "nama_placeholder": "Nama sesuai identitas resmi",
        "size_label": "Pilih Ukuran Sepatu (EU)",
        "aks_label": "Komplemen Tambahan",
        "trans_label": "Metode Konsinyasi",
        "alamat_label": "Destinasi Pengiriman",
        "alamat_placeholder": "Alamat domisili lengkap pengiriman boks",
        "qty_label": "Alokasi Kuantitas:",
        "total_label": "✨ Total Valuasi Transaksi:",
        "submit_btn": "AMANKAN UNIT SEKARANG",
        "err_input": "⚠️ Bidang Nama dan Destinasi wajib diisi untuk proses alokasi.",
        "success_msg": "Alokasi harga berhasil dikalkulasi secara presisi.",
        "wa_btn": "💬 Teruskan Manifest ke Konsultan WhatsApp",
        "foto_missing": "📸 [File gambar '{}' tidak ditemukan]",
        "file_missing": "Sistem Database 'data_sepatu.csv' gagal dijangkau.",
        "aks_options": [
            "Tanpa Tambahan",
            "Kaus Kaki Katun Premium (+Rp 150.000)",
            "Premium Shoe Care Kit (+Rp 250.000)",
            "Etalase Transparan Akrilik (+Rp 350.000)"
        ]
    },
    "English": {
        "sub_title": "Curated Legendary Silhouettes & Absolute Authenticity",
        "search_holder": "Search your exclusive silhouette here...",
        "order_btn": "REQUEST ACQUISITION",
        "pop_title": "📦 Private Order Manifest",
        "harga_satuan": "Investment Value:",
        "biodata": "📝 Client Identity Manifest",
        "nama_label": "Full Name",
        "nama_placeholder": "Legal name for verification",
        "size_label": "Select Shoe Size (EU)",
        "aks_label": "Complimentary Add-ons",
        "trans_label": "Consignment Method",
        "alamat_label": "Shipping Destination",
        "alamat_placeholder": "Complete residential address for vault delivery",
        "qty_label": "Quantity Allocation:",
        "total_label": "✨ Total Transaction Valuation:",
        "submit_btn": "SECURE ALLOCATION NOW",
        "err_input": "⚠️ Name and Destination fields are mandatory for unit reservation.",
        "success_msg": "Allocation price successfully verified.",
        "wa_btn": "💬 Route Manifest to WhatsApp Consultant",
        "foto_missing": "📸 [Image file '{}' is missing]",
        "file_missing": "Database system 'data_sepatu.csv' could not be reached.",
        "aks_options": [
            "No Add-ons",
            "Premium Cotton Socks (+Rp 150,000)",
            "Premium Shoe Care Kit (+Rp 250,000)",
            "Acrylic Exhibition Vault (+Rp 350,000)"
        ]
    }
}

t = txt[bahasa]
FILE_DATA = "data_sepatu.csv"

# ==========================================
# 3. FUNGSI POP-UP CHECKOUT (ANIMATED DIALOG)
# ==========================================
@st.dialog(t["pop_title"])
def order_dialog(item):
    st.markdown(f"<h3 style='text-align:center;'>{item['nama']}</h3>", unsafe_allow_html=True)
    st.divider()

    col_visual, col_form = st.columns([1, 1.2])

    with col_visual:
        if os.path.exists(str(item["foto"])):
            st.image(item["foto"], use_container_width=True)
        else:
            st.info(t["foto_missing"].format(item['foto']))

        st.markdown(f"<p style='text-align:center; color:#666; margin-bottom:0px;'>{t['harga_satuan']}</p>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center; color:#111; margin-top:0px;'><b>Rp {item['harga']:,}</b></h2>", unsafe_allow_html=True)

    with col_form:
        st.markdown(f"##### {t['biodata']}")
        nama = st.text_input(t["nama_label"], placeholder=t["nama_placeholder"])
        size = st.selectbox(t["size_label"], ["39", "40", "41", "42", "43", "44", "45"], index=2)

        aks_mapping = {
            t["aks_options"][0]: 0,
            t["aks_options"][1]: 150000,
            t["aks_options"][2]: 250000,
            t["aks_options"][3]: 350000,
        }
        aksesoris_terpilih = st.multiselect(t["aks_label"], t["aks_options"])

        transaksi = st.radio(t["trans_label"], ["Bank Vault Transfer", "Digital Wallet", "Amex / Credit Card"], horizontal=True)
        alamat = st.text_area(t["alamat_label"], placeholder=t["alamat_placeholder"])

    st.divider()

    # REAL-TIME CALCULATOR QUANTITY BUTTONS (+ / -)
    bottom_col1, bottom_col2 = st.columns([1.5, 1])

    with bottom_col2:
        st.write(t["qty_label"])
        jumlah_pasang = st.number_input(
            "Qty", min_value=1, max_value=10, value=1, step=1, label_visibility="collapsed"
        )

    total_aksesoris = sum([aks_mapping[aks] for aks in aksesoris_terpilih])
    total_bayar = (item["harga"] * jumlah_pasang) + total_aksesoris

    with bottom_col1:
        st.write(t["total_label"])
        st.markdown(f"## **Rp {total_bayar:,}**")

    if st.button(t["submit_btn"], type="primary"):
        if not nama or not alamat:
            st.error(t["err_input"])
        else:
            bahasa_nota = "ID" if bahasa == "Indonesia" else "EN"
            pesan_wa = (
                f"THE VAULT - RESERVATION MANIFEST ({bahasa_nota}):\n\n"
                f"- *Item Selection:* {item['nama']}\n"
                f"- *Size Assigned:* EU {size}\n"
                f"- *Quantity Allocated:* {jumlah_pasang} pair(s)\n"
                f"- *Complements:* {', '.join(aksesoris_terpilih) if aksesoris_terpilih else '-'}\n"
                f"- *Final Valuation:* Rp {total_bayar:,}\n\n"
                f"*Client Dossier:*\n"
                f"- *Full Name:* {nama}\n"
                f"- *Settlement:* {transaksi}\n"
                f"- *Destination:* {alamat}"
            )

            pesan_encoded = urllib.parse.quote(pesan_wa)
            nomor_admin = "6281234567890"  
            link_final = f"https://wa.me/{nomor_admin}?text={pesan_encoded}"

            st.success(f"✨ {t['success_msg']}")
            st.balloons()
            st.link_button(t["wa_btn"], link_final, use_container_width=True)


# ==========================================
# 4. HALAMAN UTAMA KATALOG (MAIN PAGE)
# ==========================================
st.markdown(f'<div class="luxury-header">THE VAULT</div>', unsafe_allow_html=True)
st.markdown(f'<div class="luxury-subtitle">{t["sub_title"]}</div>', unsafe_allow_html=True)

# LUXURY MINIMALIST SEARCH BAR
col_search_space, col_search_box, col_search_space2 = st.columns([1, 2, 1])
with col_search_box:
    search_query = st.text_input("Search Collection", placeholder=t["search_holder"], label_visibility="collapsed")

st.write("")
st.divider()

try:
    if os.path.exists(FILE_DATA):
        df = pd.read_csv(FILE_DATA)
        
        # Logika Filter Berdasarkan Kolom Search
        if search_query:
            df = df[df['nama'].str.contains(search_query, case=False) | 
                    df['brand'].str.contains(search_query, case=False)]
            
        df_brands = df["brand"].unique()

        for brand in df_brands:
            st.markdown(f"<h3 style='text-align: center; letter-spacing: 4px; color:#222; margin-bottom: 25px;'>— {brand.upper()} EDITION —</h3>", unsafe_allow_html=True)
            
            data_per_brand = df[df["brand"] == brand].reset_index(drop=True)
            cols = st.columns(3)

            for idx, row in data_per_brand.iterrows():
                with cols[idx % 3]:
                    
                    # 1. Gambar dirender menggunakan st.image (Fungsi Asli Streamlit agar PASTI MUNCUL)
                    if os.path.exists(str(row["foto"])):
                        st.image(row["foto"], use_container_width=True)
                    else:
                        st.warning(t["foto_missing"].format(row['foto']))
                    
                    # 2. Teks nama, harga, dan deskripsi dibungkus HTML dengan tinggi dikunci (380px) agar seragam
                    desc = row["deskripsi_id"] if bahasa == "Indonesia" else row["deskripsi_en"]
                    st.markdown(
                        f"""
                        <div class="premium-card">
                            <div style="width: 100%;">
                                <h4 style="margin: 0 0 10px 0; font-weight:400; font-size:1.25rem; color:#111;">{row['nama']}</h4>
                                <h3 style="color:#111; margin: 5px 0 15px 0;"><b>Rp {row['harga']:,}</b></h3>
                                <p style="color:#666; font-size:0.9rem; line-height:1.5; padding:0 5px;">{desc}</p>
                            </div>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    
                    # 3. Tombol Order diletakkan paling bawah
                    if st.button(t["order_btn"], key=f"btn_{brand}_{idx}"):
                        order_dialog(row)

            st.write("")
            st.write("")
            st.divider()
            
        if df.empty:
            st.markdown("<p style='text-align:center; color:#888;'>No exclusive silhouettes matched your search criteria.</p>", unsafe_allow_html=True)
    else:
        st.error(t["file_missing"])

except Exception as e:
    st.error(f"System Matrix Error: {e}")

st.write("")
st.markdown("<p style='text-align:center; color:#999; font-size:0.8rem; letter-spacing:2px;'>© 2026 THE VAULT ATELIER — SLEEK & CENTRIC ARCHITECTURE</p>", unsafe_allow_html=True)
