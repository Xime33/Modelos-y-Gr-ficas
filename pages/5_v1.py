import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.title("Modelo de Rendimientos (Cobb-Douglas) con Costos, Precio y Ganancias")

plt.rcParams.update({
    "figure.dpi": 140,
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "axes.linewidth": 1.0,
    "grid.alpha": 0.25,
    "legend.frameon": False,
})

EPS = 1e-9


def calcular_Q(x, L, K, l, k):
    return x * (L ** l) * (K ** k)


def calcular_costos_y_beneficios(Q, L, w, P):
    CT = w * L
    Q_safe = np.maximum(Q, EPS)
    CM = CT / Q_safe
    IT = P * Q
    Ganancia = IT - CT
    return CT, CM, IT, Ganancia


def tipo_rendimientos(l, k, tol=1e-6):
    s = l + k
    if s > 1 + tol:
        return "Rendimientos crecientes (IRS)", s
    if s < 1 - tol:
        return "Rendimientos decrecientes (DRS)", s
    return "Rendimientos constantes (CRS)", s


def find_break_even(L_vals, CM_vals, P):
    y = CM_vals - P
    sgn = np.sign(y)
    idx = np.where(sgn[:-1] * sgn[1:] < 0)[0]
    roots = []
    for i in idx:
        x0, x1 = L_vals[i], L_vals[i + 1]
        y0, y1 = y[i], y[i + 1]
        xr = x0 - y0 * (x1 - x0) / (y1 - y0)
        roots.append(float(xr))
    return roots


with st.sidebar:
    st.header("Parámetros")

    with st.expander("Función de Producción", expanded=True):
        x = st.number_input("Productividad total (x)", value=10.0, min_value=0.0001, step=0.5)
        K = st.number_input("Capital (K)", value=10.0, min_value=0.0001, step=1.0)
        L_max = st.number_input("Rango máximo de trabajo (L)", value=50.0, min_value=2.0, step=5.0)

    with st.expander("Elasticidades", expanded=True):
        l = st.number_input("Elasticidad del trabajo (l)", value=0.5, min_value=0.0, step=0.05)
        k = st.number_input("Elasticidad del capital (k)", value=0.5, min_value=0.0, step=0.05)

    with st.expander("Precios y Costos", expanded=True):
        w = st.number_input("Costo por trabajador (w)", value=100.0, min_value=0.0, step=5.0)
        P = st.number_input("Precio del producto (P)", value=50.0, min_value=0.0, step=1.0)

    show_table = st.checkbox("Mostrar tabla de resultados", value=True)
    show_break_even = st.checkbox("Marcar puntos donde CM = P (break-even)", value=True)


L_vals = np.linspace(1, float(L_max), 300)
Q_vals = calcular_Q(x, L_vals, K, l, k)
CT_vals, CM_vals, IT_vals, G_vals = calcular_costos_y_beneficios(Q_vals, L_vals, w, P)

rend_txt, sum_elast = tipo_rendimientos(l, k)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Tipo de rendimientos (l + k)", rend_txt, f"{sum_elast:.2f}")
c2.metric("Producción en L = 1", f"{Q_vals[0]:.3f}")
c3.metric("Costo medio mínimo", f"{np.min(CM_vals):.3f}")
c4.metric("Ganancia máxima", f"{np.max(G_vals):.3f}")

st.caption(
    "Modelo: Q = x·L^l·K^k. "
    "CT = w·L, CM = CT/Q, IT = P·Q, Ganancia = IT − CT."
)

if show_table:
    data = pd.DataFrame({
        "L": L_vals,
        "Producción (Q)": Q_vals,
        "Costo Total (CT)": CT_vals,
        "Costo Medio (CM)": CM_vals,
        "Ingreso Total (IT)": IT_vals,
        "Ganancia (IT - CT)": G_vals
    })
    st.subheader("Resultados numéricos")
    st.dataframe(data.round(3), use_container_width=True)

roots = find_break_even(L_vals, CM_vals, P) if show_break_even else []

st.subheader("Función de Producción Q(L)")
fig1, ax1 = plt.subplots(figsize=(10, 4), constrained_layout=True)
ax1.plot(L_vals, Q_vals, linewidth=2.8)
ax1.set_xlabel("Trabajo (L)")
ax1.set_ylabel("Producción (Q)")
ax1.grid(True)
st.pyplot(fig1)
plt.close(fig1)

st.subheader("Costo Medio (CM) vs Precio (P)")
fig2, ax2 = plt.subplots(figsize=(10, 4), constrained_layout=True)
ax2.plot(L_vals, CM_vals, linewidth=2.8, label="Costo medio (CM)")
ax2.axhline(y=P, linestyle="--", linewidth=2.0, label="Precio (P)")

if roots:
    for r in roots:
        ax2.axvline(r, linestyle=":", linewidth=1.6)
    ax2.text(
        0.01, 0.02,
        f"Break-even CM=P en L ≈ {', '.join([f'{r:.2f}' for r in roots[:3]])}"
        + (" ..." if len(roots) > 3 else ""),
        transform=ax2.transAxes
    )

ax2.set_xlabel("Trabajo (L)")
ax2.set_ylabel("Costo / Precio")
ax2.legend()
ax2.grid(True)
st.pyplot(fig2)
plt.close(fig2)

st.subheader("Ganancia Total (IT − CT)")
fig3, ax3 = plt.subplots(figsize=(10, 4), constrained_layout=True)
ax3.plot(L_vals, G_vals, linewidth=2.8)
ax3.axhline(y=0, linestyle="--", linewidth=2.0)

imax = int(np.argmax(G_vals))
ax3.scatter([L_vals[imax]], [G_vals[imax]], s=55)
ax3.annotate(
    f"Máx ≈ ({L_vals[imax]:.2f}, {G_vals[imax]:.2f})",
    (L_vals[imax], G_vals[imax]),
    textcoords="offset points",
    xytext=(10, 10)
)

ax3.set_xlabel("Trabajo (L)")
ax3.set_ylabel("Ganancia")
ax3.grid(True)
st.pyplot(fig3)
plt.close(fig3)

st.markdown(f"""
### Interpretación
- La suma de elasticidades es **l + k = {sum_elast:.2f}**, lo que implica **{rend_txt}**.
- La empresa opera de forma rentable cuando **P > CM**.
- La ganancia total es máxima en un nivel intermedio de trabajo, dado el salario y el precio.
""")
