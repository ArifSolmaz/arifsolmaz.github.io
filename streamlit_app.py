import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("1972 Meteor Olayı: Enerji Hesaplayıcı")

st.markdown("""
Bu uygulama, 10 Ağustos 1972'de atmosferde sıçrayan meteorun düşmesi durumunda ortaya çıkacak enerjiyi hesaplar.
Kullanıcı girdilerine göre sonuçları yeniden hesaplayabilir.
""")

# Varsayılan değerler
mass = st.number_input("Meteorun kütlesi (kg)", value=4e6, step=1e5, format="%.1e")
velocity = st.number_input("Hızı (km/s)", value=15.0, step=1.0) * 1e3  # m/s'ye çevir
tnt_megaton_energy = 4.2e15
hiroshima_kiloton = 13

# (a) Kinetik enerji hesabı
kinetic_energy = 0.5 * mass * velocity**2
st.subheader("a) Kinetik Enerji")
st.write(f"Kinetik Enerji: {kinetic_energy:.2e} J")

# (b) TNT karşılığı
megaton_tnt_equivalent = kinetic_energy / tnt_megaton_energy
st.subheader("b) TNT Karşılığı")
st.write(f"TNT karşılığı: {megaton_tnt_equivalent:.2f} megaton")

# (c) Hiroşima karşılığı
hiroshima_equivalent = megaton_tnt_equivalent * 1000 / hiroshima_kiloton
st.subheader("c) Hiroşima Bombası Karşılığı")
st.write(f"Hiroşima eşdeğeri: {hiroshima_equivalent:.2f} bomba")

# 🔢 Grafik: Hız ve Enerji ilişkisi
st.subheader("Kinetik Enerji vs. Hız Grafiği")
velocities = np.linspace(1e3, 30e3, 100)  # 1 km/s - 30 km/s
energies = 0.5 * mass * velocities**2
plt.figure()
plt.plot(velocities / 1e3, energies / 1e15)  # km/s vs PJ
plt.xlabel("Hız (km/s)")
plt.ylabel("Kinetik Enerji (PetaJoule)")
plt.title("Meteorun Hızına Göre Kinetik Enerji")
st.pyplot(plt)
