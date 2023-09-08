🔍 Credit Card Fraud Detection with Machine Learning
In this project, I performed an in-depth analysis of a fraud detection dataset using Python and machine learning techniques. Here's a concise overview of the key steps and findings:

📊 Data Preparation:
Imported necessary libraries like Pandas, NumPy, and Seaborn for data analysis and visualization.

Loaded the dataset from Kaggle on fraud detection and merged the training and testing data.
Explored the dataset, checking for duplicates, missing values, and data types.

📈 Exploratory Data Analysis:
Created visualizations to understand correlations between features using heatmap.
Explored feature distributions, such as state, category, and gender, through count plots.
Examined the distribution of fraudulent transactions.

🔍 Data Preprocessing:
Derived a new feature "age" from transaction date and birth date.
Balanced the dataset by downsampling the majority class.

📊 Visualizing Preprocessed Data:
Visualized the balanced data using count plots and age distribution histogram.
Investigated the relationship between gender and fraud, and category and fraud.

🛠️ Feature Engineering and Model Building:
Processed the data by encoding categorical features using LabelEncoder.
Selected key features for prediction while dropping less relevant ones.
Split the data into training and testing sets and applied feature scaling.

🧠 Model Training and Evaluation:
Trained three different models: Logistic Regression, Support Vector Machine, and Naive Bayes.
Evaluated each model's performance using confusion matrices, accuracy, and classification reports.
Employed cross-validation to assess model consistency.

📊 Results:
Logistic Regression, Support Vector Machine, and Naive Bayes models were trained and evaluated.
Models achieved a notable accuracy level on testing data.
Cross-validation demonstrated consistent performance across different folds.
