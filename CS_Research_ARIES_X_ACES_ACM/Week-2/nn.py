import numpy as np
from sklearn.datasets import fetch_openml

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    s = sigmoid(x)
    return s * (1 - s)

def relu(x):
    return np.maximum(0, x)

def relu_derivative(x):
    return (x > 0).astype(float)

def softmax(x):
    e_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return e_x / e_x.sum(axis=1, keepdims=True)

def cross_entropy(y_pred, y_true):
    m = y_pred.shape[0]
    p = y_pred[range(m), y_true]
    return -np.mean(np.log(p + 1e-8))

def cross_entropy_derivative(y_pred, y_true):
    m = y_pred.shape[0]
    grad = y_pred.copy()
    grad[range(m), y_true] -= 1
    return grad / m

class SimpleNN:
    def __init__(self, input_size, hidden_size, output_size):
        self.W1 = np.random.randn(input_size, hidden_size) * 0.01
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * 0.01
        self.b2 = np.zeros((1, output_size))

    def forward(self, X):
        self.Z1 = X @ self.W1 + self.b1
        self.A1 = relu(self.Z1)
        self.Z2 = self.A1 @ self.W2 + self.b2
        self.A2 = softmax(self.Z2)
        return self.A2

    def backward(self, X, y, output):
        m = X.shape[0]
        dZ2 = cross_entropy_derivative(output, y)
        dW2 = self.A1.T @ dZ2
        db2 = np.sum(dZ2, axis=0, keepdims=True)

        dA1 = dZ2 @ self.W2.T
        dZ1 = dA1 * relu_derivative(self.Z1)
        dW1 = X.T @ dZ1
        db1 = np.sum(dZ1, axis=0, keepdims=True)

        lr = 0.1
        self.W1 -= lr * dW1
        self.b1 -= lr * db1
        self.W2 -= lr * dW2
        self.b2 -= lr * db2

    def train(self, X, y, epochs=1000):
        for epoch in range(epochs):
            output = self.forward(X)
            loss = cross_entropy(output, y)
            self.backward(X, y, output)

            if epoch % 100 == 0:
                acc = np.mean(np.argmax(output, axis=1) == y)
                print(f"Epoch {epoch}, Loss: {loss:.4f}, Accuracy: {acc:.4f}")

    def predict(self, X):
        return np.argmax(self.forward(X), axis=1)

X, y = fetch_openml("Fashion-MNIST", version=1, return_X_y=True, as_frame=False)
X = X / 255.0  # normalize
y = y.astype(int)

X_train, y_train = X[:1000], y[:1000]
X_test, y_test = X[60000:60300], y[60000:60300]

model = SimpleNN(input_size=784, hidden_size=64, output_size=10)
model.train(X_train, y_train, epochs=2500)

test_preds = model.predict(X_test)
test_acc = np.mean(test_preds == y_test)
print(f"\nTest Accuracy: {test_acc:.4f}")