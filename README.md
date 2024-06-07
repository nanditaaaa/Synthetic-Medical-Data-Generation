# Synthetic Medical Data Generation

## Overview

This project focuses on generating synthetic medical data to enhance predictive modeling in healthcare, specifically for diabetes prediction. By utilizing Generative Adversarial Networks (GANs) with attention layers and data augmentation techniques, the project aims to address the scarcity of labeled healthcare data and improve the accuracy of predictive models.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Results and Analysis](#results-and-analysis)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features

- **GAN with Attention Layer**: Generates synthetic medical data.
- **Data Augmentation**: Enhances the synthetic dataset to improve model performance.
- **Predictive Modeling**: Implements logistic regression, random forest, and Gaussian process classifiers for diabetes prediction.
- **Deployment**: Flask application setup for deploying the predictive model.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/nanditaaaa/Synthetic-Medical-Data-Generation.git
    cd Synthetic-Medical-Data-Generation
    ```

2. **Create and activate a virtual environment** (optional but recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Training the Model**:
    Run the script to train the GAN and generate synthetic data:
    ```sh
    python train_gan.py
    ```

2. **Augmenting Data**:
    Run the script to augment the synthetic data:
    ```sh
    python augment_data.py
    ```

3. **Predicting Diabetes**:
    Run the script to train predictive models and evaluate performance:
    ```sh
    python predict_diabetes.py
    ```

4. **Deploying the Application**:
    Set up and run the Flask application locally:
    ```sh
    python app.py
    ```
    Access the application at `http://127.0.0.1:5000/`.

## Project Structure

```
Synthetic-Medical-Data-Generation/
├── README.md
├── app.py
├── templates/
│   ├── diab.py
│   ├── app.yaml
│   ├── requirements.txt
│   ├── Diabetes.csv
│   └── index.html
```

- **README.md**: This file.
- **app.py**: Flask application script.
- **templates/**: Directory containing application files.
  - **diab.py**: Script for diabetes prediction.
  - **app.yaml**: Configuration file for deployment.
  - **requirements.txt**: List of dependencies.
  - **Diabetes.csv**: Dataset used for the project.
  - **index.html**: HTML template for the web application.

## Results and Analysis

Detailed analysis of the models' performance on the augmented synthetic dataset can be found in the `results` directory. This includes performance metrics and comparison of different models.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or new features.


