import math

import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Stats Visualizer", layout="wide")
st.title("Stats Visualizer")
st.caption("Интерактивная визуализация вероятностных распределений")


def base_layout(x_title="x", y_title="f(x)"):
    return dict(
        plot_bgcolor="rgba(0,0,0,0.1)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e0e0e0"),
        margin=dict(l=50, r=20, t=20, b=40),
        xaxis=dict(
            title=x_title,
            gridcolor="rgba(255,255,255,0.1)",
            zerolinecolor="rgba(255,255,255,0.2)",
        ),
        yaxis=dict(
            title=y_title,
            gridcolor="rgba(255,255,255,0.1)",
            zerolinecolor="rgba(255,255,255,0.2)",
        ),
    )


tabs = st.tabs(["Нормальное", "Равномерное", "Экспоненциальное", "Биномиальное", "Пуассона"])

# ── Normal ──────────────────────────────────────────────────────────────────
with tabs[0]:
    st.subheader("Нормальное (гауссово) распределение")
    st.caption("Симметричное колоколообразное распределение, описывающее множество природных явлений.")
    col_plot, col_ctrl = st.columns([2, 1])
    with col_ctrl:
        mu = st.slider("μ (среднее)", -5.0, 5.0, 0.0, 0.1)
        sigma = st.slider("σ (стандартное отклонение)", 0.1, 3.0, 1.0, 0.1)
        variance = round(sigma ** 2, 2)
        st.metric("Среднее E[X]", round(mu, 2))
        st.metric("Дисперсия σ²", variance)
        st.metric("Стд. отклонение σ", round(sigma, 3))
        st.code(f"f(x) = 1/(σ√(2π)) · exp(-(x-μ)²/(2σ²))")
    with col_plot:
        x = np.linspace(mu - 5 * sigma, mu + 5 * sigma, 300)
        y = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))
        fig = go.Figure(
            go.Scatter(
                x=x, y=y,
                mode="lines",
                fill="tozeroy",
                fillcolor="rgba(0,212,255,0.2)",
                line=dict(color="#00d4ff", width=3),
                hovertemplate="x: %{x:.2f}<br>f(x): %{y:.4f}<extra></extra>",
            ),
            layout=base_layout("x", "f(x)"),
        )
        st.plotly_chart(fig, use_container_width=True)

# ── Uniform ──────────────────────────────────────────────────────────────────
with tabs[1]:
    st.subheader("Равномерное распределение")
    st.caption("Все значения в интервале [a, b] равновероятны.")
    col_plot, col_ctrl = st.columns([2, 1])
    with col_ctrl:
        a = st.slider("a (нижняя граница)", -5.0, 5.0, 0.0, 0.1)
        b = st.slider("b (верхняя граница)", 0.0, 15.0, 5.0, 0.1)
    with col_plot:
        if a >= b:
            st.warning("Необходимо a < b")
        else:
            with col_ctrl:
                mean_u = round((a + b) / 2, 2)
                var_u = round((b - a) ** 2 / 12, 4)
                st.metric("Среднее E[X]", mean_u)
                st.metric("Дисперсия", var_u)
                st.metric("Диапазон", f"[{a}, {b}]")
                st.code("f(x) = 1/(b-a)  для a ≤ x ≤ b")
            h = 1 / (b - a)
            x_u = [a - 1, a, a, b, b, b + 1]
            y_u = [0, 0, h, h, 0, 0]
            fig = go.Figure(
                go.Scatter(
                    x=x_u, y=y_u,
                    mode="lines",
                    fill="tozeroy",
                    fillcolor="rgba(0,212,255,0.2)",
                    line=dict(color="#00d4ff", width=3),
                    hovertemplate="x: %{x:.2f}<br>f(x): %{y:.4f}<extra></extra>",
                ),
                layout=base_layout("x", "f(x)"),
            )
            st.plotly_chart(fig, use_container_width=True)

# ── Exponential ───────────────────────────────────────────────────────────────
with tabs[2]:
    st.subheader("Экспоненциальное распределение")
    st.caption("Моделирует время ожидания между событиями в пуассоновском процессе.")
    col_plot, col_ctrl = st.columns([2, 1])
    with col_ctrl:
        lam_e = st.slider("λ (интенсивность)", 0.1, 3.0, 1.0, 0.1)
        st.metric("Среднее E[X]", round(1 / lam_e, 2))
        st.metric("Дисперсия", round(1 / lam_e ** 2, 4))
        st.metric("Мода", 0)
        st.code("f(x) = λ · exp(-λx),  x ≥ 0")
    with col_plot:
        x_e = np.linspace(0, 5 / lam_e, 300)
        y_e = lam_e * np.exp(-lam_e * x_e)
        fig = go.Figure(
            go.Scatter(
                x=x_e, y=y_e,
                mode="lines",
                fill="tozeroy",
                fillcolor="rgba(0,212,255,0.2)",
                line=dict(color="#00d4ff", width=3),
                hovertemplate="x: %{x:.2f}<br>f(x): %{y:.4f}<extra></extra>",
            ),
            layout=base_layout("x", "f(x)"),
        )
        st.plotly_chart(fig, use_container_width=True)

# ── Binomial ──────────────────────────────────────────────────────────────────
with tabs[3]:
    st.subheader("Биномиальное распределение")
    st.caption("Число успехов в n независимых испытаниях с вероятностью успеха p.")
    col_plot, col_ctrl = st.columns([2, 1])
    with col_ctrl:
        n = st.slider("n (число испытаний)", 1, 50, 10, 1)
        p = st.slider("p (вероятность успеха)", 0.0, 1.0, 0.5, 0.05)
        mean_b = round(n * p, 2)
        var_b = round(n * p * (1 - p), 4)
        std_b = round(math.sqrt(n * p * (1 - p)), 3)
        st.metric("Среднее E[X]", mean_b)
        st.metric("Дисперсия", var_b)
        st.metric("Стд. отклонение σ", std_b)
        st.code("P(X=k) = C(n,k) · p^k · (1-p)^(n-k)")
    with col_plot:
        ks = list(range(n + 1))
        pmf = [math.comb(n, k) * p ** k * (1 - p) ** (n - k) for k in ks]
        fig = go.Figure(
            go.Bar(
                x=ks, y=pmf,
                marker_color="#00d4ff",
                hovertemplate="k: %{x}<br>P(X=k): %{y:.4f}<extra></extra>",
            ),
            layout=base_layout("k", "P(X=k)"),
        )
        st.plotly_chart(fig, use_container_width=True)

# ── Poisson ───────────────────────────────────────────────────────────────────
with tabs[4]:
    st.subheader("Распределение Пуассона")
    st.caption("Число событий в фиксированном интервале при постоянной средней интенсивности λ.")
    col_plot, col_ctrl = st.columns([2, 1])
    with col_ctrl:
        lam_p = st.slider("λ (интенсивность)", 0.1, 10.0, 3.0, 0.5)
        st.metric("Среднее E[X]", round(lam_p, 2))
        st.metric("Дисперсия", round(lam_p, 2))
        st.caption("Особенность: E[X] = Var(X) = λ")
        st.code("P(X=k) = (λ^k · e^(-λ)) / k!")
    with col_plot:
        k_max = math.ceil(lam_p + 5 * math.sqrt(lam_p))
        ks_p = list(range(k_max + 1))
        pmf_p = [
            (lam_p ** k * math.exp(-lam_p)) / math.factorial(k)
            for k in ks_p
        ]
        fig = go.Figure(
            go.Bar(
                x=ks_p, y=pmf_p,
                marker_color="#00d4ff",
                hovertemplate="k: %{x}<br>P(X=k): %{y:.4f}<extra></extra>",
            ),
            layout=base_layout("k", "P(X=k)"),
        )
        st.plotly_chart(fig, use_container_width=True)
