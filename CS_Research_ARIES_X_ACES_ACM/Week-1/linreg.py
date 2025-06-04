import numpy as np
import matplotlib.pyplot as plt

def linearRegression(X: np.array, Y: np.array, lr: float, lambda_: float, epochs: int = 1000):
    """
    Parameters:
    - X: Input feature matrix (NumPy array)
    - Y: Target vector (NumPy array)
    - lr: Learning rate (float)
    - lambda_: L1 regularization coefficient (float)
    - epochs: Number of iterations for gradient descent

    Returns:
    - weights: Learned model parameters
    """

    # Add a bias term (column of ones) to the input feature matrix
    X = np.hstack((np.ones((X.shape[0], 1)), X))
    weights = np.zeros(X.shape[1])
    cost_history = []

    for epoch in range(epochs):
        # Compute model prediction and errors
        predictions = X @ weights
        errors = predictions - Y

        # Compute MSE and regularization error. Add them up to find the total cost.
        mse = (1 / (2 * X.shape[0])) * np.sum(errors ** 2)
        l1_penalty = lambda_ * np.sum(np.abs(weights[1:]))
        cost = mse + l1_penalty
        cost_history.append(cost)

        # Print cost every 100 iterations.
        if epoch % 100 == 0 or epoch == epochs - 1:
            print(f"Epoch {epoch}: Cost = {cost}")

        # Gradient of Mean Squared Error and add L1 regularization gradient (subgradient)
        gradient = (1 / X.shape[0]) * (X.T @ errors)
        l1_gradient = lambda_ * np.sign(weights)
        l1_gradient[0] = 0

        # Update weights
        weights -= lr * (gradient + l1_gradient)

    # Plotting cost vs epoch graph
    # plt.figure(figsize=(8, 5))
    # plt.plot(range(epochs), cost_history, label='Cost')
    # plt.xlabel("Epoch")
    # plt.ylabel("Cost")
    # plt.title("Cost vs Epoch")
    # plt.grid(True)
    # plt.legend()
    # plt.tight_layout()
    # plt.show()
    return weights

# Dummy data to check function, should print [1,2] as weights for y=2x+1 equation
# X = np.array([[2], [4]])
# Y = np.array([5, 9])
# lr = 0.1
# lambda_ = 0
# epochs = 1000
# weights = linearRegression(X, Y, lr, lambda_, epochs)
# print(weights)