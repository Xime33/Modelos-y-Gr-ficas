import streamlit as st

st.title("Calculadora de Funciones de Producción")

opcion = st.selectbox(
    "Tipo de función de producción:",
    [
        "Lineal: Q = K + L",
        "Cobb-Douglas: Q = A · K^a · L^b"
    ]
)

def produccion_lineal(K, L):
    return K + L

def produccion_cobb_douglas(A, K, L, a, b):
    return A * (K ** a) * (L ** b)

# PRODUCTOS MARGINALES
def pmgL_cobb(A, K, L, a, b):
    return A * b * (K ** a) * (L ** (b - 1))

def pmgK_cobb(A, K, L, a, b):
    return A * a * (K ** (a - 1)) * (L ** b)

# PRODUCTOS MEDIOS
def pmeL(Q, L):
    return Q / L if L != 0 else 0

def pmeK(Q, K):
    return Q / K if K != 0 else 0


if opcion == "Lineal: Q = K + L":
    K = st.number_input("Capital (K)", min_value=0.0, value=10.0)
    L = st.number_input("Trabajo (L)", min_value=0.0, value=5.0)

    if st.button("Calcular Q"):
        Q = produccion_lineal(K, L)

        PMe_L = pmeL(Q, L)
        PMe_K = pmeK(Q, K)

        st.success(f"**Q = {Q}**")
        st.info(f"**Producto medio del trabajo (PMe_L): {PMe_L}**")
        st.info(f"**Producto medio del capital (PMe_K): {PMe_K}**")
        st.warning("⚠ La función lineal no tiene producto marginal útil (PMg = 1 para cada insumo).")


elif opcion == "Cobb-Douglas: Q = A · K^a · L^b":
    A = st.number_input("Constante de eficiencia (A)", min_value=0.0, value=1.0)

    # CAMBIO MÍNIMO: evitar K=0 y L=0 para no romper PMg con exponentes < 1
    K = st.number_input("Capital (K)", min_value=0.0001, value=10.0)
    L = st.number_input("Trabajo (L)", min_value=0.0001, value=5.0)

    a = st.number_input("Elasticidad del capital (a)", min_value=0.0, value=0.5)
    b = st.number_input("Elasticidad del trabajo (b)", min_value=0.0, value=0.5)

    if st.button("Calcular Q"):
        Q = produccion_cobb_douglas(A, K, L, a, b)

        PMg_L = pmgL_cobb(A, K, L, a, b)
        PMg_K = pmgK_cobb(A, K, L, a, b)
        PMe_L = pmeL(Q, L)
        PMe_K = pmeK(Q, K)

        st.success(f"**Q = {Q}**")

        st.info(f"**Producto marginal del trabajo (PMg_L): {PMg_L}**")
        st.info(f"**Producto marginal del capital (PMg_K): {PMg_K}**")

        st.info(f"**Producto medio del trabajo (PMe_L): {PMe_L}**")
        st.info(f"**Producto medio del capital (PMe_K): {PMe_K}**")
