# import streamlit as st
# import streamlit.components.v1 as components
# import numpy as np
# import joblib
# import pandas as pd

# st.set_page_config(page_title="Campaign Response Predictor", layout="wide", page_icon=None)

# # ── Baked-in model coefficients (from training) ──────────────────
# INTERCEPT = -0.7650
# COEFS = {
#     "Recency":              -0.760459,
#     "Income":               -0.079304,
#     "Age":                  -0.032300,
#     "Total_Children":       -0.404187,
#     "Total_Spent":           0.879627,
#     "Total_Accepted_Cmp":    0.966136,
#     "NumWebPurchases":       0.103399,
#     "NumCatalogPurchases":   0.365338,
#     "NumStorePurchases":    -0.580991,
#     "NumDealsPurchases":     0.372935,
#     "NumWebVisitsMonth":     0.760046,
#     "Education":             0.400106,
#     "MntWines":             -0.601146,
#     "MntMeatProducts":       0.408248,
# }
# MEANS = {
#     "Recency": 49.109375, "Income": 52237.975, "Age": 45.194,
#     "Total_Children": 0.950, "Total_Spent": 605.798, "Total_Accepted_Cmp": 0.298,
#     "NumWebPurchases": 4.085, "NumCatalogPurchases": 2.662, "NumStorePurchases": 5.790,
#     "NumDealsPurchases": 2.325, "NumWebVisitsMonth": 5.317, "Education": 1.666,
#     "MntWines": 303.936, "MntMeatProducts": 166.950,
# }
# STDS = {
#     "Recency": 28.956, "Income": 25032.366, "Age": 11.981,
#     "Total_Children": 0.752, "Total_Spent": 602.115, "Total_Accepted_Cmp": 0.678,
#     "NumWebPurchases": 2.778, "NumCatalogPurchases": 2.922, "NumStorePurchases": 3.250,
#     "NumDealsPurchases": 1.932, "NumWebVisitsMonth": 2.426, "Education": 0.839,
#     "MntWines": 336.522, "MntMeatProducts": 225.665,
# }
# EDUCATION_ORDER = {"Basic": 0, "Bachelor": 1, "Master": 2, "PhD": 3}
# FEATURE_LABELS = {
#     "Recency": "Recency (days)", "Income": "Income", "Age": "Age",
#     "Total_Children": "Children at home", "Total_Spent": "Total spend",
#     "Total_Accepted_Cmp": "Past campaigns accepted", "NumWebPurchases": "Web purchases",
#     "NumCatalogPurchases": "Catalog purchases", "NumStorePurchases": "Store purchases",
#     "NumDealsPurchases": "Deal purchases", "NumWebVisitsMonth": "Web visits/month",
#     "Education": "Education level", "MntWines": "Wines spend", "MntMeatProducts": "Meat spend",
# }

# def compute_score(vals):
#     logit = INTERCEPT
#     contribs = {}
#     for k, coef in COEFS.items():
#         z = (vals[k] - MEANS[k]) / STDS[k]
#         c = coef * z
#         logit += c
#         contribs[k] = c
#     prob = 1 / (1 + np.exp(-logit))
#     return round(float(prob), 4), logit, contribs

# # ── Sidebar inputs ───────────────────────────────────────────────
# with st.sidebar:
#     st.markdown("## Customer Profile")
#     st.markdown("---")
#     st.markdown("**Demographics**")
#     year_birth    = st.slider("Birth Year", 1940, 1999, 1975)
#     income        = st.number_input("Annual Income ($)", 0, 200000, 51381)
#     education     = st.selectbox("Education", ["Basic", "Bachelor", "Master", "PhD"])
#     marital       = st.selectbox("Marital Status", ["Single", "Married", "Divorced", "Together", "Widow"])
#     kidhome       = st.number_input("Kids at Home", 0, 3, 0)
#     teenhome      = st.number_input("Teens at Home", 0, 3, 0)

#     st.markdown("---")
#     st.markdown("**Engagement**")
#     recency           = st.slider("Days Since Last Purchase", 0, 99, 49)
#     num_web_visits    = st.slider("Web Visits / Month", 0, 20, 5)
#     num_web_purch     = st.slider("Web Purchases", 0, 27, 4)
#     num_cat_purch     = st.slider("Catalog Purchases", 0, 28, 3)
#     num_store_purch   = st.slider("Store Purchases", 0, 13, 6)
#     num_deals_purch   = st.slider("Deal Purchases", 0, 15, 2)

#     st.markdown("---")
#     st.markdown("**Spending ($)**")
#     wines  = st.slider("Wines",  0, 1493, 174)
#     meat   = st.slider("Meat",   0, 1000,  68)
#     fruits = st.slider("Fruits", 0,  199,   8)
#     fish   = st.slider("Fish",   0,  259,  12)
#     sweets = st.slider("Sweets", 0,  262,   8)
#     gold   = st.slider("Gold",   0,  321,  24)

#     st.markdown("---")
#     st.markdown("**Past Campaigns**")
#     cmp1 = st.checkbox("Accepted Campaign 1")
#     cmp2 = st.checkbox("Accepted Campaign 2")
#     cmp3 = st.checkbox("Accepted Campaign 3")
#     cmp4 = st.checkbox("Accepted Campaign 4")
#     cmp5 = st.checkbox("Accepted Campaign 5")

# # ── Compute features ─────────────────────────────────────────────
# age              = 2014 - year_birth
# total_children   = kidhome + teenhome
# total_spent      = wines + fruits + meat + fish + sweets + gold
# total_accepted   = int(cmp1)+int(cmp2)+int(cmp3)+int(cmp4)+int(cmp5)
# edu_enc          = EDUCATION_ORDER[education]

# vals = {
#     "Recency":            recency,
#     "Income":             income,
#     "Age":                age,
#     "Total_Children":     total_children,
#     "Total_Spent":        total_spent,
#     "Total_Accepted_Cmp": total_accepted,
#     "NumWebPurchases":    num_web_purch,
#     "NumCatalogPurchases":num_cat_purch,
#     "NumStorePurchases":  num_store_purch,
#     "NumDealsPurchases":  num_deals_purch,
#     "NumWebVisitsMonth":  num_web_visits,
#     "Education":          edu_enc,
#     "MntWines":           wines,
#     "MntMeatProducts":    meat,
# }

# prob, logit, contribs = compute_score(vals)
# pct = int(prob * 100)

# # ── Color palette ────────────────────────────────────────────────
# if prob >= 0.6:
#     arc_color, verdict_text, verdict_color = "#3dd68c", "High likelihood to respond", "#3dd68c"
# elif prob >= 0.35:
#     arc_color, verdict_text, verdict_color = "#f7b84f", "Moderate — worth targeting", "#f7b84f"
# else:
#     arc_color, verdict_text, verdict_color = "#4f8ef7", "Unlikely to respond", "#7b84a3"

# # ── Top factors ──────────────────────────────────────────────────
# sorted_contribs = sorted(contribs.items(), key=lambda x: abs(x[1]), reverse=True)[:6]
# max_abs = max(abs(v) for _, v in sorted_contribs) or 0.01

# factors_html = ""
# for k, c in sorted_contribs:
#     bar_pct = int(abs(c) / max_abs * 100)
#     color   = "#3dd68c" if c > 0 else "#f75f5f"
#     sign    = "+" if c > 0 else "−"
#     label   = FEATURE_LABELS.get(k, k)
#     factors_html += f"""
#     <div style="display:flex;align-items:center;gap:10px;margin-bottom:9px">
#       <span style="color:{color};font-size:13px;width:14px;text-align:center;flex-shrink:0">{sign}</span>
#       <span style="font-size:12px;color:#7b84a3;width:160px;flex-shrink:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{label}</span>
#       <div style="flex:1;height:6px;background:#2a3050;border-radius:3px;overflow:hidden">
#         <div style="width:{bar_pct}%;height:100%;background:{color};border-radius:3px"></div>
#       </div>
#     </div>"""

# # ── SVG gauge arc math ───────────────────────────────────────────
# import math
# cx, cy, r = 110, 100, 80
# start_angle = math.pi
# end_angle   = 0
# sweep       = prob * math.pi
# curr_angle  = start_angle + sweep
# x1s, y1s    = cx + r * math.cos(start_angle), cy + r * math.sin(start_angle)
# x1e, y1e    = cx + r * math.cos(end_angle),   cy + r * math.sin(end_angle)
# xce, yce    = cx + r * math.cos(curr_angle),  cy + r * math.sin(curr_angle)
# large_bg    = 1
# large_arc   = 1 if sweep > math.pi else 0

# # ── Main layout ──────────────────────────────────────────────────
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@600;700&display=swap');
# section.main > div { padding-top: 1.5rem; }
# .block-container { padding: 1.5rem 2rem; }
# </style>
# """, unsafe_allow_html=True)

# st.markdown("""
# <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:700;color:#e8eaf0;margin-bottom:4px">
#   Campaign Response Predictor
# </div>
# <div style="font-family:'DM Mono',monospace;font-size:12px;color:#7b84a3;margin-bottom:1.5rem">
#   Logistic regression · 2,240 customers · ROC-AUC 0.866
# </div>
# """, unsafe_allow_html=True)

# col1, col2, col3 = st.columns([1.2, 1, 1])

# # ── Card 1: Gauge ────────────────────────────────────────────────
# with col1:
#     components.html(f"""
#     <div style="background:#181c26;border:1px solid #2a3050;border-radius:12px;padding:1.5rem;font-family:'DM Mono',monospace">
#       <div style="font-size:10px;letter-spacing:0.12em;color:#7b84a3;text-transform:uppercase;margin-bottom:1rem;padding-bottom:8px;border-bottom:1px solid #2a3050">
#         Response Probability
#       </div>
#       <div style="text-align:center">
#         <svg width="220" height="115" viewBox="0 0 220 115" xmlns="http://www.w3.org/2000/svg">
#           <!-- bg arc -->
#           <path d="M {x1s:.2f},{y1s:.2f} A {r},{r} 0 {large_bg},1 {x1e:.2f},{y1e:.2f}"
#                 fill="none" stroke="#2a3050" stroke-width="14" stroke-linecap="round"/>
#           <!-- filled arc -->
#           <path d="M {x1s:.2f},{y1s:.2f} A {r},{r} 0 {large_arc},1 {xce:.2f},{yce:.2f}"
#                 fill="none" stroke="{arc_color}" stroke-width="14" stroke-linecap="round"/>
#           <!-- center text -->
#           <text x="110" y="88" text-anchor="middle"
#                 font-family="Syne,sans-serif" font-size="32" font-weight="700" fill="{arc_color}">{pct}%</text>
#           <text x="110" y="108" text-anchor="middle"
#                 font-family="DM Mono,monospace" font-size="10" fill="#7b84a3">probability</text>
#         </svg>
#         <div style="font-size:12px;color:{verdict_color};margin-top:4px;letter-spacing:0.04em">{verdict_text}</div>
#         <div style="margin-top:12px;background:#1f2536;border:1px solid #2a3050;border-radius:6px;padding:8px 12px;font-size:11px;color:#7b84a3;text-align:left">
#           logit = <span style="color:#4f8ef7">{logit:.3f}</span> &nbsp;·&nbsp; P = 1 / (1 + e<sup>–logit</sup>)
#         </div>
#         <div style="margin-top:10px;display:flex;gap:8px;justify-content:center">
#           <div style="background:#1f2536;border:1px solid #2a3050;border-radius:6px;padding:6px 10px;font-size:11px;color:#7b84a3">
#             Base rate <span style="color:#e8eaf0">15.0%</span>
#           </div>
#           <div style="background:#1f2536;border:1px solid #2a3050;border-radius:6px;padding:6px 10px;font-size:11px;color:#7b84a3">
#             Threshold <span style="color:#e8eaf0">0.30</span>
#           </div>
#         </div>
#       </div>
#     </div>
#     """, height=310)

# # ── Card 2: Top factors ──────────────────────────────────────────
# with col2:
#     components.html(f"""
#     <div style="background:#181c26;border:1px solid #2a3050;border-radius:12px;padding:1.5rem;font-family:'DM Mono',monospace;height:100%">
#       <div style="font-size:10px;letter-spacing:0.12em;color:#7b84a3;text-transform:uppercase;margin-bottom:1rem;padding-bottom:8px;border-bottom:1px solid #2a3050">
#         Top Influencing Factors
#       </div>
#       {factors_html}
#       <div style="margin-top:14px;font-size:10px;color:#4a5070;border-top:1px solid #2a3050;padding-top:10px">
#         Bar width = relative contribution magnitude
#       </div>
#     </div>
#     """, height=310)

# # ── Card 3: Customer summary ─────────────────────────────────────
# with col3:
#     def row(label, val, highlight=False):
#         color = "#e8eaf0" if highlight else "#a0a8c0"
#         return f"""<div style="display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid #1f2536">
#           <span style="font-size:11px;color:#7b84a3">{label}</span>
#           <span style="font-size:12px;color:{color};font-weight:{'500' if highlight else '400'}">{val}</span>
#         </div>"""

#     cmps_accepted = f"{total_accepted} / 5"
#     components.html(f"""
#     <div style="background:#181c26;border:1px solid #2a3050;border-radius:12px;padding:1.5rem;font-family:'DM Mono',monospace">
#       <div style="font-size:10px;letter-spacing:0.12em;color:#7b84a3;text-transform:uppercase;margin-bottom:1rem;padding-bottom:8px;border-bottom:1px solid #2a3050">
#         Customer Snapshot
#       </div>
#       {row("Age", f"{age} yrs")}
#       {row("Income", f"${income:,}")}
#       {row("Education", education)}
#       {row("Marital status", marital)}
#       {row("Children at home", total_children)}
#       {row("Days since purchase", recency, highlight=True)}
#       {row("Campaigns accepted", cmps_accepted, highlight=True)}
#       {row("Total spend", f"${total_spent:,}", highlight=True)}
#       {row("Web visits / mo", num_web_visits)}
#     </div>
#     """, height=310)

# # ── Verdict banner ───────────────────────────────────────────────
# banner_bg     = "#0d2318" if prob >= 0.6 else ("#2a1f06" if prob >= 0.35 else "#0d1526")
# banner_border = arc_color
# icon          = "✅" if prob >= 0.6 else ("⚠️" if prob >= 0.35 else "✕")
# action        = "Include in next campaign" if prob >= 0.6 else ("Worth targeting — monitor response" if prob >= 0.35 else "Consider excluding from campaign")

# st.markdown(f"""
# <div style="margin-top:1rem;background:{banner_bg};border:1px solid {banner_border};border-radius:10px;
#             padding:1rem 1.5rem;display:flex;align-items:center;gap:1rem;font-family:'DM Mono',monospace">
#   <span style="font-size:22px">{icon}</span>
#   <div>
#     <div style="font-size:13px;color:{arc_color};font-weight:500">{action}</div>
#     <div style="font-size:11px;color:#7b84a3;margin-top:2px">
#       Predicted probability {pct}% · Base rate 15% · Model accuracy 80.5%
#     </div>
#   </div>
# </div>
# """, unsafe_allow_html=True)
import streamlit as st

def show_page():
    st.title("Dashboard Page")
