import functools
import os

from matplotlib import gridspec
#import matplotlib.pylab as plt
import numpy as np
#import tensorflow as tf
import tensorflow.io as tf_io
import tensorflow.image as tf_image
import tensorflow_hub as hub

print("TF Version: ", tf.__version__)
print("TF Hub version: ", hub.__version__)
print("Eager mode enabled: ", tf.executing_eagerly())
print("GPU available: ", tf.config.list_physical_devices('GPU'))



if __name__ != '__main__':

  def crop_center(image):
    """Returns a cropped square image."""
    shape = image.shape
    new_shape = min(shape[1], shape[2])
    offset_y = max(shape[1] - shape[2], 0) // 2
    offset_x = max(shape[2] - shape[1], 0) // 2
    image = tf.image.crop_to_bounding_box(
        image, offset_y, offset_x, new_shape, new_shape)
    return image

  @functools.lru_cache(maxsize=None)
  def load_image(image_url, image_size=(256, 256), preserve_aspect_ratio=True):
    """Loads and preprocesses images."""
    # Cache image file locally.
    image_path = tf.keras.utils.get_file(os.path.basename(image_url)[-128:], image_url)
    # Load and convert to float32 numpy array, add batch dimension, and normalize to range [0, 1].
    img = tf.io.decode_image(
        tf.io.read_file(image_path),
        channels=3, dtype=tf.float32)[tf.newaxis, ...]
    img = crop_center(img)
    img = tf.image.resize(img, image_size, preserve_aspect_ratio=True)
    return img

  # def show_n(images, titles=('',)):
  #   n = len(images)
  #   image_sizes = [image.shape[1] for image in images]
  #   w = (image_sizes[0] * 6) // 320
  #   plt.figure(figsize=(w * n, w))
  #   gs = gridspec.GridSpec(1, n, width_ratios=image_sizes)
  #   for i in range(n):
  #     plt.subplot(gs[i])
  #     plt.imshow(images[i][0], aspect='equal')
  #     plt.axis('off')
  #     plt.title(titles[i] if len(titles) > i else '')
  #   plt.show()

  # @title Load example images  { display-mode: "form" }

  def AIGenerateImage(contentImageURL, styleImageURL):
    #return contentImage, styleImage, contentImage
    content_image_url = contentImageURL # @param {type:"string"}
    style_image_url = styleImageURL # @param {type:"string"}
    output_image_size = 384  # @param {type:"integer"}

    # The content image size can be arbitrary.
    content_img_size = (output_image_size, output_image_size)
    # The style prediction model was trained with image size 256 and it's the 
    # recommended image size for the style image (though, other sizes work as 
    # well but will lead to different results).
    style_img_size = (256, 256)  # Recommended to keep it at 256.

    content_image = load_image(content_image_url, content_img_size)
    style_image = load_image(style_image_url, style_img_size)
    style_image = tf.nn.avg_pool(style_image, ksize=[3,3], strides=[1,1], padding='SAME')
    ##show_n([content_image, style_image], ['Content image', 'Style image'])

    hub_handle = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'
    hub_module = hub.load(hub_handle)

    outputs = hub_module(content_image, style_image)
    stylized_image = outputs[0]


    def deprocess_image(img):
      print('incoming img: ',img)
      print('incoming img shape: ', img.shape)
      img = img.numpy()
      #img = np.reshape(img,(384,384,3)) 
      img = np.squeeze(img, axis=0)
      img = (img * 255).astype(np.uint8)
      return img

    #content_image = deprocess_image(content_image)
    #style_image = deprocess_image(style_image)
    

    #stylized_image = stylized_image.numpy()
    #print('stylized image: ', stylized_image)
    #stylized_image = np.squeeze(stylized_image, axis=0)
    #print('stylized image shape: ', stylized_image.shape)
    #print('max min stylized image: ', np.max(stylized_image), np.min(stylized_image))
    
    # Visualize input images and the generated stylized image.

    #show_n([content_image, style_image, stylized_image], titles=['Original content image', 'Style image', 'Stylized image'])

    stylized_image = deprocess_image(stylized_image)
    print('returning stylized image', stylized_image)

    return stylized_image
