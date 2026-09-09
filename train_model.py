import pandas as pd
import numpy as np
import os
import joblib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

def train_and_evaluate():
    base_dir = "C:/Users/RAMYA VARSHI/.gemini/antigravity/scratch/AI_Diet_System"
    dataset_path = os.path.join(base_dir, "diet_dataset.csv")
    assets_dir = os.path.join(base_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset not found at {dataset_path}")
        return
        
    df = pd.read_csv(dataset_path)
    
    feature_cols = [
        "Age", "Gender", "Height", "Weight", "BMI", "ActivityLevel", "Occupation",
        "FitnessGoal", "MedicalCondition", "FoodAllergy", "DietaryPreference",
        "DailyWaterIntake_L", "Sleep_Hours", "DailySteps", "StressLevel",
        "SmokingStatus", "AlcoholConsumption"
    ]
    target_col = "DietCategory"
    
    X = df[feature_cols]
    y = df[target_col]
    
    classes = sorted(y.unique().tolist())
    class_map = {cls: idx for idx, cls in enumerate(classes)}
    y_encoded = y.map(class_map)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)
    
    numeric_features = ["Age", "Height", "Weight", "BMI", "DailyWaterIntake_L", "Sleep_Hours", "DailySteps"]
    categorical_features = [
        "Gender", "ActivityLevel", "Occupation", "FitnessGoal", "MedicalCondition",
        "FoodAllergy", "DietaryPreference", "StressLevel", "SmokingStatus", "AlcoholConsumption"
    ]
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
        
    models = {
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=42)
    }
    
    results = {}
    best_acc = 0
    best_model_name = None
    best_pipeline = None
    
    for name, clf in models.items():
        pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                   ('classifier', clf)])
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted', zero_division=0)
        
        results[name] = {
            "Accuracy": acc,
            "Precision": precision,
            "Recall": recall,
            "F1-Score": f1,
            "Pipeline": pipeline,
            "Preds": y_pred
        }
        
        print(f"--- {name} Results ---")
        print(f"Accuracy: {acc:.4f} | Precision: {precision:.4f} | Recall: {recall:.4f} | F1-Score: {f1:.4f}\n")
        
        if acc >= best_acc:
            best_acc = acc
            best_model_name = name
            best_pipeline = pipeline

    print(f"Best Model Selected: {best_model_name} (Accuracy: {best_acc:.4f})")
    
    # Save model and metadata
    model_data = {
        "pipeline": best_pipeline,
        "classes": classes,
        "results": {name: {k: v for k, v in metrics.items() if k not in ["Pipeline", "Preds"]} for name, metrics in results.items()},
        "feature_cols": feature_cols,
        "categorical_cols": categorical_features,
        "numeric_cols": numeric_features
    }
    joblib.dump(model_data, os.path.join(base_dir, "model.pkl"))
    print("Model saved to model.pkl successfully.")
    
    # 1. Model Comparison Chart
    plt.figure(figsize=(8, 5))
    metrics_names = ["Accuracy", "Precision", "Recall", "F1-Score"]
    rf_scores = [results["Random Forest"][m] for m in metrics_names]
    gb_scores = [results["Gradient Boosting"][m] for m in metrics_names]
    
    x = np.arange(len(metrics_names))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(x - width/2, rf_scores, width, label='Random Forest', color='#00E676')
    ax.bar(x + width/2, gb_scores, width, label='Gradient Boosting', color='#00E5FF')
    
    ax.set_ylabel('Scores')
    ax.set_title('Algorithm Performance Comparison (2,500 Records)')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics_names)
    ax.set_ylim(0, 1.15)
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(assets_dir, "model_comparison.png"), dpi=150)
    plt.close()
    
    # 2. Confusion Matrix
    best_preds = results[best_model_name]["Preds"]
    cm = confusion_matrix(y_test, best_preds)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='viridis', xticklabels=classes, yticklabels=classes)
    plt.title(f'Confusion Matrix ({best_model_name})')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.tight_layout()
    plt.savefig(os.path.join(assets_dir, "confusion_matrix.png"), dpi=150)
    plt.close()
    
    # 3. Feature Importance
    ohe_features = best_pipeline.named_steps['preprocessor'].named_transformers_['cat'].get_feature_names_out(categorical_features)
    all_features = numeric_features + list(ohe_features)
    
    clf = best_pipeline.named_steps['classifier']
    importances = clf.feature_importances_
    
    feat_imp = pd.Series(importances, index=all_features).sort_values(ascending=False).head(15)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=feat_imp.values, y=feat_imp.index, hue=feat_imp.index, legend=False, palette='cool')
    plt.title('Top 15 Predictor Feature Importances')
    plt.xlabel('Importance Score')
    plt.ylabel('Features')
    plt.tight_layout()
    plt.savefig(os.path.join(assets_dir, "feature_importance.png"), dpi=150)
    plt.close()
    print("Evaluation charts saved to assets/ directory.")

if __name__ == "__main__":
    train_and_evaluate()
