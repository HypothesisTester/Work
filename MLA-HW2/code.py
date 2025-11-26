import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    roc_curve, roc_auc_score,
    confusion_matrix, classification_report
)

import matplotlib.pyplot as plt

# ---------------------------------
# 1. Load data & basic preprocessing
# ---------------------------------

df = pd.read_csv("MLA-HW2/heart_data.csv")

# Target: 1 = at risk (heart disease present), 0 = not at risk
y = (df["Class"] == 2).astype(int)

# Features: all columns except Class
X = df.drop(columns=["Class"])

feature_names = X.columns.tolist()

# Optional: binary recoding if needed (example only – adjust if your coding differs)
# for col in ["Sex", "FastingBloodSugar", "ExerciseInduced"]:
#     X[col] = (X[col] == 2).astype(int)

# Train/test split with stratification
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# Common CV splitter
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# ==================================================
# 2. Logistic Regression: fit, evaluate, make graphs
# ==================================================

logit_pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("logit", LogisticRegression(max_iter=1000, solver="lbfgs"))
])

# Cross-validated performance on training data
logit_cv_auc = cross_val_score(
    logit_pipe, X_train, y_train,
    cv=cv, scoring="roc_auc"
)
logit_cv_acc = cross_val_score(
    logit_pipe, X_train, y_train,
    cv=cv, scoring="accuracy"
)

print(f"Logistic CV AUC: mean={logit_cv_auc.mean():.3f}, std={logit_cv_auc.std():.3f}")
print(f"Logistic CV ACC: mean={logit_cv_acc.mean():.3f}, std={logit_cv_acc.std():.3f}")

# Fit on full training set
logit_pipe.fit(X_train, y_train)

# Test-set predictions & probabilities
y_proba_logit = logit_pipe.predict_proba(X_test)[:, 1]
y_pred_logit = (y_proba_logit >= 0.5).astype(int)

# Test metrics
print("\nLogistic Regression – Test metrics")
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred_logit))
print(classification_report(y_test, y_pred_logit, digits=3))

logit_test_auc = roc_auc_score(y_test, y_proba_logit)
print(f"Logistic Test AUC: {logit_test_auc:.3f}")

# 2.1 ROC curve for logistic regression
fpr_logit, tpr_logit, _ = roc_curve(y_test, y_proba_logit)

plt.figure(figsize=(6, 5))
plt.plot(fpr_logit, tpr_logit, label=f"Logistic (AUC = {logit_test_auc:.2f})")
plt.plot([0, 1], [0, 1], "k--", alpha=0.5)
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve – Logistic Regression")
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig("logistic_roc.png", dpi=300)
plt.close()

# 2.2 Odds ratios plot (from logistic coefficients)

# Extract coefficients and compute ORs
logit = logit_pipe.named_steps["logit"]
# The scaler standardises features, so the coefficients are for scaled units.
# Still useful to see relative importance.
coefs = logit.coef_[0]
odds_ratios = np.exp(coefs)

# Sort by |log(OR)| for nicer plot
order = np.argsort(np.abs(np.log(odds_ratios)))[::-1]
sorted_features = np.array(feature_names)[order]
sorted_or = odds_ratios[order]

plt.figure(figsize=(7, 5))
y_pos = np.arange(len(sorted_features))
plt.barh(y_pos, sorted_or)
plt.yticks(y_pos, sorted_features)
plt.axvline(1.0, color="k", linestyle="--", linewidth=1)
plt.xlabel("Odds Ratio (per 1 SD increase in predictor)")
plt.title("Logistic Regression – Odds Ratios")
plt.gca().invert_yaxis()  # highest at top
plt.tight_layout()
plt.savefig("logistic_odds_ratios.png", dpi=300)
plt.close()

# 2.3 Confusion-matrix heatmap for logistic regression
cm_logit = confusion_matrix(y_test, y_pred_logit)

plt.figure(figsize=(5, 4))
plt.imshow(cm_logit, interpolation="nearest", cmap="Blues")
plt.title("Logistic Regression – Confusion Matrix (Test Set)")
plt.colorbar(label="Number of patients")

classes = ["No disease", "Disease"]
tick_marks = np.arange(len(classes))
plt.xticks(tick_marks, classes, rotation=0)
plt.yticks(tick_marks, classes)

# Add counts in each cell
thresh = cm_logit.max() / 2.0
for i in range(cm_logit.shape[0]):
    for j in range(cm_logit.shape[1]):
        plt.text(
            j, i, cm_logit[i, j],
            ha="center", va="center",
            color="white" if cm_logit[i, j] > thresh else "black",
            fontsize=10,
        )

plt.ylabel("True label")
plt.xlabel("Predicted label")
plt.tight_layout()
plt.savefig("logistic_confusion_matrix.png", dpi=300)
plt.close()

# 2.4 Predicted probability distributions by true class (logistic)
# y_proba_logit: predicted probability of heart disease (Class = 2)

proba_no_disease = y_proba_logit[y_test == 0]
proba_disease = y_proba_logit[y_test == 1]

plt.figure(figsize=(5.5, 4.5))
plt.boxplot(
    [proba_no_disease, proba_disease],
    labels=["No disease", "Disease"],
    showmeans=True
)
plt.axhline(0.5, linestyle="--", linewidth=1, color="k", alpha=0.7)
plt.ylabel("Predicted probability of heart disease")
plt.title("Logistic Regression – Predicted Risk by True Class")
plt.ylim(-0.05, 1.05)
plt.tight_layout()
plt.savefig("logistic_predicted_probabilities.png", dpi=300)
plt.close()

# =================================================
# 3. k-Nearest Neighbours: tuning, evaluation, plots
# =================================================

knn_pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("knn", KNeighborsClassifier())
])

# Grid of k values (odd numbers 1–25)
param_grid = {
    "knn__n_neighbors": list(range(1, 26, 2))
}

grid = GridSearchCV(
    knn_pipe,
    param_grid=param_grid,
    cv=cv,
    scoring="roc_auc",
    n_jobs=-1,
    refit=True
)

grid.fit(X_train, y_train)

print("\nBest k for kNN (by CV AUC):", grid.best_params_)
print("Best CV AUC for kNN:", grid.best_score_)

# Extract CV results for plotting
cv_results = grid.cv_results_
k_values = cv_results["param_knn__n_neighbors"].data
mean_auc = cv_results["mean_test_score"]

# 3.1 Plot CV performance vs k
plt.figure(figsize=(6, 5))
plt.plot(k_values, mean_auc, marker="o")
plt.xlabel("Number of Neighbours (k)")
plt.ylabel("Mean CV AUC")
plt.title("kNN – Cross-validated AUC vs k")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("knn_cv_auc_vs_k.png", dpi=300)
plt.close()

# 3.2 Test-set performance for best kNN
best_knn_pipe = grid.best_estimator_

y_proba_knn = best_knn_pipe.predict_proba(X_test)[:, 1]
y_pred_knn = (y_proba_knn >= 0.5).astype(int)

print("\nkNN – Test metrics (best k)")
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred_knn))
print(classification_report(y_test, y_pred_knn, digits=3))

knn_test_auc = roc_auc_score(y_test, y_proba_knn)
print(f"kNN Test AUC: {knn_test_auc:.3f}")


# 3.3 Confusion-matrix heatmap for kNN (best k)
cm_knn = confusion_matrix(y_test, y_pred_knn)

plt.figure(figsize=(5, 4))
plt.imshow(cm_knn, interpolation="nearest", cmap="Blues")
plt.title(f"kNN (k={grid.best_params_['knn__n_neighbors']}) – Confusion Matrix (Test Set)")
plt.colorbar(label="Number of patients")

classes = ["No disease", "Disease"]
tick_marks = np.arange(len(classes))
plt.xticks(tick_marks, classes)
plt.yticks(tick_marks, classes)

# Add counts in each cell
thresh = cm_knn.max() / 2.0
for i in range(cm_knn.shape[0]):
    for j in range(cm_knn.shape[1]):
        plt.text(
            j, i, cm_knn[i, j],
            ha="center", va="center",
            color="white" if cm_knn[i, j] > thresh else "black",
            fontsize=10,
        )

plt.ylabel("True label")
plt.xlabel("Predicted label")
plt.tight_layout()
plt.savefig("knn_confusion_matrix.png", dpi=300)
plt.close()

# 3.4 Predicted probability distributions by true class (kNN)
# y_proba_knn: predicted probability of heart disease (Class = 2)

proba_no_disease_knn = y_proba_knn[y_test == 0]
proba_disease_knn = y_proba_knn[y_test == 1]

plt.figure(figsize=(5.5, 4.5))
plt.boxplot(
    [proba_no_disease_knn, proba_disease_knn],
    labels=["No disease", "Disease"],  # use tick_labels if you want to silence the warning in newer matplotlib
    showmeans=True
)
plt.axhline(0.5, linestyle="--", linewidth=1, color="k", alpha=0.7)
plt.ylabel("Predicted probability of heart disease")
plt.title(f"kNN (k={grid.best_params_['knn__n_neighbors']}) – Predicted Risk by True Class")
plt.ylim(-0.05, 1.05)
plt.tight_layout()
plt.savefig("knn_predicted_probabilities.png", dpi=300)
plt.close()

# ROC curve for kNN
fpr_knn, tpr_knn, _ = roc_curve(y_test, y_proba_knn)

plt.figure(figsize=(6, 5))
plt.plot(fpr_logit, tpr_logit, label=f"Logistic (AUC = {logit_test_auc:.2f})")
plt.plot(fpr_knn, tpr_knn, label=f"kNN (k={grid.best_params_['knn__n_neighbors']}, AUC = {knn_test_auc:.2f})")
plt.plot([0, 1], [0, 1], "k--", alpha=0.5)
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curves – Logistic vs kNN")
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig("logistic_vs_knn_roc.png", dpi=300)
plt.close()