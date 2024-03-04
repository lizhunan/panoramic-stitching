# panoramic-stitching

Panoramic stitching project based on opencv.

![](https://github.com/lizhunan/asset/blob/main/panoramic-stitching/Figure_1.png?raw=true)

<p align="lift">
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-4caf50.svg" alt="License"></a>
</a>
</p>

## Requirement

The code has used as few complex third-party libraries as possible, and tried to reduce the complexity of setting up the environment. However, there are still some required libraries that need to be imported:

- opencv-python           4.7.0.72
- numpy                   1.21.6
- matplotlib              3.5.3

The left and right images were collected from the same camera. For example, both `./data/left_01.jpg` and `./data/right_01.jpg` are taken by Huawei P30. The camera parameters and image information are shown as follows:

|ISO|EV|S|Focal Length|Resolution|
|---|---|---|---|---|
|50|0|1/2169 s|54 mm|2736×3648|

The author's test environment is shown in the following table:

|CPU|GPU|Memory|OS|Camera|
|---|---|---|---|---|
|Intel(R) Core(TM) i7-1065G CPU @ 1.30GHz|Intel(R) Iris(R) Plus Graphics(Inessential)|16G|Windows 11|build-in(Essential)|

## How to Use

1. Clone the code from Github.
2. Use the following code to scale the image：
    ``` python
    size = 640 # image height
    height, width = left_image.shape[0], left_image.shape[1]
    scale = height/size # scaling
    width_size = int(width/scale) # image width
    image_resize = cv2.resize(left_image, (width_size, size)) # resize
    cv2.imwrite('./data/left_01.jpg', image_resize)
    ```
3. Run:
     `python run.py ./data/left_01.jpg ./data/right_01.jpg`. 

The running parameters are for the two input images(left image and right image). In this example, I choose the photo `left_01.jpg` and `right_01.jpg` in `./data`.

## Futher Work

As shown in the top graph, figure d eliminates the seams based on figure c(the seam at (450, 50)). However, the work of eliminating 'black edges' on the right of the graph still needs to be further improved.

## License and Citations

The source code is published under MIT license, see [license file](./LICENSE) for details.