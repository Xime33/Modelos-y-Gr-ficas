import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.title("Modelo de Rendimientos Crecientes, Decrecientes y Producción Exponencial")

plt.rcParams.update({
    "figure.dpi": 140,
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "grid.alpha": 0.25,
    "legend.frameon": False,
})

EPS = 1e-9


def calcular_Q(x, L, K, l, k):
    return x * (L ** l) * (K ** k)


def calcular_costos(Q, L, w):
    CT = w * L
    CM = np.divide(CT, Q, out=np.zeros_like(CT, dtype=float), where=Q != 0)
    return CT, CM


def calcular_exponencial(x, L, K, beta):
    return x * np.exp(beta * L) * K


with st.sidebar.expander("Parámetros de Producción", expanded=True):
    x = st.number_input("x (Productividad total)", value=10.0, min_value=0.0001, step=0.5)
    L_max = st.number_input("L máximo (Trabajo)", value=10.0, min_value=2.0, step=1.0)
    K = st.number_input("K (Capital)", value=10.0, min_value=0.0001, step=1.0)

with st.sidebar.expander("Elasticidades", expanded=True):
    l_crec = st.number_input("Elasticidad del trabajo (creciente)", value=1.2, min_value=0.0, step=0.05)
    l_decr = st.number_input("Elasticidad del trabajo (decreciente)", value=0.5, min_value=0.0, step=0.05)
    k = st.number_input("Elasticidad del capital (k)", value=0.5, min_value=0.0, step=0.05)
    beta = st.number_input("Parámetro exponencial β", value=0.15, min_value=0.0, step=0.01)

with st.sidebar.expander("Costos e ingresos", expanded=True):
    w = st.number_input("Costo por unidad de trabajo (w)", value=100.0, min_value=0.0, step=5.0)
    precio = st.number_input("Precio del producto (P)", value=50.0, min_value=0.0, step=1.0)


L_vals = np.linspace(1, float(L_max), 200)

Q_decr = calcular_Q(x, L_vals, K, l_decr, k)
Q_crec = calcular_Q(x, L_vals, K, l_crec, k)
Q_exp = calcular_exponencial(x, L_vals, K, beta)

CT_vals, CM_vals = calcular_costos(Q_crec, L_vals, w)
IT_vals = Q_crec * precio
G_vals = IT_vals - CT_vals

PM_L = x * l_crec * (L_vals ** (l_crec - 1)) * (K ** k)
PM_L_safe = np.maximum(PM_L, EPS)
CMg_vals = np.divide(w, PM_L_safe, out=np.zeros_like(PM_L_safe), where=PM_L_safe != 0)

data = pd.DataFrame({
    "Trabajo (L)": L_vals,
    "Q (creciente)": Q_crec,
    "Q (decreciente)": Q_decr,
    "Q (exponencial)": Q_exp,
    "Costo Total (w·L)": CT_vals,
    "Costo Medio (CT/Q)": CM_vals,
    "Ingreso Total (P·Q)": IT_vals,
    "Ganancia (IT - CT)": G_vals,
    "Producto Marginal del Trabajo (PM_L)": PM_L,
    "Costo Marginal (CMg)": CMg_vals,
})

st.subheader("Tabla de Resultados")
st.dataframe(data.round(3), use_container_width=True)


st.subheader("Producción con Rendimientos Decrecientes")
fig1, ax1 = plt.subplots(figsize=(10, 4), constrained_layout=True)
ax1.plot(L_vals, Q_decr, linewidth=2.8, label="Rendimientos decrecientes")
ax1.set_xlabel("Trabajo (L)")
ax1.set_ylabel("Producción (Q)")
ax1.grid(True)
ax1.legend()
st.pyplot(fig1)
plt.close(fig1)


st.subheader("Producción con Rendimientos Crecientes")
fig2, ax2 = plt.subplots(figsize=(10, 4), constrained_layout=True)
ax2.plot(L_vals, Q_crec, linewidth=2.8, label="Rendimientos crecientes")
ax2.set_xlabel("Trabajo (L)")
ax2.set_ylabel("Producción (Q)")
ax2.grid(True)
ax2.legend()
st.pyplot(fig2)
plt.close(fig2)


st.subheader("Costo Medio vs Precio del Producto")
fig3, ax3 = plt.subplots(figsize=(10, 4), constrained_layout=True)
ax3.plot(L_vals, CM_vals, linewidth=2.8, label="Costo medio (CT/Q)")
ax3.axhline(y=precio, linestyle="--", linewidth=2.0, label="Precio (P)")

ax3.fill_between(L_vals, CM_vals, precio, where=CM_vals < precio, alpha=0.15, label="Beneficio (P > CM)")
ax3.fill_between(L_vals, CM_vals, precio, where=CM_vals > precio, alpha=0.15, label="Pérdida (P < CM)")

ax3.set_xlabel("Trabajo (L)")
ax3.set_ylabel("Costo / Precio")
ax3.grid(True)
ax3.legend(loc="upper right")
st.pyplot(fig3)
plt.close(fig3)


st.subheader("Producción Exponencial respecto al Trabajo")
fig4, ax4 = plt.subplots(figsize=(10, 4), constrained_layout=True)
ax4.plot(L_vals, Q_exp, linewidth=2.8, label=f"Exponencial (β = {beta})")
ax4.set_xlabel("Trabajo (L)")
ax4.set_ylabel("Producción (Q)")
ax4.grid(True)
ax4.legend()
st.pyplot(fig4)
plt.close(fig4)


st.subheader("Costo Medio (CM) y Costo Marginal (CMg)")
fig5, ax5 = plt.subplots(figsize=(10, 4), constrained_layout=True)
ax5.plot(L_vals, CM_vals, linewidth=2.8, label="Costo medio (CM)")
ax5.plot(L_vals, CMg_vals, linestyle="--", linewidth=2.3, label="Costo marginal (CMg = w / PM_L)")
ax5.set_xlabel("Trabajo (L)")
ax5.set_ylabel("Costo")
ax5.grid(True)
ax5.legend(loc="upper right")
st.pyplot(fig5)
plt.close(fig5)


st.markdown("""
### Interpretación Económica
1. **Rendimientos decrecientes:** si el exponente del trabajo es menor que 1, el producto marginal tiende a disminuir conforme aumenta L.
2. **Rendimientos crecientes:** si el exponente del trabajo es mayor que 1, la producción aumenta de forma acelerada con L.
3. **Costo medio vs precio:** si **P > CM**, hay rentabilidad a nivel promedio; si **P < CM**, hay pérdidas a nivel promedio.
4. **Producción exponencial:** un aumento pequeño en L puede producir incrementos multiplicativos en Q cuando β > 0.
""")
