import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.style.use("seaborn-v0_8")  # Estilo general


st.title("Modelo Interactivo de Producción Cobb-Douglas")





opcion = st.sidebar.selectbox(
    "Selecciona el modelo:",
    ["Cobb-Douglas: Q = A · K^a · L^b"]
)

with st.sidebar.expander("Parámetros de Producción"):
    K = st.number_input("Capital (K)", value=10.0, min_value=0.1)
    L = st.number_input("Trabajo (L)", value=5.0, min_value=0.1)

if opcion == "Cobb-Douglas: Q = A · K^a · L^b":
    with st.sidebar.expander("Parámetros Cobb-Douglas"):
        A = st.number_input("Eficiencia total (A)", value=1.0, min_value=0.0)
        a = st.number_input("Elasticidad del Capital (a)", value=0.5, min_value=0.0)
        b = st.number_input("Elasticidad del Trabajo (b)", value=0.5, min_value=0.0)



def produccion_cobb(A, K, L, a, b):
    return A * (K**a) * (L**b)

def pmgL_cobb(A, K, L, a, b):
    return A * b * (K**a) * (L**(b-1))

def pmgK_cobb(A, K, L, a, b):
    return A * a * (K**(a-1)) * (L**b)



if opcion == "Cobb-Douglas: Q = A · K^a · L^b":

    # Producción y productos marginales y medios
    Q = produccion_cobb(A, K, L, a, b)
    PMg_L = pmgL_cobb(A, K, L, a, b)
    PMg_K = pmgK_cobb(A, K, L, a, b)
    PMe_L = Q / L
    PMe_K = Q / K

    st.subheader(" Resultados de la Producción")

    col1, col2, col3 = st.columns(3)
    col1.metric("Producción total (Q)", f"{Q:.4f}")
    col2.metric("PMg del Trabajo (PMg_L)", f"{PMg_L:.4f}")
    col3.metric("PMg del Capital (PMg_K)", f"{PMg_K:.4f}")

    col4, col5 = st.columns(2)
    col4.metric("PMe del Trabajo (PMe_L)", f"{PMe_L:.4f}")
    col5.metric("PMe del Capital (PMe_K)", f"{PMe_K:.4f}")



    st.subheader("Gráficas del Trabajo (L)")

    L_vals = np.linspace(1, L * 3, 100)
    Q_vals = produccion_cobb(A, K, L_vals, a, b)
    PMg_vals = pmgL_cobb(A, K, L_vals, a, b)
    PMe_vals = Q_vals / L_vals

    # Producción Q(L)
    fig1, ax1 = plt.subplots()
    ax1.plot(L_vals, Q_vals)
    ax1.set_title("Producción Q(L)")
    ax1.set_xlabel("Trabajo (L)")
    ax1.set_ylabel("Producción (Q)")
    ax1.grid(True)
    st.pyplot(fig1)

    # Producto Marginal del Trabajo
    fig2, ax2 = plt.subplots()
    ax2.plot(L_vals, PMg_vals, color="orange")
    ax2.set_title("Producto Marginal del Trabajo (PMg_L)")
    ax2.set_xlabel("Trabajo (L)")
    ax2.set_ylabel("PMg_L")
    ax2.grid(True)
    st.pyplot(fig2)

    # Producto Medio del Trabajo
    fig3, ax3 = plt.subplots()
    ax3.plot(L_vals, PMe_vals, color="green")
    ax3.set_title("Producto Medio del Trabajo (PMe_L)")
    ax3.set_xlabel("Trabajo (L)")
    ax3.set_ylabel("PMe_L")
    ax3.grid(True)
    st.pyplot(fig3)



    st.subheader(" Gráficas del Capital (K) ")

    K_vals_plot = np.linspace(1, K * 3, 100)
    Q_K_vals = produccion_cobb(A, K_vals_plot, L, a, b)
    PMg_K_vals = pmgK_cobb(A, K_vals_plot, L, a, b)
    PMe_K_vals = Q_K_vals / K_vals_plot

    # Producción Q(K)
    figK, axK = plt.subplots()
    axK.plot(K_vals_plot, Q_K_vals, color="purple")
    axK.set_title("Producción Q(K)")
    axK.set_xlabel("Capital (K)")
    axK.set_ylabel("Producción (Q)")
    axK.grid(True)
    st.pyplot(figK)

    # PMg(K)
    figPMgK, axPMgK = plt.subplots()
    axPMgK.plot(K_vals_plot, PMg_K_vals, color="red")
    axPMgK.set_title("Producto Marginal del Capital (PMg_K)")
    axPMgK.set_xlabel("Capital (K)")
    axPMgK.set_ylabel("PMg_K")
    axPMgK.grid(True)
    st.pyplot(figPMgK)

    # PMe(K)
    figPMeK, axPMeK = plt.subplots()
    axPMeK.plot(K_vals_plot, PMe_K_vals, color="teal")
    axPMeK.set_title("Producto Medio del Capital (PMe_K)")
    axPMeK.set_xlabel("Capital (K)")
    axPMeK.set_ylabel("PMe_K")
    axPMeK.grid(True)
    st.pyplot(figPMeK)



    st.subheader("Superficie 3D de la Función de Producción")

    K_vals3 = np.linspace(1, K * 3, 40)
    L_vals3 = np.linspace(1, L * 3, 40)
    K_mesh, L_mesh = np.meshgrid(K_vals3, L_vals3)
    Q_mesh = produccion_cobb(A, K_mesh, L_mesh, a, b)

    fig4 = plt.figure(figsize=(8, 6))
    ax4 = fig4.add_subplot(111, projection="3d")
    ax4.plot_surface(K_mesh, L_mesh, Q_mesh, cmap="viridis", edgecolor="none")
    ax4.set_title("Superficie 3D – Función Cobb-Douglas")
    ax4.set_xlabel("K")
    ax4.set_ylabel("L")
    ax4.set_zlabel("Q")

    st.pyplot(fig4)

 

    st.subheader(" Isocuantas de la Función de Producción")

    K_range = np.linspace(1, K * 3, 50)
    L_range = np.linspace(1, L * 3, 50)
    K_grid, L_grid = np.meshgrid(K_range, L_range)

    Q_grid = produccion_cobb(A, K_grid, L_grid, a, b)

    figIQ, axIQ = plt.subplots(figsize=(7, 5))

    niveles_Q = np.linspace(Q * 0.4, Q * 2, 6)

    contours = axIQ.contour(
        K_grid, L_grid, Q_grid,
        levels=niveles_Q,
        cmap="viridis"
    )

    axIQ.clabel(contours, inline=True, fontsize=8)
    axIQ.set_title("Isocuantas Cobb-Douglas")
    axIQ.set_xlabel("Capital (K)")
    axIQ.set_ylabel("Trabajo (L)")
    axIQ.grid(True)

    st.pyplot(figIQ)
