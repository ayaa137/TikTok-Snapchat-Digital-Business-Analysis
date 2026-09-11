# TikTok and Snapchat Business Analysis

**Authors:** Aya Abdine, Meriam El Askri, and Ghofran Mahmoud

This project compares TikTok and Snapchat as digital business platforms using engagement and usage data. The research focus is on how platform activity supports business models, advertising logic, and innovation strategy.

## Project Files

- `TikTok_Snapchat_Business_Analysis.ipynb` — main portfolio notebook
- `TikTok_Snapchat_Business_Analysis.html` — exported HTML version of the notebook
- `tiktok_dataset.csv` — original TikTok video-level dataset
- `social_media_usage.csv` — original social media usage dataset
- `analysis_outputs/` — cleaned data, tables, figures, and written report
- `build_business_analysis_notebook.py` — rebuilds and executes the notebook
- `validate_notebook.py` — checks that the notebook runs successfully
- `requirements.txt` — required Python packages

## Research Question

**How do TikTok and Snapchat differ in their data-driven business models, advertising-based revenue mechanisms, and innovation strategies, and how do these differences influence their competitive advantage in the digital platform economy?**

## Key Analytical Choice

The notebook treats `engagement_rate` as a constructed descriptive metric:

`engagement_rate = (likes + shares + comments) / views`

Because likes, shares, comments, and views directly define this metric, they are not used as independent predictors of engagement rate.

The corrected analysis instead uses non-circular comparisons based on variables such as:

- Content status
- Verification status
- Author ban status
- Video duration
- Download rate

## Main Findings

- The cleaned TikTok dataset contains **19,084 videos**.
- TikTok's average engagement rate is approximately **33.19%**, with a median of approximately **31.57%**.
- The TikTok vs Snapchat comparison contains **297 observations**.
- Snapchat shows slightly higher average usage values in the available comparison sample.
- However, none of the four Welch independent-sample t-tests are statistically significant at **α = 0.05**.
- TikTok is interpreted mainly through **algorithmic content discovery and personalization**.
- Snapchat is interpreted mainly through **communication, friend networks, and augmented reality**.

## Business Interpretation

TikTok and Snapchat compete within the same digital attention economy but create value differently.

### TikTok

TikTok's strategy is primarily associated with:

- Algorithmic content discovery
- Personalized recommendations
- Creator activity
- User-generated content
- Advertising inventory
- Data-driven engagement

### Snapchat

Snapchat's strategy is primarily associated with:

- Communication
- Friend networks
- Private social interaction
- Visual communication
- Augmented reality
- Advertising

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

Export the notebook to HTML:

```bash
jupyter nbconvert --to html TikTok_Snapchat_Business_Analysis.ipynb
```

## Project Structure

```text
TikTok-Snapchat-Digital-Business-Analysis/
│
├── README.md
├── requirements.txt
├── TikTok_Snapchat_Business_Analysis.ipynb
├── TikTok_Snapchat_Business_Analysis.html
├── build_business_analysis_notebook.py
├── validate_notebook.py
├── tiktok_dataset.csv
├── social_media_usage.csv
│
└── analysis_outputs/
    ├── cleaned_data/
    ├── figures/
    ├── tables/
    └── business_analysis_report.md
```

## Limitations

The TikTok dataset provides much deeper content-level information than the Snapchat comparison data.

The project does not include variables such as:

- Demographics
- Advertising revenue
- Campaign outcomes
- Watch time
- Recommendation source
- Creator category
- Follower count

Therefore, the findings should be interpreted as **descriptive business analysis supported by statistical evidence**, rather than causal or predictive evidence.

## Authors

**Aya Abdine**  
**Meriam El Askri**  
**Ghofran Mahmoud**

Digital Business Models and Functions  
Constructor University