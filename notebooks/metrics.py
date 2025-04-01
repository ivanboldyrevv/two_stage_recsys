import numpy as np


def recall(true, predicted):
    intersection = set(true).intersection(set(predicted))
    if not intersection:
        return 0
    return len(intersection) / len(true)


def recall_at_k(true, predicted, k=10):
    return recall(true, predicted[:k])


def precision(true, predicted):
    intersection = set(true).intersection(set(predicted))
    if not intersection:
        return 0
    return len(intersection) / len(predicted)


def precision_at_k(true, predicted, k=10):
    return precision(true, predicted[:k])


if __name__ == "__main__":
    true_positive_examples = np.array([1, 2, 3])
    predicted_positive_examples = np.array([1, 2, 4])

    expected_recall = 2 / 3
    computed_recall = recall(true_positive_examples, predicted_positive_examples)
    assert abs(expected_recall - computed_recall) < 1e-6

    expected_precision = 2 / 3
    computed_precision = precision(true_positive_examples, predicted_positive_examples)
    assert abs(expected_precision - computed_precision) < 1e-6

    true_negative_examples = np.array([])
    predicted_negative_examples = np.array([1, 2, 3])
    assert recall(true_negative_examples, predicted_negative_examples) == 0.0
    assert precision(true_negative_examples, predicted_negative_examples) == 0.0

    true_positive_examples = np.array([1, 2, 3, 4, 5])
    predicted_positive_examples = np.array([1, 4, 6, 7, 11])

    expected_recall_atk = 2 / 5
    computed_recall_atk = recall_at_k(true_positive_examples, predicted_positive_examples, 4)
    assert abs(expected_recall_atk - computed_recall_atk) < 1e-6

    expected_precision_atk = 1
    computed_precision_atk = precision_at_k(true_positive_examples, predicted_positive_examples, 2)
    assert abs(expected_precision_atk - computed_precision_atk) < 1e-6
