import numpy as np
import pandas as pd
import pickle
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.utils import to_categorical
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

os.makedirs("ai_model/trained_models", exist_ok=True)
os.makedirs("ai_model/reports", exist_ok=True)

def load_data():
    print("📂 Loading flood dataset...")
    with open("ai_model/processed/flood_data.pkl", "rb") as f:
        data = pickle.load(f)
    return data

def reshape_for_lstm(X, timesteps=7):
    """7-day sequence for flood prediction"""
    n_samples = len(X) - timesteps
    n_features = X.shape[1]
    X_seq = np.zeros((n_samples, timesteps, n_features))
    for i in range(n_samples):
        X_seq[i] = X[i:i+timesteps]
    return X_seq

def build_flood_model(timesteps, n_features, n_classes):
    model = Sequential([
        LSTM(128, return_sequences=True,
             input_shape=(timesteps, n_features)),
        Dropout(0.3),
        BatchNormalization(),
        LSTM(64, return_sequences=True),
        Dropout(0.2),
        LSTM(32, return_sequences=False),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dense(n_classes, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

def train():
    print("="*60)
    print("TRAINING FLOOD PREDICTION LSTM MODEL")
    print("="*60)
    
    data = load_data()
    X_train = data["X_train"]
    X_val = data["X_val"]
    X_test = data["X_test"]
    y_train = data["y_train"].values
    y_val = data["y_val"].values
    y_test = data["y_test"].values
    
    print(f"Training samples: {len(X_train)}")
    print(f"Validation samples: {len(X_val)}")
    print(f"Test samples: {len(X_test)}")
    
    # Reshape for LSTM
    TIMESTEPS = 7
    X_train_seq = reshape_for_lstm(X_train, TIMESTEPS)
    X_val_seq = reshape_for_lstm(X_val, TIMESTEPS)
    X_test_seq = reshape_for_lstm(X_test, TIMESTEPS)
    
    y_train_seq = y_train[TIMESTEPS:]
    y_val_seq = y_val[TIMESTEPS:]
    y_test_seq = y_test[TIMESTEPS:]
    
    n_classes = 4
    y_train_cat = to_categorical(y_train_seq, n_classes)
    y_val_cat = to_categorical(y_val_seq, n_classes)
    y_test_cat = to_categorical(y_test_seq, n_classes)
    
    print(f"\nSequence shape: {X_train_seq.shape}")
    print(f"Classes: {n_classes} (safe/watch/warning/emergency)")
    
    # Build model
    print("\n🏗️ Building Flood LSTM architecture...")
    model = build_flood_model(TIMESTEPS, X_train.shape[1], n_classes)
    model.summary()
    
    # Callbacks
    early_stop = EarlyStopping(
        monitor='val_accuracy',
        patience=5,
        restore_best_weights=True
    )
    checkpoint = ModelCheckpoint(
        "ai_model/trained_models/flood_model_best.h5",
        monitor='val_accuracy',
        save_best_only=True
    )
    
    # Train!
    print("\n🚀 Training started...")
    history = model.fit(
        X_train_seq, y_train_cat,
        validation_data=(X_val_seq, y_val_cat),
        epochs=30,
        batch_size=32,
        callbacks=[early_stop, checkpoint],
        verbose=1
    )
    
    # Evaluate
    print("\n📊 Evaluating on test set...")
    test_loss, test_accuracy = model.evaluate(X_test_seq, y_test_cat, verbose=0)
    print(f"Test Accuracy: {test_accuracy*100:.2f}%")
    
    y_pred = model.predict(X_test_seq)
    y_pred_classes = np.argmax(y_pred, axis=1)
    
    print("\nClassification Report:")
    unique_classes = sorted(np.unique(y_test_seq))
    target_names_present = ['Safe', 'Watch', 'Warning', 'Emergency']
    labels_present = [target_names_present[i] for i in unique_classes]

    print(classification_report(
    y_test_seq, y_pred_classes,
    labels=unique_classes,
    target_names=labels_present
))
    
    # Save model
    model.save("ai_model/trained_models/flood_model.h5")
    print("\n✅ Flood model saved!")
    
    with open("ai_model/reports/flood_history.pkl", "wb") as f:
        pickle.dump(history.history, f)
    
    # Plot
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Val Accuracy')
    plt.title('Flood Model — Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Val Loss')
    plt.title('Flood Model — Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.tight_layout()
    plt.savefig('ai_model/reports/flood_training_curves.png')
    print("✅ Training curves saved!")
    
    return model, test_accuracy

if __name__ == "__main__":
    model, accuracy = train()
    print(f"\n🎯 Final Test Accuracy: {accuracy*100:.2f}%")
    print("Flood LSTM model training complete!")