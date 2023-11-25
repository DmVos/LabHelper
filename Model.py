import io
import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import base64


def define_corrosion(image_input, sample_size_h, sample_size_w):

    image = cv2.cvtColor(np.array(image_input), cv2.COLOR_RGB2BGR)
    # Convert to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Apply Gaussian blur
    sigma = 0.3 * ((7 - 1) * 0.5 - 1) + 0.8
    blurred_image = cv2.GaussianBlur(hsv_image, (7, 7), sigma)

    # Apply Laplacian Operator
    laplacian = cv2.Laplacian(blurred_image, cv2.CV_64F)
    laplace_smoothness = laplacian.var()

    # Define labeling functions
    def label_function_1(pixel):
        h, s, v = pixel
        return 175 <= h < 205 and 30 <= s < 205 and 30 < v <= 135

    def label_function_2(pixel):
        h, s, v = pixel
        return 4 < h <= 15 and 30 <= s < 205 and 30 < v <= 135

    def label_function_3(pixel):
        h, s, v = pixel
        return laplace_smoothness < 10 and ((4 < h <= 15) or (175 <= h < 205)) and 30 <= s < 205 and 30 < v <= 135

    def label_function_4(pixel):
        return laplace_smoothness > 4000

    def label_function_5(pixel):
        _, _, v = pixel
        return v < 30

    def label_function_6(pixel):
        h, s, v = pixel
        return v > 230 and s > 35

    def label_function_7(pixel):
        h, s, _ = pixel
        return 230 < h < 256 and s > 230


    # Apply labeling functions to create mask
    mask = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            pixel = blurred_image[i, j]
            if (
                label_function_1(pixel) or
                label_function_2(pixel) or
                label_function_3(pixel) or
                #label_function_4(pixel) or
                #label_function_5(pixel) or
                #label_function_6(pixel) or
                label_function_7(pixel)
            ):
                mask[i, j] = 255  # White for corroded pixels

    # Create a 3-channel mask for visualization
    corroded_mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    corroded_mask[np.where((corroded_mask == [255, 255, 255]).all(axis=2))] = [0, 0, 255]  # Red color

    # Blend the original image with the corroded mask
    result_image = cv2.addWeighted(image, 0.7, corroded_mask, 0.3, 0)

    # Display the original image, corroded mask, and the result
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), extent=[0, sample_size_h, sample_size_w, 0])
    plt.title('Original Image')

    plt.subplot(1, 3, 2)
    plt.imshow(corroded_mask, extent=[0, sample_size_h, sample_size_w, 0])  # Set extent to control axis limits
    plt.title('Corroded Mask')

    plt.subplot(1, 3, 3)
    plt.imshow(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB), extent=[0, sample_size_h, sample_size_w, 0])
    plt.title('Result with Corroded Outline')

    corroded_area_pixels = cv2.countNonZero(mask)

    # Define the total area in square meters
    total_area_meters = (sample_size_h*sample_size_w)/10000  # calculate corrosion area from input values

    # Calculate the area per pixel
    area_per_pixel = total_area_meters / (512 * 512)

    # Calculate the corroded area in square meters
    corroded_area_meters = area_per_pixel * corroded_area_pixels
    corroded_area_cm2 = corroded_area_meters * 10000

    # Add image to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Safe image for result
    image = base64.b64encode(buf.getvalue()).decode('utf-8')

    # Close buffer
    buf.close()

    return image, corroded_area_meters, corroded_area_cm2

