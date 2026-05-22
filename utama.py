import os
import pandas as pd
import streamlit as st
import urllib.parse

# ==========================================
# 1. KONFIGURASI HALAMAN & BACKGROUND MEWAH
# ==========================================
st.set_page_config(
    page_title="Premium Sneaker Vault", layout="wide", initial_sidebar_state="collapsed"
)

# Kustomisasi CSS untuk background gradasi putih-abu-abu dan style kartu
st.markdown(
    """
    <style>
    /* Background Utama Gradasi */
    .stApp {
        background: linear-gradient(180deg, #FFFFFF 0%, #F5F5F7 50%, #E2E2E5 100%);
    }
    
    /* Mempercantik tombol bawaan Streamlit */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #111111;
        color: white;
        font-weight: bold;
        transition: all 0.3s ease;
        border: 1px solid #111111;
    }
    .stButton>button:hover {
        background-color: #FFFFFF;
        color: #111111;
        border-color: #111111;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# 2. PENGATURAN MULTI-BAHASA (DICTIONARY)
# ==========================================
# Pilihan bahasa di pojok kanan atas halaman
col_header, col_lang = st.columns([6, 1])
with col_lang:
    bahasa = st.selectbox("🌐 Language", ["Indonesia", "English"], index=0)

# Kamus teks terjemahan
txt = {
    "Indonesia": {
        "sub_title": "Koleksi Mewah & Keaslian Terjamin",
        "order_btn": "PESAN SEKARANG",
        "pop_title": "📦 Formulir Pemesanan Eksklusif",
        "harga_satuan": "Harga Satuan:",
        "biodata": "📝 Biodata Pembeli",
        "nama_label": "Nama Lengkap",
        "nama_placeholder": "Masukkan nama Anda",
        "size_label": "Pilih Ukuran Sepatu (EU)",
        "aks_label": "Aksesoris Tambahan",
        "trans_label": "Metode Transaksi",
        "alamat_label": "Alamat Pengiriman Lengkap",
        "alamat_placeholder": "Nama jalan, Nomor rumah, RT/RW, Kecamatan, Kota",
        "qty_label": "Jumlah Pasang Sepatu:",
        "total_label": "✨ Total Pembayaran Anda:",
        "submit_btn": "KONFIRMASI PESANAN SEKARANG",
        "err_input": "⚠️ Mohon lengkapi Nama dan Alamat Pengiriman Anda terlebih dahulu!",
        "success_msg": "Pesanan Anda berhasil dihitung!",
        "wa_btn": "💬 Kirim Rincian Nota via WhatsApp",
        "foto_missing": "📸 [Tempatkan file gambar '{}' di folder aplikasi]",
        "file_missing": "Gagal memuat! File 'data_sepatu.csv' tidak ditemukan.",
        "aks_options": [
            "Tanpa Aksesoris",
            "Kaus Kaki Premium (+Rp 150.000)",
            "Premium Shoe Cleaner Kit (+Rp 250.000)",
            "Boks Transparan Akrilik (+Rp 350.000)"
        ]
    },
    "English": {
        "sub_title": "Luxury Collection & Guaranteed Authenticity",
        "order_btn": "ORDER NOW",
        "pop_title": "📦 Exclusive Order Form",
        "harga_satuan": "Unit Price:",
        "biodata": "📝 Buyer Information",
        "nama_label": "Full Name",
        "nama_placeholder": "Enter your full name",
        "size_label": "Select Shoe Size (EU)",
        "aks_label": "Additional Accessories",
        "trans_label": "Transaction Method",
        "alamat_label": "Full Delivery Address",
        "alamat_placeholder": "Street name, House number, District, City, Zip Code",
        "qty_label": "Pairs of Shoes Quantity:",
        "total_label": "✨ Your Total Payment:",
        "submit_btn": "CONFIRM ORDER NOW",
        "err_input": "⚠️ Please complete your Name and Shipping Address first!",
        "success_msg": "Your order has been successfully calculated!",
        "wa_btn": "💬 Send Order Details via WhatsApp",
        "foto_missing": "📸 [Place the image file '{}' in the app folder]",
        "file_missing": "Failed to load! File 'data_sepatu.csv' not found.",
        "aks_options": [
            "No Accessories",
            "Premium Socks (+Rp 150,000)",
            "Premium Shoe Cleaner Kit (+Rp 250,000)",
            "Acrylic Transparent Box (+Rp 350,000)"
        ]
    }
}

# Menyimpan preferensi bahasa yang dipilih pengguna ke variabel lokal
t = txt[bahasa]

# ==========================================
# 3. AUTO-GENERATE DATASET (CSV)
# ==========================================
FILE_DATA = "data_sepatu.csv"

if not os.path.exists(FILE_DATA):
    data_awal = {
        "brand": ["Nike", "Nike", "Adidas"],
        "nama": [
            'Nike SB Dunk Low x Travis Scott "Cactus Jack"',
            "Nike Air Jordan 1 x Dior",
            'Adidas Samba "Black"',
        ],
        "harga": [35000000, 150000000, 2200000],
        "deskripsi_id": [
            "Dibuat dengan material suede premium, panel kanvas bermotif paisley yang bisa dikelupas, serta aksen flannel tartan yang ikonik.",
            "Diproduksi langsung di Italia menggunakan kulit lembu asli (Calfskin) tertinggi dengan motif monogram Oblique khas Dior pada logo Swoosh.",
            "Siluet klasik legendaris berbahan full-grain leather hitam dengan suede T-toe overlay, serta sol karet (gum sole) yang sangat nyaman.",
        ],
        "deskripsi_en": [
            "Crafted with premium suede materials, tear-away paisley canvas panels, and iconic flannel tartan accents signature to Travis Scott.",
            "Manufactured directly in Italy using the highest quality calfskin leather with Dior's signature Oblique monogram on the Swoosh.",
            "The legendary classic silhouette featuring black full-grain leather, suede T-toe overlay, and a comfortable gum sole.",
        ],
        "foto": ["travis.jpg", "dior.jpg", "samba.jpg"],
    }
    df_buat = pd.DataFrame(data_awal)
    df_buat.to_csv(FILE_DATA, index=False)


# ==========================================
# 4. FUNGSI POP-UP CHECKOUT (ANIMATED DIALOG)
# ==========================================
@st.dialog(t["pop_title"])
def order_dialog(item):
    st.markdown(f"### {item['nama']}")
    st.divider()

    col_visual, col_form = st.columns([1, 1.2])

    with col_visual:
        if os.path.exists(str(item["foto"])):
            st.image(item["foto"], use_container_width=True)
        else:
            st.info(t["foto_missing"].format(item['foto']))

        st.markdown(t["harga_satuan"])
        st.markdown(f"## **Rp {item['harga']:,}**")

    with col_form:
        st.markdown(f"##### {t['biodata']}")
        nama = st.text_input(t["nama_label"], placeholder=t["nama_placeholder"])
        size = st.selectbox(
            t["size_label"],
            ["39", "40", "41", "42", "43", "44", "45"],
            index=2,
        )

        # Map opsi aksesoris ke nilai harga matematika
        aks_mapping = {
            t["aks_options"][0]: 0,
            t["aks_options"][1]: 150000,
            t["aks_options"][2]: 250000,
            t["aks_options"][3]: 350000,
        }
        aksesoris_terpilih = st.multiselect(t["aks_label"], t["aks_options"])

        transaksi = st.radio(
            t["trans_label"],
            ["Bank Transfer", "E-Wallet", "Credit Card"],
            horizontal=True,
        )
        alamat = st.text_area(t["alamat_label"], placeholder=t["alamat_placeholder"])

    st.divider()

    # ==========================================
    # KANAN: TOMBOL + / -  &  KIRI: TOTAL HARGA
    # ==========================================
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
        st.markdown(f"# **Rp {total_bayar:,}**")

    if st.button(t["submit_btn"], type="primary"):
        if not nama or not alamat:
            st.error(t["err_input"])
        else:
            # Teks WhatsApp otomatis adaptif sesuai bahasa terpilih
            bahasa_nota = "ID" if bahasa == "Indonesia" else "EN"
            pesan_wa = (
                f"New Order Details ({bahasa_nota}):\n\n"
                f"- *Item:* {item['nama']}\n"
                f"- *Size:* {size}\n"
                f"- *Quantity:* {jumlah_pasang} pair(s)\n"
                f"- *Accessories:* {', '.join(aksesoris_terpilih) if aksesoris_terpilih else '-'}\n"
                f"- *Total Payment:* Rp {total_bayar:,}\n\n"
                f"*Customer Info:*\n"
                f"- *Name:* {nama}\n"
                f"- *Payment:* {transaksi}\n"
                f"- *Address:* {alamat}"
            )

            pesan_encoded = urllib.parse.quote(pesan_wa)
            nomor_admin = "6285725744807"  # Taruh nomor WA Anda di sini
            link_final = f"https://wa.me/{nomor_admin}?text={pesan_encoded}"

            st.success(f"✨ {t['success_msg']}")
            st.balloons()

            st.link_button(t["wa_btn"], link_final, use_container_width=True)


# ==========================================
# 5. HALAMAN UTAMA KATALOG (MAIN PAGE)
# ==========================================
with col_header:
    st.markdown(
        "<h1 style='color: #111111; font-family: sans-serif; margin-bottom:0px;'>👟 PREMIUM SNEAKER VAULT</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='color: #666666; font-style: italic; margin-top:0px;'>{t['sub_title']}</p>",
        unsafe_allow_html=True,
    )
st.divider()

try:
    if os.path.exists(FILE_DATA):
        df = pd.read_csv(FILE_DATA)
        daftar_brand = df["brand"].unique()

        for brand in daftar_brand:
            st.markdown(f"## **{brand.upper()} EDITION**")
            data_per_brand = df[df["brand"] == brand].reset_index(drop=True)

            cols = st.columns(3)

            for idx, row in data_per_brand.iterrows():
                with cols[idx % 3]:
                    with st.container(border=True):
                        if os.path.exists(str(row["foto"])):
                            st.image(row["foto"], use_container_width=True)
                        else:
                            st.warning(t["foto_missing"].format(row['foto']))

                        st.subheader(row["nama"])
                        st.markdown(f"### **Rp {row['harga']:,}**")
                        
                        # Menampilkan deskripsi berdasarkan pilihan bahasa
                        if bahasa == "Indonesia":
                            st.write(row["deskripsi_id"])
                        else:
                            st.write(row["deskripsi_en"])
                            
                        st.write("")  # Spacer

                        if st.button(t["order_btn"], key=f"btn_{brand}_{idx}"):
                            order_dialog(row)

            st.write("")
            st.divider()
    else:
        st.error(t["file_missing"])

except Exception as e:
    st.error(f"System Error: {e}")

st.write("")
st.caption("© 2026 Vault Premium Sneaker Store - Sleek & Elegant Dual-Language Design")
st.caption("made by Razkha Raditya Haryadi")