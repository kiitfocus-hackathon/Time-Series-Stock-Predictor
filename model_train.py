import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from sklearn.metrics import mean_squared_error
from math import sqrt

def load_data(filename):
    stock_data = pd.read_csv(filename)
    stock_data = stock_data[50:]
    return stock_data

def preprocess_data(stock_data):
    # Extract necessary features
    X = stock_data[['close', '20ma', 'rsi']].values
    y = stock_data['close'].values
    
    # Normalize features and target variable
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    y_scaled = scaler.fit_transform(y.reshape(-1, 1))
    
    return X_scaled, y_scaled

def create_sequences(X, y, time_steps=1):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        Xs.append(X[i:(i + time_steps)])
        ys.append(y[i + time_steps])
    return np.array(Xs), np.array(ys)

def build_model(X_train):
    model = tf.keras.Sequential([
        tf.keras.layers.LSTM(64, input_shape=(X_train.shape[1], X_train.shape[2])),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(1, activation='linear')
    ])
    
    model.compile(optimizer='adam', loss='mse')
    
    return model

def train_model(X_train, y_train):
    model = build_model(X_train)
    
    model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=0)
    
    return model

def make_predictions(model, X_test):
    y_pred = model.predict(X_test)
    
    return y_pred

def evaluate_model(y_test, y_pred):
    mse = mean_squared_error(y_test, y_pred)
    rmse = sqrt(mse)
    accuracy = (1 - (rmse / np.mean(y_test))) * 100
    print('MSE: %.3f' % mse)
    print('RMSE: %.3f' % rmse)
    return accuracy

def predict(filename):
    df = load_data(filename)
    
    # Preprocess data and create sequences
    X_scaled, y_scaled = preprocess_data(df)
    X_train_scaled, y_train_scaled = create_sequences(X_scaled, y_scaled, time_steps=1)
    
    # Split data into training and testing sets
    train_size = int(len(X_train_scaled) * 0.8)
    X_train, y_train = X_train_scaled[:train_size], y_train_scaled[:train_size]
    X_test, y_test = X_train_scaled[train_size:], y_train_scaled[train_size:]
    
    # Train model
    model = train_model(X_train, y_train)
    
    # Evaluate performance on the testing set
    test_loss = model.evaluate(X_test, y_test, verbose=0)
    print("Test loss:", test_loss)
    
    # Make predictions
    y_pred = make_predictions(model, X_test)
    # Inverse scaling of the predicted value
    scaler = MinMaxScaler()
    scaler.fit(df[['close']]) # Fit the scaler on the original closing prices
    y_pred_inv = scaler.inverse_transform(y_pred)
    y_test_inv = scaler.inverse_transform(y_test)
    
    # Evaluate model performance
    model_accuracy = evaluate_model(y_test_inv, y_pred_inv)
    
    # Adjust predicted price within 10% range from the previous price
    prev_price = df['close'].iloc[-1]
    y_pred_inv = y_pred_inv[-1][0]
    max_price = prev_price * 1.10
    min_price = prev_price * 0.90
    y_pred_inv = min(y_pred_inv, max_price)
    y_pred_inv = max(y_pred_inv, min_price)
    # Return predicted price
    print("predicted price is ", y_pred_inv)

    return y_pred_inv,model_accuracy
