from flask import Flask, render_template, jsonify, request
import chatgpt

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/checklists", methods=["POST"])
def checklists():
    print("entered api")
    
    #Get the type of media and the content
    media = request.form.get('media')
    content = request.form.get('content')

    recommendations = chatgpt.getRecomendations(media, content)

    #Checks if the user has input a media or content
    if media and content:
        #new HTML page with the recommendations
        return render_template("results.html", media=media, content=content, recommendations=recommendations)
    else:
        return "Missing media or content", 400


if __name__== '__main__':
    app.run(debug=True, host="0.0.0.0")
