import cv2

class SupplyWriter:
    def __init__(self, intput_video, output_video, opt_thres, rgb_input=True):
        reader = cv2.VideoCapture(intput_video)
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        fps = reader.get(cv2.CAP_PROP_FPS)
        width = int(reader.get(3))
        height = int(reader.get(4))
        reader.release()
        self.padding = 40
        self.writer = cv2.VideoWriter(output_video, fourcc, fps, (height, width)[::-1])
        self.rgb_input = rgb_input
        self.opt_thres = opt_thres

    def run(self, images, scores, boxes):
        # Text variables
        font_face = cv2.FONT_HERSHEY_SIMPLEX
        thickness = 5
        font_scale = 2

        for image, score, box in zip(images, scores, boxes):
            if self.rgb_input:
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if box is not None:
                label = "fake" if score > self.opt_thres else "real"
                x1, y1, x2, y2 = box
                x = int(x1)
                y = int(y1)
                w = int(x2 - x1)
                h = int(y2 - y1)
                color = (
                    (255, 255, 0) if label == "real" else (0, 255, 255)
                )  # BGR 255  0
                text = label + str(format(score, '.4f'))  # add probability
                cv2.putText(
                    image,
                    text,  ##
                    (x, y + h + 68),
                    font_face,
                    font_scale,
                    color,
                    thickness,
                    2,
                )
                # draw box over face
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 10)
            self.writer.write(image)
        # print(image.shape)
        self.writer.release()
