import argparse
import os
import sys
import timeit
import datetime
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer
import pymia.evaluation.evaluator as eval_

# Import mialab modules with error handling
try:
    import mialab.data.structure as structure
    import mialab.utilities.file_access_utilities as futil
    import mialab.utilities.pipeline_utilities as putil
except ImportError:
    # Append the MIALab root directory to Python path if not found
    sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '..'))
    import mialab.data.structure as structure
    import mialab.utilities.file_access_utilities as futil
    import mialab.utilities.pipeline_utilities as putil

# Define LOADING_KEYS to specify which image types to load
LOADING_KEYS = [
    structure.BrainImageTypes.T1w,
    structure.BrainImageTypes.T2w,
    structure.BrainImageTypes.GroundTruth,
    structure.BrainImageTypes.BrainMask,
    structure.BrainImageTypes.RegistrationTransform
]

# Define fixed paths as in pipeline.py
DEFAULT_ATLAS_DIR = "../mialab/data/atlas"
DEFAULT_TRAIN_DIR = "../mialab/data/train"
DEFAULT_TEST_DIR = "../mialab/data/test"

# Custom scoring functions for GridSearch
def dice_score(y_true, y_pred):
    evaluator = putil.init_evaluator()
    evaluator.evaluate(y_pred, y_true, "Dice")
    return evaluator.results["Dice"]

def hausdorff_score(y_true, y_pred):
    evaluator = putil.init_evaluator()
    evaluator.evaluate(y_pred, y_true, "Hausdorff")
    return evaluator.results["Hausdorff"]

# Scorers dictionary
scoring = {'Dice': make_scorer(dice_score, greater_is_better=True),
           'Hausdorff': make_scorer(hausdorff_score, greater_is_better=False)}

def main(result_dir: str):
    # Results directory with timestamp
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    result_dir = os.path.join(result_dir, f'doe_results_{timestamp}')
    os.makedirs(result_dir, exist_ok=True)

    # Load atlas images
    putil.load_atlas_images(DEFAULT_ATLAS_DIR)

    # Set up data crawler and pre-process training data
    crawler = futil.FileSystemDataCrawler(
        DEFAULT_TRAIN_DIR, LOADING_KEYS, futil.BrainImageFilePathGenerator(), futil.DataDirectoryFilter()
    )
    pre_process_params = {
        'skullstrip_pre': True,
        'normalization_pre': True,
        'registration_pre': True,
        'coordinates_feature': True,
        'intensity_feature': True,
        'gradient_intensity_feature': True
    }
    images = putil.pre_process_batch(crawler.data, pre_process_params, multi_process=True)
    data_train = np.concatenate([img.feature_matrix[0] for img in images])
    labels_train = np.concatenate([img.feature_matrix[1] for img in images]).squeeze()

    # Parameter grid for GridSearch
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [10, 20, None],
        'max_features': ['sqrt', 'log2'],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2]
    }

    # Set up GridSearchCV
    forest = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(
        estimator=forest,
        param_grid=param_grid,
        scoring=scoring,
        refit='Dice',  # Use Dice score to select best model
        cv=3,  # 3-fold cross-validation
        verbose=2,
        n_jobs=-1
    )
    # Use Hausdorff to select the best parameters
    

    # Run the grid search
    print("Starting Grid Search...")
    start_time = timeit.default_timer()
    grid_search.fit(data_train, labels_train)
    print("Grid Search Time elapsed:", timeit.default_timer() - start_time, "s")

    # Save grid search results
    results_df = pd.DataFrame(grid_search.cv_results_)
    results_file = os.path.join(result_dir, 'grid_search_results.csv')
    results_df.to_csv(results_file, index=False)
    print(f"Grid search results saved to {results_file}")

    # Save best parameters and best score
    best_params = grid_search.best_params_
    best_score = grid_search.best_score_
    print("Best Parameters:", best_params)
    print("Best Score (Dice):", best_score)

    with open(os.path.join(result_dir, 'best_params.txt'), 'w') as f:
        f.write(f"Best Parameters: {best_params}\n")
        f.write(f"Best Score (Dice): {best_score}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Grid search for Random Forest parameters in a medical image analysis pipeline')

    parser.add_argument(
        '--result_dir',
        type=str,
        default='./mia-doe-results',
        help='Directory for results.'
    )

    args = parser.parse_args()
    main(args.result_dir)
