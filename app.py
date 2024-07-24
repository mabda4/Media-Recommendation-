from flask import Flask, render_template, jsonify, request
import chatgpt
import spotify
import movie


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
   

    # #Checks if the user has input a media or content
    # if media and content:
    #     #new HTML page with the recommendations
    #     #nested if statements for the type of media
    #     return render_template("results.html", media=media, content=content, recommendations=recommendations)
    # else:
    #     return "Missing media or content", 400

    if media and content:
        track_ids = {}
        trailers = {}
        if media.lower() == 'music':
            track_ids = spotify.getTrackIDs(recommendations)
            print("Track IDs:", track_ids)
        elif media.lower() == 'movie':
            trailers = movie.getTrailers(recommendations)
            print("Trailers:", trailers)

        return render_template("results.html", media=media, content=content, recommendations=recommendations, track_ids=track_ids, trailers=trailers)
    else:
        return "Missing media or content", 400


if __name__== '__main__':
    app.run(debug=True, host="0.0.0.0")
