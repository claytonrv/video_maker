from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize
import os, imutils, shutil

def make_video(image_folder, out_video_name, out_video_ext, rotation_angle, image_ext, vid_to_web, fps=10, size=None, is_color=True, format="FMP4"):
    """
    Create a video from a list of images.
 
    @param      outvid      output video
    @param      images      list of images to use in the video
    @param      fps         frame per second
    @param      size        size of each frame
    @param      is_color    color
    @param      format      see http://www.fourcc.org/codecs.php
    @return                 see http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
 
    The function relies on http://opencv-python-tutroals.readthedocs.org/en/latest/.
    By default, the video will have the size of the first image.
    It will resize every image to this size before adding them to the video.
    """
    images = [image_folder+img for img in os.listdir(image_folder) if img.endswith(image_ext)]
    fourcc = VideoWriter_fourcc(*format)
    vid = None
    images.sort()
    for image in images:
        if not os.path.exists(image):
            raise FileNotFoundError(image)
        print(image)
        img = imread(image)
        if(rotation_angle):
            img = imutils.rotate(img, int(rotation_angle))
        if vid is None:
            if size is None:
                size = img.shape[1], img.shape[0]
            print(image_folder + out_video_name)
            vid = VideoWriter((image_folder + out_video_name+".avi"), fourcc, float(fps), size, is_color)
        if size[0] != img.shape[1] and size[1] != img.shape[0]:
            img = resize(img, size)
        vid.write(img)
    vid.release()
    if vid_to_web:
        make_for_web(image_folder, (out_video_name+".avi"), (out_video_name+out_video_ext))
    return vid

def make_for_web(video_path, original_video_name, video_name):
    original_video= video_path+original_video_name
    new_video= video_path+video_name
    os.system("ffmpeg -i "+original_video+" -vcodec h264 -acodec aac -strict -2  -q:v 2 "+new_video)


def move_images(images_folder, image_ext):
    path = images_folder+"thumbs/"
    os.mkdir(path)
    for img in os.listdir(images_folder):
        image = images_folder+img
        if image.endswith(image_ext):
            shutil.move(image, path+img)
