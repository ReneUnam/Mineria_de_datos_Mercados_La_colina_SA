def verify_installation():
    print("=" * 60)
    print("Verifying installation of required packages for the project...")
    print("=" * 60)

    errors = []

    #1. Python
    import sys
    print(f"\nPython: {sys.version}")

    #2. Pandas
    try:
        import pandas as pd
        print(f"✔ Pandas: {pd.__version__}")
    except ImportError:
        errors.append("pandas")

    #3. NumPy
    try:
        import numpy as np
        print(f"✔ NumPy: {np.__version__}")
    except ImportError:
        errors.append("numpy")

    #4. Matplotlib
    try:
        import matplotlib
        print(f"✔ Matplotlib:{matplotlib.__version__}")
    except ImportError:
        errors.append("matplotlib")

    #5. Skicit-learn
    try: 
        import sklearn
        print(f"✔ Skicit-learn: {sklearn.__version__}")
    except ImportError:
        errors.append("scikit-learn")

    #6. XGBoost
    try:
        import xgboost as xgb
        print(f"✔ XGBoost: {xgb.__version__}")
    except ImportError:
        errors.append("xgboost")

    #7. Seaborn
    try:
        import seaborn as sns
        print(f"✔ Seaborn: {sns.__version__}")
    except ImportError:
        errors.append("seaborn")

    #8. dotenv
    try:
        import dotenv
        print(f"✔ Python-dotenv: installed")
    except ImportError:
        errors.append("python-dotenv")

    #9. SQLAlchemy
    try:
        import sqlalchemy
        print(f"✔ SQLAlchemy: {sqlalchemy.__version__}")
    except ImportError:
        errors.append("sqlalchemy")

    #10. lightgbm
    try:
        import lightgbm as lgb
        print(f"✔ LightGBM: {lgb.__version__}")
    except ImportError:
        errors.append("lightgbm")

    #11. mxltend
    try:
        import mlxtend
        print(f"✔ mlxtend: {mlxtend.__version__}")
    except ImportError:
        errors.append("mlxtend")

    #12 . psycopg
    try:
        import psycopg
        print(f"✔ psycopg: {psycopg.__version__}")
    except ImportError:
        errors.append("psycopg")

    #Resume
    print("\n" + "=" * 60)
    if errors: 
        print(f"✖ There are {len(errors)} missing packages: {', '.join(errors)}")
        print(f" Please install the missing packages using pip install {' '.join(errors)}")
    else: 
        print("✔ All required packages are installed.")
    print("=" * 60)


verify_installation() 