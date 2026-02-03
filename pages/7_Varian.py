import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def estilo_varian():
    plt.rcParams['axes.edgecolor'] = 'black'
    plt.rcParams['axes.linewidth'] = 1.2
    plt.rcParams['font.size'] = 14
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['figure.figsize'] = (6, 4)
    plt.rcParams['axes.grid'] = False

st.title("Gráficas Capítulos 16–19 (Varian)")

EPS = 1e-6  # solo para evitar 0 en potencias / divisiones y que no truene

# 1) FUNCIÓN DE PRODUCCIÓN
st.header("1. Función de Producción")
estilo_varian()

with st.sidebar.expander("Parámetros Gráfica 1", expanded=True):
    A = st.number_input("A (Productividad total)", value=10.0)
    b = st.number_input("b (Elasticidad)", value=0.6)
    Lmax = st.slider("Máximo de L", 10, 50, 20)

L = np.linspace(EPS, Lmax, 200)
Y = A * (L ** b)

fig1, ax1 = plt.subplots()
ax1.plot(L, Y, color="black")
ax1.set_xlabel("Trabajo (L)")
ax1.set_ylabel("Producto (Y)")
ax1.spines["right"].set_visible(False)
ax1.spines["top"].set_visible(False)

ymin, ymax = np.nanmin(Y), np.nanmax(Y)
if np.isfinite(ymin) and np.isfinite(ymax) and ymin != ymax:
    ax1.set_ylim(ymin - 0.05 * (ymax - ymin), ymax + 0.08 * (ymax - ymin))

st.pyplot(fig1)
plt.close(fig1)

# 2) DEMANDA DE TRABAJO – VPM (Gráfica 6)
st.header("2. Demanda de trabajo – Gráfica 6")
estilo_varian()

with st.sidebar.expander("Parámetros Gráfica 2", expanded=True):
    m = st.number_input("Pendiente (negativa)", value=-0.6, step=0.1)
    b1 = st.number_input("Intercepto VPM1", value=18.0)
    b2 = st.number_input("Intercepto VPM2", value=16.0)
    W1 = st.number_input("Salario W1", value=12.0)
    W2 = st.number_input("Salario W2", value=8.0)
    Lmax2 = st.slider("Máximo del eje de empleo", 10, 50, 25)

L2 = np.linspace(0, Lmax2, 200)
VPM1 = m * L2 + b1
VPM2 = m * L2 + b2

den = (-m) if abs(m) > EPS else (-EPS)  # evita división entre 0
E1 = (b1 - W1) / den
E2 = (b2 - W2) / den

# Recortar al rango para que siempre se vean
E1_plot = float(np.clip(E1, 0, Lmax2))
E2_plot = float(np.clip(E2, 0, Lmax2))

fig2, ax2 = plt.subplots()
ax2.plot(L2, VPM1, linewidth=1.4, color="black")
ax2.plot(L2, VPM2, linewidth=1.4, color="black")

ax2.axhline(W1, color="black")
ax2.axhline(W2, color="black")
ax2.vlines(E1_plot, 0, W1, color="black")
ax2.vlines(E2_plot, 0, W2, color="black")

# Textos: colocarlos relativo al eje para que no se pierdan
ax2.text(0.02, W1, "W1", va="bottom", ha="left")
ax2.text(0.02, W2, "W2", va="bottom", ha="left")
ax2.text(E1_plot, ax2.get_ylim()[0], "E1", ha="center", va="bottom")
ax2.text(E2_plot, ax2.get_ylim()[0], "E2", ha="center", va="bottom")

ax2.set_xlabel("Empleo")
ax2.set_ylabel("Salario")
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

# Límites y para que se vea todo
ys = np.array([VPM1.min(), VPM1.max(), VPM2.min(), VPM2.max(), W1, W2], dtype=float)
ys = ys[np.isfinite(ys)]
if len(ys) > 0:
    y0, y1 = ys.min(), ys.max()
    if y0 == y1:
        y0 -= 1
        y1 += 1
    pad = 0.08 * (y1 - y0)
    ax2.set_ylim(y0 - pad, y1 + pad)

st.pyplot(fig2)
plt.close(fig2)

# 3) CFM
st.header("3. Gráfica 7 – Costo Fijo Medio")
estilo_varian()

with st.sidebar.expander("Parámetros Gráfica 3", expanded=True):
    CF = st.number_input("Costo Fijo (CF)", value=200.0)
    ymax3 = st.slider("Máximo de y", 20, 200, 50)

y3 = np.linspace(1, ymax3, 200)
CFM = CF / y3

fig3, ax3 = plt.subplots()
ax3.plot(y3, CFM, color="black")
ax3.text(y3[-1], CFM[-1], "CFM", ha="left", va="center")
ax3.set_xlabel("y")
ax3.set_ylabel("CFM")
ax3.spines["top"].set_visible(False)
ax3.spines["right"].set_visible(False)

st.pyplot(fig3)
plt.close(fig3)

# 4) CVM – Máxima capacidad
st.header("4. Gráfica 8 – CVM con Máxima Capacidad")
estilo_varian()

with st.sidebar.expander("Parámetros Gráfica 4", expanded=True):
    costo_base = st.number_input("Costo base", value=20.0)
    capacidad = st.slider("Máxima Capacidad", 10, 80, 40)
    potencia = st.slider("Exponente", 1, 3, 2)

y4 = np.linspace(1, 60, 300)
CVM = np.piecewise(
    y4,
    [y4 < capacidad, y4 >= capacidad],
    [
        lambda y: costo_base * np.ones_like(y),
        lambda y: costo_base + 0.5 * (y - capacidad) ** potencia
    ]
)

fig4, ax4 = plt.subplots()
ax4.plot(y4, CVM, color="black")
ax4.axvline(capacidad, color="black")
ax4.text(capacidad + 1, costo_base, "Máxima\ncapacidad", ha="left", va="top")
ax4.set_xlabel("y")
ax4.set_ylabel("CVM")
ax4.spines["top"].set_visible(False)
ax4.spines["right"].set_visible(False)

# y-limits robustos
ymin, ymax = np.nanmin(CVM), np.nanmax(CVM)
if np.isfinite(ymin) and np.isfinite(ymax) and ymin != ymax:
    ax4.set_ylim(ymin - 0.08 * (ymax - ymin), ymax + 0.10 * (ymax - ymin))

st.pyplot(fig4)
plt.close(fig4)

# 5) CVMe (U)
st.header("5. Gráfica 9 – CVMe")
estilo_varian()

with st.sidebar.expander("Parámetros Gráfica 5", expanded=True):
    a = st.number_input("Constante base", value=8.0)
    c = st.number_input("Pendiente cuadrática", value=0.015)

y5 = np.linspace(1, 60, 300)
CVMe = a + c * (y5 - 20) ** 2

fig5, ax5 = plt.subplots()
ax5.plot(y5, CVMe, color="black")
ax5.text(y5[-1], CVMe[-1], "CVMe", ha="left", va="center")
ax5.set_xlabel("y")
ax5.set_ylabel("CMe")
ax5.spines["top"].set_visible(False)
ax5.spines["right"].set_visible(False)

st.pyplot(fig5)
plt.close(fig5)

# 6) CMe – U pronunciada
st.header("6. Gráfica 10 – CMe (Curva en U)")
estilo_varian()

with st.sidebar.expander("Parámetros Gráfica 6", expanded=True):
    c0 = st.number_input("Nivel base", value=10.0)
    c2 = st.number_input("Coeficiente cuadrático", value=0.02)

y6 = np.linspace(1, 60, 300)
CMe = c0 + c2 * (y6 - 30) ** 2

fig6, ax6 = plt.subplots()
ax6.plot(y6, CMe, color="black")
ax6.text(y6[-1], CMe[-1], "CMe", ha="left", va="center")
ax6.set_xlabel("y")
ax6.set_ylabel("CMe")
ax6.spines["top"].set_visible(False)
ax6.spines["right"].set_visible(False)

st.pyplot(fig6)
plt.close(fig6)

# 7) CM + CVMe (Gráfica 11)
st.header("7. Gráfica 11 – CM y CVMe")
estilo_varian()

with st.sidebar.expander("Parámetros Gráfica 7", expanded=True):
    cCM = st.number_input("CM — parámetro cuadrático", value=0.015)
    cCV = st.number_input("CVMe — parámetro cuadrático", value=0.008)
    shift_CM = st.number_input("Desplazamiento CM", value=28.0)
    shift_CV = st.number_input("Desplazamiento CVMe", value=38.0)

y7 = np.linspace(1, 60, 300)
CM = cCM * (y7 - shift_CM) ** 2 + 8
CVMe2 = cCV * (y7 - shift_CV) ** 2 + 9

fig7, ax7 = plt.subplots()
ax7.plot(y7, CM, color="black")
ax7.plot(y7, CVMe2, color="black")

# Etiquetas colocadas dentro del rango de forma robusta
i_cm = int(np.argmin(CM))
i_cv = int(np.argmin(CVMe2))
ax7.text(y7[i_cm], CM[i_cm], "CM", ha="left", va="bottom")
ax7.text(y7[i_cv], CVMe2[i_cv], "CVMe", ha="left", va="bottom")

ax7.set_xlabel("y")
ax7.set_ylabel("Costos")
ax7.spines["top"].set_visible(False)
ax7.spines["right"].set_visible(False)

ys = np.array([CM.min(), CM.max(), CVMe2.min(), CVMe2.max()], dtype=float)
y0, y1 = ys.min(), ys.max()
pad = 0.08 * (y1 - y0) if y1 != y0 else 1
ax7.set_ylim(y0 - pad, y1 + pad)

st.pyplot(fig7)
plt.close(fig7)

