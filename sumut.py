import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =====================
# BACA DATA
# =====================
df = pd.read_excel("SUMUT.xlsx", sheet_name="Sheet1")

# =====================
# PREPROCESSING
# =====================
# Agregasi tahunan
agg = df.groupby("Tahun").agg({
    "Curah_Hujan": "sum",
    "Tx": "mean",
    "Tn": "mean",
    "Tavg": "mean",
    "Selisih_Suhu": "mean"
}).reset_index()
agg = agg.round(2)

# =====================
# DASHBOARD
# =====================
st.set_page_config(page_title="Dashboard Iklim Sumatera Utara", layout="wide")
st.title("🌦️ Dashboard Iklim Provinsi Sumatera Utara")
st.markdown("Analisis tahunan iklim berdasarkan suhu, curah hujan, dan rentang suhu.")

# =====================
# TABEL DATA
# =====================
st.subheader("📄 Data Iklim Tahunan")
st.dataframe(agg)

# =====================
# TREND GRAFIK
# =====================
col1, col2 = st.columns(2)
with col1:
    st.subheader("🌡️ Suhu Rata-rata Tahunan")
    st.line_chart(agg.set_index("Tahun")["Tavg"])

with col2:
    st.subheader("🌧️ Curah Hujan Tahunan")
    st.bar_chart(agg.set_index("Tahun")["Curah_Hujan"])

# =====================
# ANOMALI SUHU
# =====================
st.subheader("📈 Anomali Suhu terhadap Rata-rata")
baseline = agg[(agg["Tahun"] >= 2000) & (agg["Tahun"] <= 2020)]["Tavg"].mean()
agg["Anomali_Suhu"] = agg["Tavg"] - baseline

fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.barplot(x="Tahun", y="Anomali_Suhu", data=agg, palette="coolwarm", ax=ax1)
ax1.axhline(0, color="black", linestyle="--")
ax1.set_ylabel("Anomali (°C)")
plt.xticks(rotation=45)
st.pyplot(fig1)

# =====================
# RENTANG SUHU
# =====================
st.subheader("🌡️ Rentang Suhu Tahunan")
st.line_chart(agg.set_index("Tahun")["Selisih_Suhu"])

# =====================
# KORELASI
# =====================
st.subheader("📊 Korelasi Variabel Iklim")
fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.heatmap(agg.select_dtypes(include='number').corr(), annot=True, cmap="coolwarm", ax=ax2)
st.pyplot(fig2)

# =====================
# DEKADE
# =====================
st.subheader("📆 Rata-rata per Dekade")
agg["Dekade"] = (agg["Tahun"] // 10) * 10
dekade = agg.groupby("Dekade")[["Tavg", "Curah_Hujan"]].mean().round(2)
st.dataframe(dekade)

fig3, ax3 = plt.subplots()
dekade.plot(kind="bar", ax=ax3)
ax3.set_ylabel("Rata-rata")
st.pyplot(fig3)

# =====================
# TAHUN EKSTREM
# =====================
st.subheader("📌 Tahun Ekstrem")
st.markdown(f"""
- 🌡️ **Tahun Terpanas**: {agg.loc[agg['Tavg'].idxmax()]['Tahun']} ({agg['Tavg'].max():.2f} °C)  
- ❄️ **Tahun Terdingin**: {agg.loc[agg['Tavg'].idxmin()]['Tahun']} ({agg['Tavg'].min():.2f} °C)  
- 🌧️ **Hujan Terbanyak**: {agg.loc[agg['Curah_Hujan'].idxmax()]['Tahun']} ({agg['Curah_Hujan'].max():.1f} mm)  
- ☀️ **Hujan Terkering**: {agg.loc[agg['Curah_Hujan'].idxmin()]['Tahun']} ({agg['Curah_Hujan'].min():.1f} mm)
""")
