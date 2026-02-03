import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


st.title("Costo Medio de Largo Plazo (CMLP) – Envolvente de técnicas")


with st.sidebar:
    st.header("Parámetros")
    st.caption("Ajusta niveles y pendientes de cada técnica. La CMLP es la envolvente (mínimo) entre CM1, CM2 y CM3.")

    st.subheader("Técnica 1 (CM1)")
    a1 = st.number_input("a₁ (nivel)", value=120.0, min_value=0.0, step=5.0)
    b1 = st.number_input("b₁ (pendiente)", value=9.0, min_value=0.0, step=0.1)
    tp1 = st.number_input("TP1 (posición)", value=30.0, min_value=0.0, step=1.0)
    p1 = st.number_input("P1 (precio)", value=60.0, min_value=0.0, step=1.0)

    st.subheader("Técnica 2 (CM2)")
    a2 = st.number_input("a₂ (nivel)", value=90.0, min_value=0.0, step=5.0)
    b2 = st.number_input("b₂ (pendiente)", value=6.0, min_value=0.0, step=0.1)
    tp2 = st.number_input("TP2 (posición)", value=70.0, min_value=0.0, step=1.0)
    p2 = st.number_input("P2 (precio)", value=40.0, min_value=0.0, step=1.0)

    st.subheader("Técnica 3 (CM3)")
    a3 = st.number_input("a₃ (nivel)", value=70.0, min_value=0.0, step=5.0)
    b3 = st.number_input("b₃ (pendiente)", value=0.8, min_value=0.0, step=0.1)
    tp3 = st.number_input("TP3 (posición)", value=110.0, min_value=0.0, step=1.0)
    p3 = st.number_input("P3 (precio)", value=20.0, min_value=0.0, step=1.0)

    st.divider()
    Qmax = st.number_input("Máximo del eje X (Cantidad)", value=120.0, min_value=2.0, step=5.0)
    npts = st.slider("Resolución (puntos)", min_value=200, max_value=1200, value=500, step=50)

    st.divider()
    show_prices = st.checkbox("Mostrar líneas de precio (P1, P2, P3)", value=True)
    show_tps = st.checkbox("Mostrar líneas verticales TP", value=True)
    show_minima = st.checkbox("Marcar mínimos de cada CM", value=True)
    highlight_envelope = st.checkbox("Resaltar envolvente (CMLP)", value=True)


q = np.linspace(1, Qmax, int(npts))

CM1 = a1 / q + b1
CM2 = a2 / q + b2
CM3 = a3 / q + b3

CMLP = np.minimum.reduce([CM1, CM2, CM3])

# Mínimos "dentro del rango" (en esta forma funcional a/q + b, el mínimo ocurre al máximo q)
# Pero marcamos el mínimo numérico en el rango por robustez.
def argmin_xy(x, y):
    i = int(np.argmin(y))
    return x[i], y[i]

q1m, cm1m = argmin_xy(q, CM1)
q2m, cm2m = argmin_xy(q, CM2)
q3m, cm3m = argmin_xy(q, CM3)

# Límites de y (robustos)
y_min = min(CM1.min(), CM2.min(), CM3.min(), CMLP.min()) * 0.92
y_max = max(CM1.max(), CM2.max(), CM3.max(), CMLP.max()) * 1.08
if not np.isfinite(y_min) or not np.isfinite(y_max) or y_min == y_max:
    y_min, y_max = 0, 1


plt.rcParams.update({
    "figure.dpi": 140,
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "axes.edgecolor": "#2b2b2b",
    "axes.linewidth": 1.0,
    "grid.alpha": 0.25,
    "grid.linestyle": "-",
    "legend.frameon": False
})

fig, ax = plt.subplots(figsize=(11, 6), constrained_layout=True)

# Curvas SRAC (costo medio de corto plazo)
ax.plot(q, CM1, linewidth=2.5, label="CM1 (técnica 1)")
ax.plot(q, CM2, linewidth=2.5, label="CM2 (técnica 2)")
ax.plot(q, CM3, linewidth=2.5, label="CM3 (técnica 3)")

# Envolvente (CMLP)
if highlight_envelope:
    ax.plot(q, CMLP, linewidth=4.0, label="CMLP (envolvente)")
    # Sombreado muy sutil para enfatizar
    ax.fill_between(q, CMLP, y_max, alpha=0.06)

# Líneas verticales TP
if show_tps:
    for tp, lab in [(tp1, "TP1"), (tp2, "TP2"), (tp3, "TP3")]:
        if 0 <= tp <= Qmax:
            ax.axvline(tp, linestyle="--", linewidth=1.4)
            ax.text(tp, y_min + (y_max - y_min) * 0.02, lab, rotation=90,
                    va="bottom", ha="right")

# Líneas horizontales de precio (segmentos)
if show_prices:
    def hseg(p, tp, lab):
        if 0 <= tp <= Qmax:
            x0 = max(0, tp - 10)
            x1 = min(Qmax, tp + 10)
            ax.hlines(p, x0, x1, linewidth=3.0)
            ax.text(tp, p, f" {lab}", va="bottom", ha="left")

    hseg(p1, tp1, "P1")
    hseg(p2, tp2, "P2")
    hseg(p3, tp3, "P3")

# Marcadores de mínimos
if show_minima:
    ax.scatter([q1m, q2m, q3m], [cm1m, cm2m, cm3m], s=55, zorder=5)
    ax.annotate(f"min CM1 ≈ ({q1m:.1f}, {cm1m:.1f})", (q1m, cm1m),
                textcoords="offset points", xytext=(10, 10), ha="left")
    ax.annotate(f"min CM2 ≈ ({q2m:.1f}, {cm2m:.1f})", (q2m, cm2m),
                textcoords="offset points", xytext=(10, -15), ha="left")
    ax.annotate(f"min CM3 ≈ ({q3m:.1f}, {cm3m:.1f})", (q3m, cm3m),
                textcoords="offset points", xytext=(10, 10), ha="left")

# Ejes, título, grid
ax.set_title("Costo Medio de Largo Plazo (CMLP) como envolvente de técnicas")
ax.set_xlabel("Cantidad (q)")
ax.set_ylabel("Costo medio / Precio")

ax.set_xlim(0, Qmax)
ax.set_ylim(y_min, y_max)
ax.grid(True)

# Leyenda
ax.legend(loc="upper right")

# Render
st.pyplot(fig)

# Panel de lectura rápida
with st.expander("Ver resumen numérico"):
    colA, colB, colC, colD = st.columns(4)
    colA.metric("CMLP mínimo (en rango)", f"{CMLP.min():.3f}")
    colB.metric("CMLP en q=Qmax", f"{CMLP[-1]:.3f}")
    colC.metric("q donde CMLP es mínimo", f"{q[np.argmin(CMLP)]:.2f}")
    colD.metric("Qmax", f"{Qmax:.0f}")
