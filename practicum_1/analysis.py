import os
import cv2
import time
import threading


class ImageAnalysis:
    def __init__(self, image_path: str):
        self.stars_count = 0
        self.planets_count = 0
        self.image_path = image_path
        self.image = cv2.imread(image_path)

        if self.image is None:
            raise ValueError("Failed to upload image!")

    def analyze(self) -> None:
        """ Grayscale conversion, binarization, and contour search """
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(gray_image, 211, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        """ Classification of objects and allocation """
        for _, contour in enumerate(contours):
            if cv2.contourArea(contour) < 1:
                """ Planets are circled in red """
                cv2.drawContours(self.image, [contour], -1, (0, 255, 0), 2)
                self.planets_count += 1
            else:
                """ Stars are circled in green """
                cv2.drawContours(self.image, [contour], -1, (0, 0, 255), 2)
                self.stars_count += 1

        cv2.imwrite(os.path.join("processed_images", os.path.basename(self.image_path.replace('.jpg', ' (out).jpg'))), self.image)
        cv2.destroyAllWindows()

    def print_statistics(self, processing_time: float) -> None:
        """ Output of collected statistics """
        print(f"{self.image_path}")
        print(f"Resolution: {self.image.shape[1]}x{self.image.shape[0]}")
        print(f"Total stars: {self.stars_count}")
        print(f"Total planets: {self.planets_count}")
        print(f"Total objects: {self.stars_count + self.planets_count}")
        print(f"Processing time: {processing_time:.2f} seconds\n")


def process_image(file):
    start_time = time.time()
    image = ImageAnalysis(f"{os.path.join('images', file)}")
    image.analyze()
    end_time = time.time()
    image.print_statistics(end_time - start_time)


if __name__ == "__main__":
    image_files = [file for file in os.listdir("images")]
    threads = []

    for image_file in image_files:
        thread = threading.Thread(target=process_image, args=(image_file,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
