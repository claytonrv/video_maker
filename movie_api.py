from flask import Flask
from flask import request, abort
import video_maker
import requests
app = Flask(__name__)

@app.route('/movie_api/process_video/', methods=['POST'])
def process_video():
    if not request.json or not 'id' in request.json:
        abort(400)
    
    video_infos = {
        'id': request.json['id'],
        'images_path':request.json['path'],
        'rotation': request.json['rotation'],
        'images_ext': request.json['files_extension'],
        'video_ext': request.json['video_ext'],
        'return_url': request.json['return_url'],
        'error_url': request.json['error_url']

    }
    create_video(video_infos)
    return "ok"


def create_video(video_infos):
    video = video_maker.make_video(image_folder=video_infos['images_path'], out_video_name='video',
                                   out_video_ext=video_infos['video_ext'], rotation_angle=video_infos['rotation'],
                                   image_ext=video_infos['images_ext'], vid_to_web=True)
    if video:
       video_maker.move_images(video_infos['images_path'], video_infos['images_ext'])
       save_video(video_infos['id'], video_infos['return_url'])
       print("video created")
    else:
        inform_error(video_infos['id'], video_infos['error_url'])
        print("error")

def save_video(json_id, return_url):
    request_url = return_url+json_id
    r = requests.get(request_url)
    print(r.status_code)


def inform_error(json_id, error_url):
    request_url = error_url + json_id
    r = requests.get(request_url)
    print(r.status_code)


if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)