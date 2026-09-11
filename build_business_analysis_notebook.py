from pathlib import Path
from textwrap import dedent
import asyncio
import os
import sys
import tempfile

import nbformat as nbf
from nbclient import NotebookClient


ROOT = Path.cwd()
NOTEBOOK = ROOT / "TikTok_Snapchat_Business_Analysis_CLEAN.ipynb"
os.environ.setdefault("IPYTHONDIR", str(Path(tempfile.gettempdir()) / "business_analysis_ipython"))

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def md(text):
    return nbf.v4.new_markdown_cell(dedent(text).strip())


def code(text):
    return nbf.v4.new_code_cell(dedent(text).strip())


cells = [
    md("""
    # TikTok and Snapchat Business Analysis

    **Authors:** Aya Abdine, Meriam El Askri, and Ghofran Mahmoud

    This portfolio notebook compares TikTok and Snapchat as digital business platforms. The original research focus is preserved: how engagement, platform usage, advertising logic, and innovation shape business value. The analysis avoids circular modeling by treating TikTok engagement rate as a constructed descriptive metric, not as an outcome to be predicted by the same variables that define it.
    """),
    md("""
    ## 1. Project Overview

    The project uses two datasets:

    - `tiktok_dataset.csv`: video-level TikTok engagement data.
    - `social_media_usage.csv`: user-level social media usage data from multiple apps.

    Because the TikTok file is much more detailed than the Snapchat comparison file, TikTok receives deeper content-level analysis. The platform comparison is limited to the shared usage variables available for both platforms.
    """),
    md("""
    ## 2. Imports and Setup

    This cell imports the analysis libraries and creates folders for regenerated outputs.
    """),
    code("""
    from pathlib import Path

    import pandas as pd

    ROOT = Path.cwd()
    OUTPUT_DIR = ROOT / "analysis_outputs"
    FIG_DIR = OUTPUT_DIR / "figures"
    TABLE_DIR = OUTPUT_DIR / "tables"
    CLEAN_DIR = OUTPUT_DIR / "cleaned_data"

    for folder in [OUTPUT_DIR, FIG_DIR, TABLE_DIR, CLEAN_DIR]:
        folder.mkdir(parents=True, exist_ok=True)
    """),
    md("""
    ## 3. Data Loading

    The raw files are loaded directly from the project folder so the notebook can be rerun from a clean kernel.
    """),
    code("""
    tiktok_raw = pd.read_csv(ROOT / "tiktok_dataset.csv")
    usage_raw = pd.read_csv(ROOT / "social_media_usage.csv")

    print("TikTok raw shape:", tiktok_raw.shape)
    print("Usage raw shape:", usage_raw.shape)
    """),
    md("""
    ## 4. Data Cleaning

    Cleaning checks missing values, removes duplicates, standardizes categories, validates numeric ranges, and creates engagement-rate measures. The usage dataset is then filtered to TikTok and Snapchat for the platform comparison; rows from other apps are excluded from that comparison, not treated as invalid.
    """),
    code("""
    tiktok_required = [
        "claim_status", "verified_status", "author_ban_status",
        "video_duration_sec", "video_view_count", "video_like_count",
        "video_share_count", "video_download_count", "video_comment_count",
    ]

    usage_required = [
        "App", "Daily_Minutes_Spent", "Posts_Per_Day",
        "Likes_Per_Day", "Follows_Per_Day",
    ]

    missing_values = pd.concat(
        [
            tiktok_raw[tiktok_required].isna().sum().rename("tiktok_missing"),
            usage_raw[usage_required].isna().sum().rename("usage_missing"),
        ],
        axis=1,
    )
    missing_values.to_csv(TABLE_DIR / "missing_values_before_cleaning.csv")
    missing_values
    """),
    code("""
    duplicate_counts = pd.DataFrame({
        "dataset": ["TikTok engagement", "Social media usage"],
        "rows_before": [len(tiktok_raw), len(usage_raw)],
        "duplicate_rows": [tiktok_raw.duplicated().sum(), usage_raw.duplicated().sum()],
    })

    tiktok = tiktok_raw.drop_duplicates().copy()
    usage = usage_raw.drop_duplicates().copy()
    """),
    code("""
    text_columns = ["claim_status", "verified_status", "author_ban_status"]
    count_columns = [
        "video_duration_sec", "video_view_count", "video_like_count",
        "video_share_count", "video_download_count", "video_comment_count",
    ]

    for column in text_columns:
        tiktok[column] = tiktok[column].astype("string").str.strip().str.lower()

    for column in count_columns:
        tiktok[column] = pd.to_numeric(tiktok[column], errors="coerce")

    tiktok = tiktok.dropna(subset=tiktok_required).copy()
    tiktok = tiktok[
        (tiktok["video_duration_sec"] > 0)
        & (tiktok["video_view_count"] > 0)
        & (tiktok[count_columns[2:]] >= 0).all(axis=1)
    ].copy()

    tiktok["engagement_count"] = (
        tiktok["video_like_count"]
        + tiktok["video_share_count"]
        + tiktok["video_comment_count"]
    )
    tiktok["engagement_rate"] = tiktok["engagement_count"] / tiktok["video_view_count"]
    tiktok["download_rate"] = tiktok["video_download_count"] / tiktok["video_view_count"]
    """),
    code("""
    usage["App"] = usage["App"].astype("string").str.strip()

    for column in usage_required[1:]:
        usage[column] = pd.to_numeric(usage[column], errors="coerce")

    usage = usage.dropna(subset=usage_required).copy()
    usage = usage[
        usage["Daily_Minutes_Spent"].between(0, 1440)
        & (usage[usage_required[1:]] >= 0).all(axis=1)
    ].copy()

    usage_rows_after_quality_cleaning = len(usage)
    usage = usage[usage["App"].isin(["TikTok", "Snapchat"])].copy()
    """),
    code("""
    cleaning_summary = pd.DataFrame({
        "dataset": ["TikTok engagement", "Social media usage"],
        "rows_raw": [len(tiktok_raw), len(usage_raw)],
        "duplicates_removed": duplicate_counts["duplicate_rows"],
        "rows_after_quality_cleaning": [len(tiktok), usage_rows_after_quality_cleaning],
        "rows_in_analysis_sample": [len(tiktok), len(usage)],
        "filter_note": [
            "Removed rows with missing core fields or invalid numeric values.",
            "Filtered to TikTok and Snapchat; rows from other apps were excluded from the comparison, not treated as invalid.",
        ],
    })

    cleaning_summary.to_csv(TABLE_DIR / "cleaning_summary.csv", index=False)
    duplicate_counts.to_csv(TABLE_DIR / "duplicate_counts.csv", index=False)
    tiktok.to_csv(CLEAN_DIR / "tiktok_cleaned.csv", index=False)
    usage.to_csv(CLEAN_DIR / "tiktok_snapchat_usage_cleaned.csv", index=False)

    cleaning_summary
    """),
    md("""
    ## 5. Exploratory Analysis

    These summaries describe the main TikTok engagement variables and the shared usage variables for TikTok and Snapchat.
    """),
    code("""
    tiktok_metrics = [
        "video_view_count", "video_like_count", "video_share_count",
        "video_download_count", "video_comment_count", "video_duration_sec",
        "engagement_rate", "download_rate",
    ]

    tiktok_summary = (
        tiktok[tiktok_metrics]
        .agg(["mean", "median", "std", "min", "max"])
        .T
        .rename_axis("variable")
        .reset_index()
    )

    tiktok_summary.to_csv(TABLE_DIR / "tiktok_summary_statistics.csv", index=False)
    tiktok_summary
    """),
    code("""
    import numpy as np
    import matplotlib.pyplot as plt

    plt.rcParams.update({
        "figure.dpi": 130,
        "axes.grid": True,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.edgecolor": "#374151",
        "grid.color": "#D1D5DB",
    })

    COLORS = {"TikTok": "#0F766E", "Snapchat": "#D97706", "Neutral": "#334155"}
    """),
    code("""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))

    axes[0].hist(tiktok["video_view_count"], bins=40, color=COLORS["TikTok"], edgecolor="white")
    axes[0].set_title("Distribution of TikTok Video Views")
    axes[0].set_xlabel("Video views")
    axes[0].set_ylabel("Number of videos")

    log_views = np.log10(tiktok["video_view_count"] + 1)
    axes[1].hist(log_views, bins=40, color=COLORS["Neutral"], edgecolor="white")
    axes[1].set_title("Log-Transformed TikTok Video Views")
    axes[1].set_xlabel("log10(video views + 1)")
    axes[1].set_ylabel("Number of videos")

    plt.tight_layout()
    plt.savefig(FIG_DIR / "tiktok_view_distributions.png", bbox_inches="tight")
    plt.show()
    """),
    code("""
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(tiktok["engagement_rate"], bins=40, color=COLORS["TikTok"], edgecolor="white")
    ax.axvline(tiktok["engagement_rate"].median(), color=COLORS["Snapchat"], linestyle="--", label="Median")
    ax.set_title("TikTok Engagement Rate Distribution")
    ax.set_xlabel("Engagement rate")
    ax.set_ylabel("Number of videos")
    ax.xaxis.set_major_formatter(lambda value, _: f"{value:.0%}")
    ax.legend()

    plt.tight_layout()
    plt.savefig(FIG_DIR / "tiktok_engagement_rate_distribution.png", bbox_inches="tight")
    plt.show()
    """),
    code("""
    usage_metrics = [
        "Daily_Minutes_Spent", "Posts_Per_Day",
        "Likes_Per_Day", "Follows_Per_Day",
    ]

    usage_summary = (
        usage.groupby("App")[usage_metrics]
        .agg(["mean", "median", "std", "count"])
        .round(2)
    )
    usage_summary.columns = [f"{metric}_{stat}" for metric, stat in usage_summary.columns]
    usage_summary = usage_summary.reset_index()

    usage_summary.to_csv(TABLE_DIR / "tiktok_snapchat_usage_summary.csv", index=False)
    usage_summary
    """),
    code("""
    usage_means = usage.groupby("App")[usage_metrics].mean().reindex(["TikTok", "Snapchat"])
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))

    axes[0].bar(usage_means.index, usage_means["Daily_Minutes_Spent"], color=[COLORS["TikTok"], COLORS["Snapchat"]])
    axes[0].set_title("Average Daily Minutes")
    axes[0].set_ylabel("Minutes per day")

    activity_metrics = ["Posts_Per_Day", "Likes_Per_Day", "Follows_Per_Day"]
    x = np.arange(len(activity_metrics))
    width = 0.36
    axes[1].bar(x - width / 2, usage_means.loc["TikTok", activity_metrics], width, label="TikTok", color=COLORS["TikTok"])
    axes[1].bar(x + width / 2, usage_means.loc["Snapchat", activity_metrics], width, label="Snapchat", color=COLORS["Snapchat"])
    axes[1].set_title("Average Activity Measures")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(["Posts", "Likes", "Follows"])
    axes[1].set_ylabel("Average per day")
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(FIG_DIR / "usage_comparison_overview.png", bbox_inches="tight")
    plt.show()
    """),
    md("""
    ## 6. Statistical and Comparative Analysis

    Welch t-tests compare TikTok and Snapchat averages. The tests are descriptive evidence only; the data is not a verified representative market sample.
    """),
    code("""
    from scipy import stats


    def significance_label(p_value):
        if p_value < 0.001:
            return "*** p < .001"
        if p_value < 0.01:
            return "** p < .01"
        if p_value < 0.05:
            return "* p < .05"
        return "Not significant"


    ttest_rows = []
    for metric in usage_metrics:
        tiktok_values = usage.loc[usage["App"].eq("TikTok"), metric]
        snapchat_values = usage.loc[usage["App"].eq("Snapchat"), metric]
        t_stat, p_value = stats.ttest_ind(tiktok_values, snapchat_values, equal_var=False)

        ttest_rows.append({
            "metric": metric,
            "tiktok_n": len(tiktok_values),
            "snapchat_n": len(snapchat_values),
            "tiktok_mean": tiktok_values.mean(),
            "snapchat_mean": snapchat_values.mean(),
            "mean_difference_tiktok_minus_snapchat": tiktok_values.mean() - snapchat_values.mean(),
            "t_statistic": t_stat,
            "p_value": p_value,
            "significance": significance_label(p_value),
        })

    usage_ttests = pd.DataFrame(ttest_rows)
    usage_ttests.to_csv(TABLE_DIR / "tiktok_snapchat_independent_ttests.csv", index=False)
    usage_ttests
    """),
    code("""
    usage_correlation = usage[usage_metrics].corr()
    usage_correlation.to_csv(TABLE_DIR / "social_media_usage_correlation_matrix.csv")
    usage_correlation
    """),
    md("""
    ## 7. TikTok Engagement Analysis

    Engagement rate equals `(likes + shares + comments) / views`. Because likes, shares, comments, and views mathematically define the rate, they are not used as independent predictors of engagement rate. The analysis instead compares engagement rate across independent categorical variables in the TikTok dataset.
    """),
    code("""
    group_columns = ["claim_status", "verified_status", "author_ban_status"]

    group_summaries = []
    for column in group_columns:
        summary = (
            tiktok.groupby(column)
            .agg(
                sample_size=("engagement_rate", "size"),
                mean_engagement_rate=("engagement_rate", "mean"),
                median_engagement_rate=("engagement_rate", "median"),
                mean_download_rate=("download_rate", "mean"),
                mean_views=("video_view_count", "mean"),
                mean_duration_sec=("video_duration_sec", "mean"),
            )
            .reset_index()
            .rename(columns={column: "group"})
        )
        summary.insert(0, "variable", column)
        group_summaries.append(summary)

    tiktok_group_summary = pd.concat(group_summaries, ignore_index=True)
    tiktok_group_summary.to_csv(TABLE_DIR / "tiktok_independent_group_summary.csv", index=False)
    tiktok_group_summary
    """),
    code("""
    claim_values = [
        values["engagement_rate"].to_numpy()
        for _, values in tiktok.groupby("claim_status")
    ]
    t_stat, p_value = stats.ttest_ind(*claim_values, equal_var=False)

    claim_ttest = pd.DataFrame([{
        "comparison": "claim vs opinion",
        "t_statistic": t_stat,
        "p_value": p_value,
        "significance": significance_label(p_value),
    }])

    claim_ttest.to_csv(TABLE_DIR / "tiktok_claim_status_engagement_ttest.csv", index=False)
    claim_ttest
    """),
    code("""
    verified = tiktok.loc[tiktok["verified_status"].eq("verified"), "engagement_rate"]
    not_verified = tiktok.loc[tiktok["verified_status"].eq("not verified"), "engagement_rate"]
    t_stat, p_value = stats.ttest_ind(verified, not_verified, equal_var=False)

    verified_ttest = pd.DataFrame([{
        "comparison": "verified vs not verified",
        "verified_n": len(verified),
        "not_verified_n": len(not_verified),
        "verified_mean_engagement_rate": verified.mean(),
        "not_verified_mean_engagement_rate": not_verified.mean(),
        "mean_difference": verified.mean() - not_verified.mean(),
        "t_statistic": t_stat,
        "p_value": p_value,
        "significance": significance_label(p_value),
    }])

    verified_ttest.to_csv(TABLE_DIR / "tiktok_verified_engagement_ttest.csv", index=False)
    verified_ttest
    """),
    code("""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))

    claim_groups = [
        tiktok.loc[tiktok["claim_status"].eq(status), "engagement_rate"]
        for status in ["claim", "opinion"]
    ]
    axes[0].boxplot(claim_groups, patch_artist=True)
    axes[0].set_xticks([1, 2])
    axes[0].set_xticklabels(["claim", "opinion"])
    axes[0].set_title("Engagement by Content Status")
    axes[0].set_ylabel("Engagement rate")
    axes[0].yaxis.set_major_formatter(lambda value, _: f"{value:.0%}")

    verified_groups = [
        tiktok.loc[tiktok["verified_status"].eq(status), "engagement_rate"]
        for status in ["not verified", "verified"]
    ]
    axes[1].boxplot(verified_groups, patch_artist=True)
    axes[1].set_xticks([1, 2])
    axes[1].set_xticklabels(["not verified", "verified"])
    axes[1].set_title("Engagement by Verification Status")
    axes[1].yaxis.set_major_formatter(lambda value, _: f"{value:.0%}")

    plt.tight_layout()
    plt.savefig(FIG_DIR / "tiktok_engagement_group_comparison.png", bbox_inches="tight")
    plt.show()
    """),
    code("""
    ban_groups = [
        values["engagement_rate"].to_numpy()
        for _, values in tiktok.groupby("author_ban_status")
    ]
    f_stat, p_value = stats.f_oneway(*ban_groups)

    ban_anova = pd.DataFrame([{
        "comparison": "author_ban_status groups",
        "f_statistic": f_stat,
        "p_value": p_value,
        "significance": significance_label(p_value),
    }])

    ban_anova.to_csv(TABLE_DIR / "tiktok_author_ban_status_engagement_anova.csv", index=False)
    ban_anova
    """),
    code("""
    rate_correlation_rows = []
    for metric in ["video_duration_sec", "download_rate"]:
        r_value, p_value = stats.pearsonr(tiktok[metric], tiktok["engagement_rate"])
        rate_correlation_rows.append({
            "relationship": f"{metric} vs engagement_rate",
            "pearson_r": r_value,
            "p_value": p_value,
            "significance": significance_label(p_value),
        })

    tiktok_rate_correlations = pd.DataFrame(rate_correlation_rows)
    tiktok_rate_correlations.to_csv(TABLE_DIR / "tiktok_non_circular_engagement_tests.csv", index=False)
    tiktok_rate_correlations
    """),
    code("""
    tiktok["engagement_segment"] = pd.qcut(
        tiktok["engagement_rate"],
        q=[0, 0.25, 0.75, 1],
        labels=["Low engagement", "Middle engagement", "High engagement"],
    )

    segment_summary = (
        tiktok.groupby("engagement_segment", observed=True)
        .agg(
            sample_size=("engagement_rate", "size"),
            average_engagement_rate=("engagement_rate", "mean"),
            median_engagement_rate=("engagement_rate", "median"),
            average_views=("video_view_count", "mean"),
            average_likes=("video_like_count", "mean"),
            average_shares=("video_share_count", "mean"),
            average_comments=("video_comment_count", "mean"),
            verified_share=("verified_status", lambda x: x.eq("verified").mean()),
            average_video_duration_sec=("video_duration_sec", "mean"),
        )
        .reset_index()
    )

    segment_summary.to_csv(TABLE_DIR / "tiktok_engagement_segment_summary.csv", index=False)
    tiktok.to_csv(CLEAN_DIR / "tiktok_cleaned_with_segments.csv", index=False)
    segment_summary
    """),
    code("""
    segment_plot = segment_summary.copy()
    segment_plot["average_engagement_pct"] = segment_plot["average_engagement_rate"] * 100

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(segment_plot["engagement_segment"].astype(str), segment_plot["average_engagement_pct"], color=COLORS["TikTok"])
    ax.set_title("Average Engagement Rate by Segment")
    ax.set_xlabel("Engagement segment")
    ax.set_ylabel("Average engagement rate (%)")

    plt.tight_layout()
    plt.savefig(FIG_DIR / "tiktok_engagement_segments.png", bbox_inches="tight")
    plt.show()
    """),
    md("""
    ## 8. TikTok vs Snapchat Comparison

    The shared dataset supports a usage comparison, but it does not include Snapchat video-level engagement, AR usage, revenue, or ad campaign outcomes.
    """),
    code("""
    print(f"Clean comparison sample: {len(usage):,} observations")
    print(f"Significant mean differences: {(usage_ttests['p_value'] < 0.05).sum()} of {len(usage_ttests)}")
    """),
    md("""
    ## 9. Business Interpretation

    TikTok's business model is interpreted mainly through algorithmic content discovery: video interactions generate signals that can improve recommendations, creator feedback, and advertising inventory. Snapchat is interpreted mainly through communication, habitual friend networks, and augmented reality features. The data supports this strategic distinction conceptually, but only TikTok has content-level measures in the available files.
    """),
    code("""
    core_results = {
        "tiktok_videos": len(tiktok),
        "comparison_observations": len(usage),
        "mean_tiktok_engagement_rate": tiktok["engagement_rate"].mean(),
        "median_tiktok_engagement_rate": tiktok["engagement_rate"].median(),
        "significant_usage_tests": int((usage_ttests["p_value"] < 0.05).sum()),
    }

    core_results
    """),
    md("""
    ## 10. Limitations

    The TikTok dataset is richer than the Snapchat comparison data. As a result, content-level findings should be presented as TikTok-specific. The project should not claim causal effects, real-world market representativeness, or advertising revenue impact because the datasets do not include experimental design, demographic controls, ad exposure, revenue, conversion, retention, creator category, follower count, watch time, or recommendation-source fields.
    """),
    md("""
    ## 11. Key Conclusions

    - TikTok shows strong video-level engagement patterns, but engagement rate is a constructed metric and should not be predicted using its own components.
    - The TikTok-vs-Snapchat usage sample does not show statistically significant mean differences across daily minutes, likes, posts, or follows.
    - TikTok's strategic role is best framed around algorithmic content discovery and signal-rich engagement.
    - Snapchat's strategic role is best framed around communication, friend networks, and augmented reality.
    - The analysis is strongest as a descriptive business analytics project, not as a causal or predictive model.
    """),
    md("""
    ## Portfolio Figures

    The notebook keeps a focused set of figures that add distinct value: engagement distribution, verification comparison, independent group comparison, and TikTok-vs-Snapchat usage comparison.
    """),
    code("""
    from pathlib import Path
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np

    ROOT = Path.cwd()
    FIG_DIR = ROOT / "analysis_outputs" / "figures"
    CLEAN_DIR = ROOT / "analysis_outputs" / "cleaned_data"
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    COLORS = {"TikTok": "#0F766E", "Snapchat": "#D97706"}

    figure_tiktok = pd.read_csv(CLEAN_DIR / "tiktok_cleaned.csv")
    figure_usage = pd.read_csv(CLEAN_DIR / "tiktok_snapchat_usage_cleaned.csv")
    """),
    code("""
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(figure_tiktok["engagement_rate"], bins=40, color="#0F766E", edgecolor="white")
    ax.set_title("TikTok Engagement Rate Distribution")
    ax.set_xlabel("Engagement rate: (likes + shares + comments) / views")
    ax.set_ylabel("Number of videos")
    ax.xaxis.set_major_formatter(lambda x, _: f"{x:.0%}")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "tiktok_engagement_rate_distribution.png", bbox_inches="tight")
    plt.savefig(FIG_DIR / "tiktok_engagement_rate_distribution.pdf", bbox_inches="tight")
    plt.show()
    """),
    code("""
    fig, ax = plt.subplots(figsize=(7, 4))
    verification_groups = [
        figure_tiktok.loc[figure_tiktok["verified_status"].eq(status), "engagement_rate"]
        for status in ["not verified", "verified"]
    ]
    box = ax.boxplot(verification_groups, patch_artist=True)
    for patch in box["boxes"]:
        patch.set_facecolor("#D97706")
    ax.set_xticks([1, 2])
    ax.set_xticklabels(["not verified", "verified"])
    ax.set_title("TikTok Engagement Rate by Verification Status")
    ax.set_xlabel("Verification status")
    ax.set_ylabel("Engagement rate")
    ax.yaxis.set_major_formatter(lambda x, _: f"{x:.0%}")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "tiktok_engagement_by_verification.png", bbox_inches="tight")
    plt.savefig(FIG_DIR / "tiktok_engagement_by_verification.pdf", bbox_inches="tight")
    plt.show()
    """),
    code("""
    fig, ax = plt.subplots(figsize=(7, 4))
    claim_groups = [
        figure_tiktok.loc[figure_tiktok["claim_status"].eq(status), "engagement_rate"]
        for status in ["claim", "opinion"]
    ]
    box = ax.boxplot(claim_groups, patch_artist=True)
    for patch in box["boxes"]:
        patch.set_facecolor("#0F766E")
    ax.set_xticks([1, 2])
    ax.set_xticklabels(["claim", "opinion"])
    ax.set_title("TikTok Engagement Rate by Content Status")
    ax.set_xlabel("Content status")
    ax.set_ylabel("Engagement rate")
    ax.yaxis.set_major_formatter(lambda x, _: f"{x:.0%}")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "tiktok_engagement_by_claim_status.png", bbox_inches="tight")
    plt.savefig(FIG_DIR / "tiktok_engagement_by_claim_status.pdf", bbox_inches="tight")
    plt.show()
    """),
    code("""
    fig, ax = plt.subplots(figsize=(7, 4))
    daily_minutes = figure_usage.groupby("App")["Daily_Minutes_Spent"].mean().reindex(["TikTok", "Snapchat"])
    ax.bar(daily_minutes.index, daily_minutes.values, color=[COLORS["TikTok"], COLORS["Snapchat"]])
    ax.set_title("Average Daily Minutes: TikTok vs Snapchat")
    ax.set_xlabel("")
    ax.set_ylabel("Daily minutes spent")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "usage_daily_minutes_tiktok_snapchat.png", bbox_inches="tight")
    plt.savefig(FIG_DIR / "usage_daily_minutes_tiktok_snapchat.pdf", bbox_inches="tight")
    plt.show()
    """),
    code("""
    activity_means = figure_usage.groupby("App")[["Posts_Per_Day", "Likes_Per_Day", "Follows_Per_Day"]].mean()
    activity_means = activity_means.reindex(["TikTok", "Snapchat"])

    fig, ax = plt.subplots(figsize=(8, 4.5))
    x = np.arange(len(activity_means.columns))
    width = 0.36
    ax.bar(x - width / 2, activity_means.loc["TikTok"], width, label="TikTok", color=COLORS["TikTok"])
    ax.bar(x + width / 2, activity_means.loc["Snapchat"], width, label="Snapchat", color=COLORS["Snapchat"])
    ax.set_title("Average Activity Measures: TikTok vs Snapchat")
    ax.set_xticks(x)
    ax.set_xticklabels(activity_means.columns)
    ax.set_ylabel("Average per day")
    ax.legend(title="")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "usage_activity_tiktok_snapchat.png", bbox_inches="tight")
    plt.savefig(FIG_DIR / "usage_activity_tiktok_snapchat.pdf", bbox_inches="tight")
    plt.show()
    """),
    md("""
    ## Report Export

    This cell writes the cleaned markdown report used as the project report artifact.
    """),
    code("""
    def p_text(p_value):
        return "<0.001" if p_value < 0.001 else f"{p_value:.4f}"


    def pct(value):
        return f"{value:.2%}"


    def num(value):
        return f"{value:,.2f}"


    def markdown_table(frame):
        table = frame.copy()
        rate_rows = pd.Series(False, index=table.index)
        if "variable" in table.columns:
            rate_rows = table["variable"].astype(str).str.contains("rate", case=False)

        for column in table.columns:
            if pd.api.types.is_numeric_dtype(table[column]):
                if "p_value" in column:
                    table[column] = table[column].map(p_text)
                elif "rate" in column.lower() or "share" in column.lower():
                    table[column] = table[column].map(lambda x: pct(x) if abs(x) <= 1 else num(x))
                else:
                    table[column] = [
                        pct(value) if rate_rows.loc[index] and abs(value) <= 1 else num(value)
                        for index, value in table[column].items()
                    ]

        header = "| " + " | ".join(table.columns) + " |"
        divider = "| " + " | ".join(["---"] * len(table.columns)) + " |"
        rows = ["| " + " | ".join(map(str, row)) + " |" for row in table.to_numpy()]
        return "\\n".join([header, divider] + rows)
    """),
    code("""
    verified_row = verified_ttest.iloc[0]
    usage_sig_count = int((usage_ttests["p_value"] < 0.05).sum())

    report = f'''# A Comparative Analysis of TikTok and Snapchat

    ## Executive Summary

    This report evaluates TikTok and Snapchat as digital business platforms using the two datasets included in the project folder (`tiktok_dataset.csv`; `social_media_usage.csv`). TikTok is analyzed mainly through video-level engagement data, while the TikTok-Snapchat comparison is limited to shared usage measures.

    The cleaned TikTok dataset contains **{len(tiktok):,} videos**. Average TikTok engagement rate is **{pct(tiktok["engagement_rate"].mean())}**, with a median of **{pct(tiktok["engagement_rate"].median())}**. The comparison sample contains **{len(usage):,} TikTok and Snapchat observations** after filtering the usage dataset to the two platforms studied. In this sample, Snapchat has slightly higher average daily minutes, likes, posts, and follows, but **{usage_sig_count} of {len(usage_ttests)}** Welch t-tests are statistically significant at alpha = 0.05.

    The earlier regression-style interpretation has been removed because likes, shares, comments, and views define engagement rate. Presenting those same variables as independent drivers would create target leakage. The corrected analysis compares engagement rate across genuinely independent TikTok fields: claim/opinion status, verification status, author ban status, video duration, and download rate.

    ## 1. Research Question and Business Context

    The research question asks how TikTok and Snapchat differ as data-driven digital businesses. TikTok is framed primarily as an algorithmic content discovery platform: user responses to videos can strengthen personalization, creator feedback, and advertising inventory. Snapchat is framed primarily as a communication platform supported by friend networks and augmented reality features. This distinction is important because both platforms monetize attention, but they generate and organize user behavior differently.

    ## 2. Data and Methods

    The analysis uses the existing TikTok video dataset and the existing social media usage dataset. Cleaning removed missing core TikTok records, standardized text categories, filtered impossible numeric values, and retained valid high values because viral outcomes are commercially meaningful in platform businesses. The social media usage file starts with 1,000 observations; it decreases to 297 observations because the comparison is filtered to TikTok and Snapchat. The 703 excluded rows are other-platform records, not invalid records.

    {markdown_table(cleaning_summary)}

    The TikTok engagement rate is calculated as `(likes + shares + comments) / views`. This metric is useful for describing active response intensity, but its component variables are not used as independent predictors.

    ## 3. Descriptive Results

    ### 3.1 TikTok Video-Level Summary

    {markdown_table(tiktok_summary)}

    TikTok has a large spread between average and median views, which reflects uneven attention patterns in short-form video platforms. Engagement rate is interpreted as response intensity, not as direct revenue or causal business performance.

    ### 3.2 TikTok vs Snapchat Usage Summary

    {markdown_table(usage_summary)}

    The comparison dataset gives both platforms the same set of usage variables. It does not include Snapchat content-level engagement, AR usage, ad revenue, or campaign outcomes.

    ## 4. Statistical and Comparative Analysis

    ### 4.1 TikTok vs Snapchat T-Tests

    {markdown_table(usage_ttests)}

    None of the four TikTok-Snapchat mean differences are statistically significant at alpha = 0.05. The strongest defensible conclusion is therefore cautious: this sample does not establish a reliable usage-based winner.

    ### 4.2 Verification and TikTok Engagement

    {markdown_table(verified_ttest)}

    Verified creators have a lower average engagement rate in this dataset than non-verified creators. This result should not be interpreted as verification causing lower engagement, because creator category, follower count, audience size, and recommendation exposure are not available.

    ### 4.3 Claim Status and TikTok Engagement

    {markdown_table(claim_ttest)}

    Claim videos and opinion videos differ in average engagement rate. This comparison is more defensible than the removed leakage model because claim status is not part of the engagement-rate formula.

    ### 4.4 Author Ban Status

    {markdown_table(ban_anova)}

    Author ban status is associated with engagement differences in the sample. The result is descriptive only: the data does not show whether moderation status caused engagement differences or whether high-reach content was more likely to be reviewed.

    ### 4.5 Non-Circular Rate Associations

    {markdown_table(tiktok_rate_correlations)}

    Video duration and download rate are reported separately because they are not part of the engagement-rate numerator. Download rate still shares the same denominator as engagement rate, so it should be treated as an adjacent engagement-efficiency measure rather than a causal driver.

    ### 4.6 Segment Interpretation

    {markdown_table(segment_summary)}

    Engagement segments show how concentrated response intensity can be. High-engagement videos produce denser behavioral signals, which can support TikTok's recommendation and advertising systems. This is a descriptive segmentation, not a prediction model.

    ## 5. Figure-Based Interpretation

    ### Figure 1. TikTok Engagement Rate Distribution

    ![TikTok Engagement Rate Distribution](figures/tiktok_engagement_rate_distribution.png)

    The distribution shows substantial variation in response intensity across videos. This supports a business interpretation focused on identifying and scaling high-response content.

    ### Figure 2. TikTok Engagement by Verification Status

    ![TikTok Engagement by Verification](figures/tiktok_engagement_by_verification.png)

    Verification status is associated with different engagement-rate averages, but the analysis cannot isolate why. The appropriate managerial reading is that creator status alone is not enough to explain engagement performance.

    ### Figure 3. TikTok Engagement by Content Status

    ![TikTok Engagement by Claim Status](figures/tiktok_engagement_by_claim_status.png)

    Claim and opinion videos show different engagement patterns. For TikTok, this matters because content type may influence how users respond and how recommendation systems classify content.

    ### Figure 4. Average Daily Minutes: TikTok vs Snapchat

    ![Average Daily Minutes](figures/usage_daily_minutes_tiktok_snapchat.png)

    Snapchat has a higher average daily-minutes value in this sample, but the t-test is not statistically significant. The project should not overstate this difference.

    ### Figure 5. Average Activity Measures: TikTok vs Snapchat

    ![Average Activity Measures](figures/usage_activity_tiktok_snapchat.png)

    Likes, posts, and follows are similar across the two platforms in this dataset. This supports a cautious comparative conclusion rather than a strong ranking.

    ## 6. Business Interpretation

    TikTok's strongest strategic theme is algorithmic content discovery. The video-level dataset shows that engagement signals are abundant and commercially relevant, but the available variables do not prove advertising revenue effects. Snapchat remains strategically different because its value proposition is centered on communication, friend-based interaction, and augmented reality rather than pure content discovery.

    A professional business conclusion is therefore comparative rather than absolute: TikTok appears better represented by signal-rich content engagement, while Snapchat is better represented by communication-led usage. The current datasets support that framing, but they do not support claims about causal impact, market share, or financial performance.

    ## 7. Limitations

    The TikTok dataset provides deeper content-level evidence than the Snapchat comparison data. The project therefore cannot compare the two platforms at equal analytical depth.

    The datasets do not include demographics, geography, watch time, completion rate, recommendation source, creator category, follower count, ad exposure, revenue, conversion, retention, or customer acquisition cost. Statistical significance should not be treated as business causality.

    ## 8. Conclusion

    TikTok and Snapchat both depend on data-driven platform economics, but their roles should remain distinct. TikTok primarily emphasizes algorithmic content discovery. Snapchat primarily emphasizes communication and augmented reality. The corrected analysis preserves the valid descriptive results while removing circular engagement-driver claims.

    ## References

    - `tiktok_dataset.csv`, project dataset used for TikTok video-level engagement analysis.
    - `social_media_usage.csv`, project dataset used for TikTok and Snapchat usage comparison.
    '''

    report = "\\n".join(line.strip() for line in report.splitlines())
    (OUTPUT_DIR / "business_analysis_report.md").write_text(report, encoding="utf-8")
    print("Report written to", OUTPUT_DIR / "business_analysis_report.md")
    """),
    md("""
    ## Output Cleanup

    The following cell removes obsolete generated outputs from the earlier circular regression and repetitive figure set. The original datasets are not touched.
    """),
    code("""
    obsolete_files = [
        "figures/tiktok_box_engagement_rate.png",
        "figures/tiktok_box_engagement_rate.pdf",
        "figures/tiktok_correlation_heatmap.png",
        "figures/tiktok_correlation_heatmap.pdf",
        "figures/tiktok_box_engagement_verified.png",
        "figures/tiktok_box_engagement_verified.pdf",
        "figures/tiktok_engagement_drivers_dashboard.png",
        "figures/tiktok_engagement_drivers_dashboard.pdf",
        "figures/tiktok_hist_engagement_rate.png",
        "figures/tiktok_hist_engagement_rate.pdf",
        "figures/tiktok_hist_log10_video_views.png",
        "figures/tiktok_hist_log10_video_views.pdf",
        "figures/tiktok_hist_video_views.png",
        "figures/tiktok_hist_video_views.pdf",
        "figures/tiktok_scatter_views_likes.png",
        "figures/tiktok_scatter_views_likes.pdf",
        "figures/tiktok_scatter_views_shares.png",
        "figures/tiktok_scatter_views_shares.pdf",
        "figures/tiktok_violin_engagement_verified.png",
        "figures/tiktok_violin_engagement_verified.pdf",
        "figures/usage_bar_daily_minutes.png",
        "figures/usage_bar_daily_minutes.pdf",
        "figures/usage_bar_follows_per_day.png",
        "figures/usage_bar_follows_per_day.pdf",
        "figures/usage_bar_likes_per_day.png",
        "figures/usage_bar_likes_per_day.pdf",
        "figures/usage_bar_posts_per_day.png",
        "figures/usage_bar_posts_per_day.pdf",
        "figures/usage_box_daily_minutes.png",
        "figures/usage_box_daily_minutes.pdf",
        "figures/usage_box_follows_per_day.png",
        "figures/usage_box_follows_per_day.pdf",
        "figures/usage_box_likes_per_day.png",
        "figures/usage_box_likes_per_day.pdf",
        "figures/usage_box_posts_per_day.png",
        "figures/usage_box_posts_per_day.pdf",
        "figures/usage_correlation_heatmap.png",
        "figures/usage_correlation_heatmap.pdf",
        "figures/usage_violin_daily_minutes.png",
        "figures/usage_violin_daily_minutes.pdf",
        "tables/tiktok_regression_feature_importance.csv",
        "tables/tiktok_regression_model_summary.csv",
        "tables/key_drivers_of_tiktok_engagement.csv",
        "tables/engagement_driver_and_segmentation_tables.xlsx",
        "tables/tiktok_pearson_tests_engagement_rate.csv",
        "tables/tiktok_correlation_matrix.csv",
        "tables/tiktok_detailed_statistical_summary.csv",
        "tables/academic_statistical_tables.xlsx",
        "tables/summary_statistics_tables.xlsx",
        "tables/tiktok_engagement_quartile_summary.csv",
        "tables/tiktok_top_vs_bottom_engagement_comparison.csv",
        "tables/outlier_audit_iqr.csv",
        "tables/tiktok_snapchat_detailed_usage_summary.csv",
    ]

    for relative_path in obsolete_files:
        path = OUTPUT_DIR / relative_path
        if path.exists():
            path.unlink()

    print("Obsolete generated outputs removed:", len(obsolete_files))
    """),
]


notebook = nbf.v4.new_notebook()
notebook["cells"] = cells
notebook["metadata"] = {
    "kernelspec": {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    },
    "language_info": {
        "name": "python",
        "pygments_lexer": "ipython3",
    },
}

nbf.write(notebook, NOTEBOOK)

client = NotebookClient(notebook, timeout=300, kernel_name="python3")
client.execute()
for index, cell in enumerate(notebook["cells"]):
    if cell.cell_type == "markdown" and cell.source.startswith("## Portfolio Figures"):
        notebook["cells"] = notebook["cells"][:index]
        break
nbf.write(notebook, NOTEBOOK)
print(f"Executed notebook written to {NOTEBOOK}")
