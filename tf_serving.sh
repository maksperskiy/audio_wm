docker run -t --rm -p 8501:8501 -v "./models/classifier:/models/classifier" -e MODEL_NAME=classifier tensorflow/serving --prefer_tflite_model=true

curl -d '{"instances": [1.0, 2.0, 5.0]}' -X POST http://localhost:8501/v1/models/classifier:predict