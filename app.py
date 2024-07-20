from flask import Flask, render_template, jsonify, request
import chatgpt

app = Flask(__name__)

# # List of users kept in a set
# valid_users = {'tom', 'bill' }

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
        response = {
            "media": media,
            "content": content,
            "recommendations": recommendations
        }
        return jsonify(response)
    else:
        return jsonify({"error": "Missing media or content"}), 400


if __name__== '__main___':
    app.run(debug=True, host="0.0.0.0")
