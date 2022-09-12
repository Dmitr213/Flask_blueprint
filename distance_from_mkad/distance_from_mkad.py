from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def results():
    return "Hello World"

print(results)

#https://geocode-maps.yandex.ru/1.x/?apikey=8fb54072-d844-4ae6-ae64-162fd0c901b0&geocode=Москва,+Тверская+улица,+дом+7

if __name__ == "__main__":
    app.run(debug=True)
