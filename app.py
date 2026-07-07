import gradio as gr

from engine import PredictionEngine
import pandas as pd

from loaders import load_retail_model, load_sme_model

retail_engine = PredictionEngine(load_retail_model())
sme_engine = PredictionEngine(load_sme_model())


def get_recommendation(pd):
    if pd < 0.02:
        return "🟢 Approve"
    elif pd < 0.08:
        return "🟠 Manual Review"
    else:
        return "🔴 Reject"


def format_tier(tier):
    colors = {
        "Low": "🟢 Low",
        "Medium": "🟡 Medium",
        "High": "🟠 High",
        "Critical": "🔴 Critical",
    }
    return colors.get(tier, tier)


def predict_retail(
    revolving_utilization,
    age,
    late_30_59,
    debt_ratio,
    monthly_income,
    open_credit_lines,
    late_90,
    real_estate_loans,
    late_60_89,
    dependents,
    income_missing,
    dependents_missing,
):
    features = {
        "RevolvingUtilizationOfUnsecuredLines": revolving_utilization,
        "age": age,
        "NumberOfTime30-59DaysPastDueNotWorse": late_30_59,
        "DebtRatio": debt_ratio,
        "MonthlyIncome": monthly_income,
        "NumberOfOpenCreditLinesAndLoans": open_credit_lines,
        "NumberOfTimes90DaysLate": late_90,
        "NumberRealEstateLoansOrLines": real_estate_loans,
        "NumberOfTime60-89DaysPastDueNotWorse": late_60_89,
        "NumberOfDependents": dependents,
        "income_missing": int(income_missing),
        "dependents_missing": int(dependents_missing),
    }

    result = retail_engine.predict(features)

    pd = result["prediction"]["probability"]
    score = result["prediction"]["score"]
    tier = result["prediction"]["tier"]

    recommendation = get_recommendation(pd)

    probability_md = f"""
### Probability of Default

# **{pd:.2%}**
"""

    score_md = f"""
### Credit Score

# **{score:.0f}**
"""

    tier_md = f"""
### Risk Tier

# **{format_tier(tier)}**
"""

    recommendation_md = f"""
### Recommendation

# **{recommendation}**
"""

    drivers_md = "## Why was this predicted?\n\n"

    for driver in result["explanation"]["drivers"]:
        icon = "📉" if driver["impact"] < 0 else "📈"

        drivers_md += (
            f"{icon} **{driver['reason']}**\n\n"
            f"Impact on score: `{driver['impact']:.2f}`\n\n"
        )

    return (
        probability_md,
        score_md,
        tier_md,
        recommendation_md,
        drivers_md,
    )

def predict_sme(file):
    if file is None:
        raise gr.Error("Please upload a CSV file.")

    df = pd.read_csv(file.name)

    features = df.iloc[0].to_dict()

    result = sme_engine.predict(features)

    pd_value = result["prediction"]["probability"]
    score = result["prediction"]["score"]
    tier = result["prediction"]["tier"]

    recommendation = get_recommendation(pd_value)

    probability_md = f"""
### Probability of Default

# **{pd_value:.2%}**
"""

    score_md = f"""
### Credit Score

# **{score:.0f}**
"""

    tier_md = f"""
### Risk Tier

# **{format_tier(tier)}**
"""

    recommendation_md = f"""
### Recommendation

# **{recommendation}**
"""

    drivers_md = "## Why was this predicted?\n\n"

    for driver in result["explanation"]["drivers"]:
        icon = "📉" if driver["impact"] < 0 else "📈"

        drivers_md += (
            f"{icon} **{driver['reason']}**\n\n"
            f"Impact on score: `{driver['impact']:.2f}`\n\n"
        )

    return (
        probability_md,
        score_md,
        tier_md,
        recommendation_md,
        drivers_md,
    )

with gr.Blocks(
    title="Default Risk Platform",
    theme=gr.themes.Soft(),
) as demo:

    gr.Markdown(
        """
# 🏦 Default Risk Platform

### Explainable AI Credit Risk Assessment

Estimate **Probability of Default**, generate a standardized **Credit Score**, and understand **why** the model reached its decision using SHAP explainability.
"""
    )

    with gr.Tab("🏠 Retail"):

        gr.Markdown("## Borrower Information")

        with gr.Row():

            with gr.Column():

                age = gr.Number(label="Age", value=59)

                monthly_income = gr.Number(
                    label="Monthly Income",
                    value=5500,
                )

                debt_ratio = gr.Number(
                    label="Debt Ratio",
                    value=0.57,
                )

                revolving_utilization = gr.Number(
                    label="Revolving Utilization",
                    value=1.0,
                )

                dependents = gr.Number(
                    label="Dependents",
                    value=1,
                )

            with gr.Column():

                open_credit_lines = gr.Number(
                    label="Open Credit Lines",
                    value=10,
                )

                real_estate_loans = gr.Number(
                    label="Real Estate Loans",
                    value=2,
                )

                late_30_59 = gr.Number(
                    label="30–59 Days Late",
                    value=0,
                )

                late_60_89 = gr.Number(
                    label="60–89 Days Late",
                    value=0,
                )

                late_90 = gr.Number(
                    label="90+ Days Late",
                    value=0,
                )

        with gr.Accordion("Advanced Options", open=False):

            income_missing = gr.Checkbox(
                label="Income Missing",
                value=False,
            )

            dependents_missing = gr.Checkbox(
                label="Dependents Missing",
                value=False,
            )

        predict_btn = gr.Button(
            "🔍 Predict Credit Risk",
            variant="primary",
            size="lg",
        )

        gr.Markdown("---")

        with gr.Row():

            probability = gr.Markdown()

            score = gr.Markdown()

        with gr.Row():

            tier = gr.Markdown()

            recommendation = gr.Markdown()

        drivers = gr.Markdown()

        predict_btn.click(
            predict_retail,
            inputs=[
                revolving_utilization,
                age,
                late_30_59,
                debt_ratio,
                monthly_income,
                open_credit_lines,
                late_90,
                real_estate_loans,
                late_60_89,
                dependents,
                income_missing,
                dependents_missing,
            ],
            outputs=[
                probability,
                score,
                tier,
                recommendation,
                drivers,
            ],
        )

    with gr.Tab("🏢 SME"):

        gr.Markdown(
            """
    ## SME / Corporate Credit Risk

    Upload a CSV containing a single company's financial ratios.
    """
        )

        csv_file = gr.File(
            label="Upload SME CSV",
            file_types=[".csv"],
        )

        predict_btn_sme = gr.Button(
            "🔍 Predict SME Credit Risk",
            variant="primary",
            size="lg",
        )

        gr.Markdown("---")

        with gr.Row():

            probability_sme = gr.Markdown()

            score_sme = gr.Markdown()

        with gr.Row():

            tier_sme = gr.Markdown()

            recommendation_sme = gr.Markdown()

        drivers_sme = gr.Markdown()

        predict_btn_sme.click(
            predict_sme,
            inputs=[csv_file],
            outputs=[
                probability_sme,
                score_sme,
                tier_sme,
                recommendation_sme,
                drivers_sme,
            ],
        )
demo.launch()