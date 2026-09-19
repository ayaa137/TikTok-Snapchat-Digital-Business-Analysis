
# 📱 TikTok vs Snapchat: Data-Driven Digital Business Analysis

This project compares TikTok and Snapchat as digital business platforms, focusing on how data, user engagement, advertising mechanisms, and innovation contribute to value creation and competitive advantage.

The analysis combines **business-model evaluation, exploratory data analysis, statistical testing, and strategic interpretation** using TikTok video-level data and cross-platform social media usage data.

## 🔍 Research Question

**How do TikTok and Snapchat differ in their data-driven business models, advertising-based revenue mechanisms, and innovation strategies, and how do these differences influence their competitive advantage in the digital platform economy?**

The project examines differences in:

- User engagement
- Platform activity
- Data utilization
- Advertising-based revenue models
- Content discovery and communication
- Innovation strategy
- Competitive positioning

## 📊 Project Overview

The project includes:

- Data quality assessment and cleaning
- Exploratory data analysis
- TikTok engagement analysis
- TikTok vs Snapchat usage comparison
- Welch independent-sample t-tests
- Engagement comparisons across creator and content characteristics
- Engagement segmentation
- Statistical interpretation
- Business-model comparison
- Revenue and advertising analysis
- Innovation and competitive-advantage analysis
- Limitations and strategic interpretation

## 📦 Datasets

Two datasets are used in the analysis.

### TikTok Video Dataset

The TikTok dataset contains video-level information used to study content engagement and creator characteristics.

After cleaning, the final dataset contains:

- **19,084 TikTok videos**

The dataset includes variables related to views, likes, comments, shares, downloads, video duration, creator verification, claim status, and author status.

### Social Media Usage Dataset

The second dataset contains user-level activity across several social media platforms.

For this project, the data is filtered to **TikTok and Snapchat only**, resulting in:

- **297 TikTok and Snapchat observations**

The shared variables used for comparison include:

- Daily minutes spent
- Posts per day
- Likes per day
- Follows per day

The TikTok dataset provides much deeper content-level information than the Snapchat comparison dataset, so the detailed engagement analysis focuses primarily on TikTok.

## 📈 Statistical Results

| **Analysis** | **Result** |
|---|---:|
| Cleaned TikTok videos | **19,084** |
| Mean TikTok engagement rate | **33.19%** |
| Median TikTok engagement rate | **31.57%** |
| TikTok vs Snapchat observations | **297** |
| Shared usage measures tested | **4** |
| Significant Welch t-tests at α = 0.05 | **0 of 4** |

Snapchat shows slightly higher average values across several usage measures in the available sample.

However, none of the four Welch independent-sample t-tests are statistically significant at **α = 0.05**, so these differences should not be interpreted as strong evidence that one platform consistently produces higher levels of user activity.

## 🧪 Important Methodological Choice

TikTok engagement rate is calculated as:

`engagement_rate = (likes + shares + comments) / views`

Because likes, shares, comments, and views directly define the engagement-rate metric, they are **not used as independent predictors of engagement rate**.

Using these variables to predict engagement rate would create a circular relationship and could produce misleading conclusions.

The corrected analysis therefore focuses on non-circular comparisons involving variables such as:

- Claim status
- Creator verification status
- Author ban status
- Video duration
- Download rate

This keeps the analysis descriptive and statistically defensible rather than forcing an inappropriate predictive model.

## 💡 Key Findings

- The cleaned TikTok dataset contains **19,084 videos**.
- TikTok's average engagement rate is approximately **33.19%**.
- The median engagement rate is approximately **31.57%**.
- Engagement differs across several creator and content characteristics.
- Download rate shows a strong positive relationship with engagement.
- Video duration shows little meaningful relationship with engagement.
- The TikTok vs Snapchat comparison contains **297 observations**.
- Snapchat has slightly higher sample averages across several activity measures.
- None of the four cross-platform Welch t-tests are statistically significant at **α = 0.05**.
- TikTok is strategically associated with algorithmic content discovery and personalization.
- Snapchat is strategically associated with communication, friend networks, visual interaction, and augmented reality.
- Both platforms compete for user attention and advertising revenue while creating value through different mechanisms.

## 💼 Business Interpretation

### TikTok

TikTok's digital business model is strongly associated with:

- Algorithmic content discovery
- Personalized recommendations
- Creator ecosystems
- User-generated content
- High-volume content consumption
- Data-driven engagement
- Digital advertising
- Social commerce

TikTok creates value primarily by continuously connecting users with personalized content through its recommendation system.

### Snapchat

Snapchat follows a different strategic model centered around:

- Private communication
- Friend networks
- Visual messaging
- Social interaction
- Stories and short-form content
- Augmented reality
- Digital advertising
- Premium services such as Snapchat+

Snapchat differentiates itself through communication-oriented experiences and innovation in augmented reality.

## 🛠️ Technologies Used

- Python
- pandas
- NumPy
- SciPy
- Matplotlib
- Jupyter Notebook
- Git
- GitHub

## 📁 Repository Structure

```text
TikTok-Snapchat-Digital-Business-Analysis/
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
    ├── business_analysis_report.md
    ├── cleaned_data/
    ├── figures/
    └── tables/
```

## 📓 Full Analysis

The complete project analysis is available in:

- `TikTok_Snapchat_Business_Analysis.ipynb` — complete Jupyter Notebook
- `TikTok_Snapchat_Business_Analysis.html` — exported HTML version
- `analysis_outputs/business_analysis_report.md` — written business analysis
- `analysis_outputs/figures/` — generated visualizations
- `analysis_outputs/tables/` — statistical results and summary tables

## ▶️ Reproducing the Analysis

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Rebuild and execute the notebook:

```bash
python build_business_analysis_notebook.py
```

Validate that all notebook cells execute successfully:

```bash
python validate_notebook.py
```

Export the notebook to HTML:

```bash
jupyter nbconvert --to html TikTok_Snapchat_Business_Analysis.ipynb
```

## 🌐 Project Website

A live project website provides a visual overview of the analysis, key statistical results, platform comparison, and business findings.

**Live website:** [View the live project website](https://ayaa137.github.io/TikTok-Snapchat-Digital-Business-Analysis/)

## ⚠️ Limitations

The TikTok dataset provides substantially richer content-level information than the Snapchat comparison data.

The project does not include several variables that could provide deeper insight into platform performance, including:

- User demographics
- Advertising revenue
- Advertising campaign outcomes
- Watch time
- Recommendation source
- Creator category
- Creator follower count
- Platform profitability

The available cross-platform dataset also provides only a limited set of comparable behavioral variables.

Therefore, the findings should be interpreted as **descriptive business analysis supported by statistical evidence**, rather than causal or predictive evidence.

## 👩‍💻 Authors

**Aya Abdine**  
**Meriam El Askri**  
**Ghofran Mahmoud**

Digital Business Models and Functions  
Constructor University
