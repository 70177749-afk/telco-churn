"""
charts.py — Chart and visualization functions for Telco Churn Dashboard
All charts use a consistent professional colour palette.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

# ── Colour Palette ────────────────────────────────────────────────────────────
PALETTE = {
    "primary":   "#1A73E8",
    "accent":    "#E84545",
    "success":   "#2ECC71",
    "warning":   "#F39C12",
    "neutral":   "#7F8C8D",
    "dark":      "#1C1C2E",
    "light_bg":  "#F5F7FA",
}

CHURN_COLORS  = [PALETTE["success"], PALETTE["accent"]]
CAT_PALETTE   = [PALETTE["primary"], PALETTE["accent"], PALETTE["success"],
                 PALETTE["warning"], PALETTE["neutral"], "#9B59B6", "#1ABC9C"]

def _style_ax(ax, title, xlabel="", ylabel=""):
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12, color=PALETTE["dark"])
    ax.set_xlabel(xlabel, fontsize=11, color=PALETTE["dark"])
    ax.set_ylabel(ylabel, fontsize=11, color=PALETTE["dark"])
    ax.tick_params(colors=PALETTE["dark"])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_facecolor(PALETTE["light_bg"])

def _fig(w=7, h=5):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(PALETTE["light_bg"])
    return fig, ax


# 1. PIE CHART ─────────────────────────────────────────────────────────────────
def pie_churn(df: pd.DataFrame):
    counts = df["Churn"].value_counts()
    fig, ax = _fig(6, 5)
    wedges, texts, autotexts = ax.pie(
        counts,
        labels=counts.index,
        autopct="%1.1f%%",
        colors=CHURN_COLORS,
        startangle=140,
        wedgeprops=dict(edgecolor="white", linewidth=2),
    )
    for t in autotexts:
        t.set_fontsize(12)
        t.set_fontweight("bold")
    ax.set_title("Customer Churn Distribution", fontsize=14, fontweight="bold",
                 color=PALETTE["dark"], pad=14)
    fig.patch.set_facecolor(PALETTE["light_bg"])
    return fig


# 2. HISTOGRAM ─────────────────────────────────────────────────────────────────
def histogram_monthly(df: pd.DataFrame):
    fig, ax = _fig(7, 5)
    ax.hist(df["MonthlyCharges"], bins=30, color=PALETTE["primary"],
            edgecolor="white", linewidth=0.6, alpha=0.9)
    _style_ax(ax, "Distribution of Monthly Charges", "Monthly Charges ($)", "Number of Customers")
    return fig


# 3. LINE CHART ────────────────────────────────────────────────────────────────
def line_tenure_charges(df: pd.DataFrame):
    grouped = (
        df.groupby("tenure")["MonthlyCharges"]
        .mean()
        .reset_index()
    )
    fig, ax = _fig(8, 5)
    ax.plot(grouped["tenure"], grouped["MonthlyCharges"],
            color=PALETTE["primary"], linewidth=2.5, marker="o", markersize=3)
    ax.fill_between(grouped["tenure"], grouped["MonthlyCharges"],
                    alpha=0.15, color=PALETTE["primary"])
    _style_ax(ax, "Avg Monthly Charges Over Customer Tenure",
              "Tenure (months)", "Avg Monthly Charges ($)")
    return fig


# 4. BAR CHART ─────────────────────────────────────────────────────────────────
def bar_contract_churn(df: pd.DataFrame):
    grp = df.groupby(["Contract", "Churn"]).size().unstack(fill_value=0)
    fig, ax = _fig(7, 5)
    grp.plot(kind="bar", ax=ax, color=CHURN_COLORS, edgecolor="white",
             linewidth=0.6, rot=0)
    _style_ax(ax, "Churn Count by Contract Type", "Contract Type", "Number of Customers")
    ax.legend(title="Churn", labels=["No", "Yes"])
    return fig


# 5. SCATTER PLOT ──────────────────────────────────────────────────────────────
def scatter_tenure_total(df: pd.DataFrame):
    fig, ax = _fig(7, 5)
    colors = df["Churn"].map({"No": PALETTE["success"], "Yes": PALETTE["accent"]})
    ax.scatter(df["tenure"], df["TotalCharges"], c=colors,
               alpha=0.5, s=20, edgecolors="none")
    _style_ax(ax, "Tenure vs Total Charges by Churn Status",
              "Tenure (months)", "Total Charges ($)")
    legend_handles = [
        mpatches.Patch(color=PALETTE["success"], label="No Churn"),
        mpatches.Patch(color=PALETTE["accent"],  label="Churned"),
    ]
    ax.legend(handles=legend_handles)
    return fig


# 6. BOX PLOT ──────────────────────────────────────────────────────────────────
def box_monthly_churn(df: pd.DataFrame):
    fig, ax = _fig(6, 5)
    sns.boxplot(data=df, x="Churn", y="MonthlyCharges", ax=ax,
                palette={"No": PALETTE["success"], "Yes": PALETTE["accent"]},
                linewidth=1.5)
    _style_ax(ax, "Monthly Charges: Churn vs No Churn",
              "Churn", "Monthly Charges ($)")
    return fig


# 7. HEATMAP ───────────────────────────────────────────────────────────────────
def heatmap_correlation(df: pd.DataFrame):
    num_cols = ["tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen"]
    corr = df[num_cols].corr()
    fig, ax = _fig(6, 5)
    sns.heatmap(
        corr, annot=True, fmt=".2f", cmap="Blues", ax=ax,
        linewidths=0.5, linecolor="white",
        annot_kws={"size": 11, "weight": "bold"},
    )
    ax.set_title("Feature Correlation Heatmap", fontsize=14, fontweight="bold",
                 color=PALETTE["dark"], pad=12)
    fig.patch.set_facecolor(PALETTE["light_bg"])
    return fig


# 8. AREA CHART ────────────────────────────────────────────────────────────────
def area_tenure_group(df: pd.DataFrame):
    grp = (
        df.groupby(["TenureGroup", "Churn"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    fig, ax = _fig(8, 5)
    ax.fill_between(range(len(grp)), grp.get("No", 0),
                    color=PALETTE["success"], alpha=0.7, label="No Churn")
    ax.fill_between(range(len(grp)), grp.get("Yes", 0),
                    color=PALETTE["accent"], alpha=0.7, label="Churned")
    ax.set_xticks(range(len(grp)))
    ax.set_xticklabels(grp["TenureGroup"].astype(str), rotation=15)
    _style_ax(ax, "Cumulative Churn Trend Across Tenure Groups",
              "Tenure Group", "Number of Customers")
    ax.legend()
    return fig


# 9. COUNT PLOT ────────────────────────────────────────────────────────────────
def count_internet_service(df: pd.DataFrame):
    fig, ax = _fig(7, 5)
    order = df["InternetService"].value_counts().index
    sns.countplot(data=df, x="InternetService", hue="Churn", ax=ax,
                  order=order,
                  palette={"No": PALETTE["success"], "Yes": PALETTE["accent"]})
    _style_ax(ax, "Internet Service Type — Churn Frequency",
              "Internet Service", "Count")
    ax.legend(title="Churn")
    return fig


# 10. VIOLIN PLOT ──────────────────────────────────────────────────────────────
def violin_tenure_churn(df: pd.DataFrame):
    fig, ax = _fig(6, 5)
    sns.violinplot(data=df, x="Churn", y="tenure", ax=ax,
                   palette={"No": PALETTE["success"], "Yes": PALETTE["accent"]},
                   inner="quartile", linewidth=1.2)
    _style_ax(ax, "Tenure Distribution by Churn Status",
              "Churn", "Tenure (months)")
    return fig


# BONUS — PAIR PLOT ────────────────────────────────────────────────────────────
def pair_plot(df: pd.DataFrame):
    sub = df[["tenure", "MonthlyCharges", "TotalCharges", "Churn"]].copy()
    g = sns.pairplot(sub, hue="Churn",
                     palette={"No": PALETTE["success"], "Yes": PALETTE["accent"]},
                     plot_kws={"alpha": 0.4, "s": 15},
                     diag_kind="kde")
    g.figure.suptitle("Pair Plot of Numerical Features by Churn", y=1.02,
                       fontsize=13, fontweight="bold")
    return g.figure
