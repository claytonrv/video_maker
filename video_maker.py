from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize
import os, imutils, shutil

def make_video(image_folder, outvid, rotation_angle, image_ext, fps=5, size=None, is_color=True, format="X264"):
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
    try:
        images = [image_folder+img for img in os.listdir(image_folder) if img.endswith(image_ext)]
        fourcc = VideoWriter_fourcc(*format)
        vid = None
        for image in images:
            if not os.path.exists(image):
                raise FileNotFoundError(image)
            print(image)
            img = imread(image)
            if(rotation_angle):
                img = imutils.rotate(img, rotation_angle)
            if vid is None:
                if size is None:
                    size = img.shape[1], img.shape[0]
                vid = VideoWriter((image_folder+outvid), fourcc, float(fps), size, is_color)
            if size[0] != img.shape[1] and size[1] != img.shape[0]:
                img = resize(img, size)
            vid.write(img)
        vid.release()
        return vid
    except:
        return None


def move_images(images_folder, image_ext):
    path = images_folder+"thumbs/"
    os.mkdir(path)
    for img in os.listdir(images_folder):
        image = images_folder+img
        if image.endswith(image_ext):
            shutil.move(image, path+img)