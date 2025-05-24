{\rtf1\ansi\ansicpg1254\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # streamlit_app.py\
import streamlit as st\
import matplotlib.pyplot as plt\
import numpy as np\
\
st.title("1972 Meteor Olay\uc0\u305 : Enerji Hesaplay\u305 c\u305 ")\
\
st.markdown("""\
Bu uygulama, 10 A\uc0\u287 ustos 1972'de atmosferde s\u305 \'e7rayan meteorun d\'fc\u351 mesi durumunda ortaya \'e7\u305 kacak enerjiyi hesaplar.\
Kullan\uc0\u305 c\u305  girdilerine g\'f6re sonu\'e7lar\u305  yeniden hesaplayabilir.\
""")\
\
# Varsay\uc0\u305 lan de\u287 erler\
mass = st.number_input("Meteorun k\'fctlesi (kg)", value=4e6, step=1e5, format="%.1e")\
velocity = st.number_input("H\uc0\u305 z\u305  (km/s)", value=15.0, step=1.0) * 1e3  # m/s'ye \'e7evir\
tnt_megaton_energy = 4.2e15\
hiroshima_kiloton = 13\
\
# (a) Kinetik enerji hesab\uc0\u305 \
kinetic_energy = 0.5 * mass * velocity**2\
st.subheader("a) Kinetik Enerji")\
st.write(f"Kinetik Enerji: \{kinetic_energy:.2e\} J")\
\
# (b) TNT kar\uc0\u351 \u305 l\u305 \u287 \u305 \
megaton_tnt_equivalent = kinetic_energy / tnt_megaton_energy\
st.subheader("b) TNT Kar\uc0\u351 \u305 l\u305 \u287 \u305 ")\
st.write(f"TNT kar\uc0\u351 \u305 l\u305 \u287 \u305 : \{megaton_tnt_equivalent:.2f\} megaton")\
\
# (c) Hiro\uc0\u351 ima kar\u351 \u305 l\u305 \u287 \u305 \
hiroshima_equivalent = megaton_tnt_equivalent * 1000 / hiroshima_kiloton\
st.subheader("c) Hiro\uc0\u351 ima Bombas\u305  Kar\u351 \u305 l\u305 \u287 \u305 ")\
st.write(f"Hiro\uc0\u351 ima e\u351 de\u287 eri: \{hiroshima_equivalent:.2f\} bomba")\
\
# \uc0\u55357 \u56610  Grafik: H\u305 z ve Enerji ili\u351 kisi\
st.subheader("Kinetik Enerji vs. H\uc0\u305 z Grafi\u287 i")\
velocities = np.linspace(1e3, 30e3, 100)  # 1 km/s - 30 km/s\
energies = 0.5 * mass * velocities**2\
plt.figure()\
plt.plot(velocities / 1e3, energies / 1e15)  # km/s vs PJ\
plt.xlabel("H\uc0\u305 z (km/s)")\
plt.ylabel("Kinetik Enerji (PetaJoule)")\
plt.title("Meteorun H\uc0\u305 z\u305 na G\'f6re Kinetik Enerji")\
st.pyplot(plt)\
}