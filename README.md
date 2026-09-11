# TikTok and Snapchat Business Analysis

**Authors:** Aya Abdine, Meriam El Askri, and Ghofran Mahmoud

This project compares TikTok and Snapchat as digital business platforms using engagement and usage data. The research focus is on how platform activity supports business models, advertising logic, and innovation strategy.

## Project Files

- `TikTok_Snapchat_Business_Analysis_CLEAN.ipynb` is the main portfolio notebook.
- `TikTok_Snapchat_Business_Analysis.html` is an exported HTML version of the notebook.
- `tiktok_dataset.csv` is the original TikTok video-level dataset.
- `social_media_usage.csv` is the original social media usage dataset.
- `analysis_outputs/` contains regenerated cleaned data, tables, figures, and the written report.
- `build_business_analysis_notebook.py` rebuilds and executes the notebook.

## Key Analytical Choice

The notebook treats `engagement_rate` as a constructed descriptive metric:

`engagement_rate = (likes + shares + comments) / views`

Because likes, shares, comments, and views define this metric, they are not used as independent predictors of engagement rate. The corrected analysis uses non-circular comparisons based on fields such as content status, verification status, author ban status, video duration, and download rate.

## Main Findings

- The cleaned TikTok dataset contains 19,084 videos.
- TikTok's average engagement rate is 33.19%, with a median of 31.57%.
- The TikTok vs Snapchat comparison dataset contains 297 observations.
- Snapchat has slightly higher average usage values in this sample, but none of the four Welch t-tests are statistically significant at alpha = 0.05.
- TikTok is interpreted mainly through algorithmic content discovery.
- Snapchat is interpreted mainly through communication and augmented reality.

## How to Run

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Run the notebook from a clean kernel, or rebuild the executed notebook and report with:

```bash
python build_business_analysis_notebook.py
```

Validate that every notebook cell executes without hidden variables:

```bash
python validate_notebook.py
```

Export the notebook to HTML with:

```bash
jupyter nbconvert --to html TikTok_Snapchat_Business_Analysis.ipynb
```

## Limitations

The TikTok dataset provides deeper content-level analysis than the Snapchat comparison data. The project does not include demographics, ad revenue, campaign outcomes, watch time, recommendation source, creator category, or follower count, so the findings should be read as descriptive business analysis rather than causal evidence.
