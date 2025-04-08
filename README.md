## Intro

This project is a demonstration version of a two-stage recommendation system. At this stage of implementation, a significant number of functional features planned for implementation are missing. These include, among other things, solving the cold start problem, adjusting user features, and similar tasks.

## Installation

To ensure correct operation of the system, perform the following sequence of actions:
```
1. download h&m dataset
2. docker compose up postgres, mlflow, minio
3. run files prepare_data.ipynb, train.ipynb
4. upload images to minio s3
5. docker compose up -d
```

## User Interface

A compact web application based on React has been developed for visual assessment of recommendations. The interaction process with the web application is presented in the GIF: <img src="interaction.gif" style="border-radius:15px">

## Algorithm

The operation of the recommendation system is based on the following algorithm:
```
First model -> Selection of candidates from the general set of objects.
Second model -> Ranking of selected candidates.
```

- The first model is based on the Alternating Least Squares (ALS) method for implicit factorization.

- The second model uses gradient boosting implemented by the CatBoost library.

## Model`s Training

TODO: description about first-stage/second-stage metrics, data.