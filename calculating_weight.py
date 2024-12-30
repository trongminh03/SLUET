import numpy as np

def softmax(x):
    """Computes the softmax of a vector."""
    exp_x = np.exp(x - np.max(x))  # Subtract max(x) for numerical stability
    return exp_x / np.sum(exp_x)

def get_weights_from_accuracy(accuracies):
    """
    Calculate weights for ensembling based on model accuracies using softmax.
    
    Args:
    accuracies (list): List of model accuracies. Each element represents the accuracy of a single model.
    
    Returns:
    list: Normalized weights for each model based on their accuracies using softmax.
    """
    
    # Convert accuracies to numpy array
    accuracies = np.array(accuracies)
    
    # Apply softmax to get normalized weights
    weights = softmax(accuracies)
    
    return weights.tolist()

# Example usage
accuracies = [77.84, 77.53, 78.06]  # Example models with very close accuracies
weights = get_weights_from_accuracy(accuracies)
print("Softmax Normalized Weights: ", weights)
