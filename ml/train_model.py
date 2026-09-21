import pandas as pd
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

BASE_DIR = "C:/Users/RAMYA VARSHI/.gemini/antigravity/scratch/AI_Diet_System"
DATA_PATH = os.path.join(BASE_DIR, "data", "diet_dataset.csv")
ML_DIR = os.path.join(BASE_DIR, "ml")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

os.makedirs(ML_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

def train_and_evaluate():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found at: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    print(f"Loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns.")

    feature_cols = [
        "Age", "Gender", "Height", "Weight", "BMI", "ActivityLevel", "Occupation",
        "FitnessGoal", "MedicalCondition", "FoodAllergy", "DietaryPreference",
        "DailyWaterIntake_L", "Sleep_Hours", "DailySteps", "StressLevel",
        "SmokingStatus", "AlcoholConsumption"
    ]
    target_col = "DietCategory"

    X = df[feature_cols]
    y = df[target_col]

    categorical_cols = [
        "Gender", "ActivityLevel", "Occupation", "FitnessGoal", "MedicalCondition",
        "FoodAllergy", "DietaryPreference", "StressLevel", "SmokingStatus", "AlcoholConsumption"
    ]
    numerical_cols = [
        "Age", "Height", "Weight", "BMI", "DailyWaterIntake_L", "Sleep_Hours", "DailySteps"
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numerical_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_cols)
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    classes = np.unique(y)
    print(f"Target classes ({len(classes)}): {classes}")

    rf_clf = RandomForestClassifier(n_estimators=150, max_depth=12, random_state=42)
    rf_pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("classifier", rf_clf)])
    rf_pipeline.fit(X_train, y_train)
    rf_preds = rf_pipeline.predict(X_test)

    rf_acc = accuracy_score(y_test, rf_preds)
    rf_prec = precision_score(y_test, rf_preds, average="weighted", zero_division=0)
    rf_rec = recall_score(y_test, rf_preds, average="weighted", zero_division=0)
    rf_f1 = f1_score(y_test, rf_preds, average="weighted", zero_division=0)

    print("\n--- Random Forest Results ---")
    print(f"Accuracy: {rf_acc:.4f} | Precision: {rf_prec:.4f} | Recall: {rf_rec:.4f} | F1-Score: {rf_f1:.4f}")

    gb_clf = GradientBoostingClassifier(n_estimators=120, learning_rate=0.1, max_depth=5, random_state=42)
    gb_pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("classifier", gb_clf)])
    gb_pipeline.fit(X_train, y_train)
    gb_preds = gb_pipeline.predict(X_test)

    gb_acc = accuracy_score(y_test, gb_preds)
    gb_prec = precision_score(y_test, gb_preds, average="weighted", zero_division=0)
    gb_rec = recall_score(y_test, gb_preds, average="weighted", zero_division=0)
    gb_f1 = f1_score(y_test, gb_preds, average="weighted", zero_division=0)

    print("\n--- Gradient Boosting Results ---")
    print(f"Accuracy: {gb_acc:.4f} | Precision: {gb_prec:.4f} | Recall: {gb_rec:.4f} | F1-Score: {gb_f1:.4f}")

    if gb_acc >= rf_acc:
        best_pipeline = gb_pipeline
        best_name = "Gradient Boosting"
        best_acc = gb_acc
        best_preds = gb_preds
    else:
        best_pipeline = rf_pipeline
        best_name = "Random Forest"
        best_acc = rf_acc
        best_preds = rf_preds

    print(f"\nBest Model Selected: {best_name} (Accuracy: {best_acc:.4f})")

    model_data = {
        "pipeline": best_pipeline,
        "classes": list(classes),
        "feature_names": feature_cols,
        "categorical_cols": categorical_cols,
        "numerical_cols": numerical_cols,
        "results": {
            "Random Forest": {"Accuracy": rf_acc, "Precision": rf_prec, "Recall": rf_rec, "F1": rf_f1},
            "Gradient Boosting": {"Accuracy": gb_acc, "Precision": gb_prec, "Recall": gb_rec, "F1": gb_f1}
        }
    }

    model_pkl_ml = os.path.join(ML_DIR, "model.pkl")
    model_pkl_root = os.path.join(BASE_DIR, "model.pkl")
    joblib.dump(model_data, model_pkl_ml)
    joblib.dump(model_data, model_pkl_root)
    print(f"Saved model pipeline to {model_pkl_ml} and {model_pkl_root}")

    # Generate Evaluation Charts
    plt.style.use('dark_background')

    # Chart 1: Model Comparison Bar Chart
    plt.figure(figsize=(8, 5))
    metrics_df = pd.DataFrame({
        "Metric": ["Accuracy", "Precision", "Recall", "F1-Score"] * 2,
        "Value": [rf_acc, rf_prec, rf_rec, rf_f1, gb_acc, gb_prec, gb_rec, gb_f1],
        "Model": ["Random Forest"] * 4 + ["Gradient Boosting"] * 4
    })
    sns.barplot(data=metrics_df, x="Metric", y="Value", hue="Model", palette=["#00E5FF", "#00E676"])
    plt.title("ML Performance Benchmarks", fontsize=14, pad=12, color="#00E676")
    plt.ylim(0.85, 1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(ASSETS_DIR, "model_comparison.png"), dpi=200)
    plt.close()

    # Chart 2: Confusion Matrix Heatmap
    plt.figure(figsize=(10, 8))
    cm = confusion_matrix(y_test, best_preds)
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=classes, yticklabels=classes)
    plt.title(f"Confusion Matrix — {best_name}", fontsize=14, pad=12, color="#00E676")
    plt.xlabel("Predicted Category")
    plt.ylabel("True Category")
    plt.tight_layout()
    plt.savefig(os.path.join(ASSETS_DIR, "confusion_matrix.png"), dpi=200)
    plt.close()

    # Chart 3: Feature Importances
    plt.figure(figsize=(10, 6))
    clf_model = best_pipeline.named_steps["classifier"]
    ohe_cols = list(best_pipeline.named_steps["preprocessor"].named_transformers_["cat"].get_feature_names_out(categorical_cols))
    all_feature_names = numerical_cols + ohe_cols

    if hasattr(clf_model, "feature_importances_"):
        importances = clf_model.feature_importances_
        imp_df = pd.DataFrame({"Feature": all_feature_names, "Importance": importances})
        top_imp = imp_df.sort_values(by="Importance", ascending=False).head(15)

        sns.barplot(data=top_imp, x="Importance", y="Feature", palette="mako")
        plt.title(f"Top 15 Feature Importances ({best_name})", fontsize=14, pad=12, color="#00E676")
        plt.tight_layout()
        plt.savefig(os.path.join(ASSETS_DIR, "feature_importance.png"), dpi=200)
        plt.close()

    print("Saved evaluation charts to assets/ directory.")

if __name__ == "__main__":
    train_and_evaluate()
