from byuimage import Image
import sys

#validates command line arguments
def validate_commands(args):
    args_key = {
        '-d' : 2,
        '-k' : 4,
        '-s' : 3,
        '-g' : 3,
        '-b' : 7,
        '-f' : 3,
        '-m' : 3,
        '-c' : 7,
        '-y' : 6,
        '-h' : 1
    }

    # checks if the matching flag and length pair are in the args_key dictionary
    if args[0] in args_key and len(args) == args_key[args[0]]:
        return True
    
# displays the image that is input
def display(args):
    img = Image(args[0])
    img.save("cached_images/image_cache.png")

# darkens image by a certain percent and saves to output file location
def darken(args):
    img = Image(args[0])
    percent = float(args[1])
    brightness = 1 - percent

    for pixel in img:
        pixel.red = pixel.red * brightness
        pixel.green = pixel.green * brightness
        pixel.blue = pixel.blue * brightness

    img.save("cached_images/image_cache.png")

# applies sepia filter to input image and saves to output file location
def sepia(args):
    img = Image(args[0])

    for pixel in img:
        true_red = 0.393*pixel.red + 0.769*pixel.green + 0.189*pixel.blue
        true_green = 0.349*pixel.red + 0.686*pixel.green + 0.168*pixel.blue
        true_blue = 0.272*pixel.red + 0.534*pixel.green + 0.131*pixel.blue

        pixel.red = true_red
        pixel.green = true_green
        pixel.blue = true_blue

        if pixel.red > 255:
            pixel.red = 255
        if pixel.green > 255:
            pixel.green = 255
        if pixel.blue > 255:
            pixel.blue = 255

    img.save("cached_images/image_cache.png")

# averages the colors of each pixel to create grayscale image, then returns it
def grayscale(args):
    img = Image(args[0])

    for pixel in img:
        average = (pixel.red + pixel.green + pixel.blue) / 3
        pixel.red = average
        pixel.green = average
        pixel.blue = average
    
    img.save("cached_images/image_cache.png")

# creates a new image with borders around the edges of a specified thickness and color and outputs to selected file
def make_borders(args):
    img = Image(args[0])
    w = img.width
    h = img.height
    thickness = int(args[1])
    new_img = Image.blank(w + 2*thickness, h + 2*thickness)

    for x in range(new_img.width):
        for y in range(new_img.height):
            pixel = new_img.get_pixel(x, y)

            if x < thickness or y < thickness or x >= w + thickness or y >= h + thickness:
                pixel.red = args[2]
                pixel.green = args[3]
                pixel.blue = args[4]
            else:
                o_pixel = img.get_pixel(x - thickness, y - thickness)
                set_pixel(pixel, o_pixel)

    new_img.save("cached_images/image_cache.png")

# flips input image top to bottom and saves to output file
def flip(args):
    img = Image(args[0])
    w = img.width
    h = img.height
    new_img = Image.blank(w, h)

    for x in range(w):
        for y in range(h):
            pixel = img.get_pixel(x, h - y - 1)
            n_pixel = new_img.get_pixel(x, y)
            set_pixel(n_pixel, pixel)

    new_img.save("cached_images/image_cache.png")

# mirrors input image left to right and saves to output file
def mirror(args):
    img = Image(args[0])
    w = img.width
    h = img.height
    new_img = Image.blank(w, h)

    for x in range(w):
        for y in range(h):
            pixel = img.get_pixel(w - x - 1, y)
            n_pixel = new_img.get_pixel(x, y)
            set_pixel(n_pixel, pixel)

    new_img.save("cached_images/image_cache.png")

# composites 4 images of the same size into one image with a specified border thickenss and saves to output file. Border color is black
def composite(args):
    img1 = Image(args[1])
    img2 = Image(args[2])
    img3 = Image(args[3])
    img4 = Image(args[4])
    w = img1.width
    h = img1.height
    thickness = int(args[6])
    new_w = 2*w + 3*thickness
    new_h = 2*h + 3*thickness
    new_img = Image.blank(new_w, new_h)

    for x in range(new_w):
        for y in range(new_h):
            n_pixel = new_img.get_pixel(x, y)
            
            if x < w + thickness and x >= thickness and y < h + thickness and y >= thickness:
                set_pixel(n_pixel, img1.get_pixel(x - thickness, y - thickness))
            elif x >= w + 2*thickness and x < 2*w + 2*thickness and y < h + thickness and y >= thickness:
                set_pixel(n_pixel, img2.get_pixel(x - w - 2*thickness, y - thickness))
            elif x < w + thickness and x >= thickness and y >= h + 2*thickness and y < 2*h + 2*thickness:
                set_pixel(n_pixel, img3.get_pixel(x - thickness, y - h - 2*thickness))
            elif x >= w + 2*thickness and x < 2*w + 2*thickness and y >= h + 2*thickness and y < 2*h + 2*thickness:
                set_pixel(n_pixel, img4.get_pixel(x - w - 2*thickness, y - h - 2*thickness))
            else:
                n_pixel.red = 0
                n_pixel.green = 0
                n_pixel.blue = 0

    new_img.save("cached_images/image_cache.png")

# given threshold and factor, composes two images onto each other, removing green from the foreground image
def greenscreen(args):
    f_img = Image(args[1])
    b_img = Image(args[2])
    w = b_img.width
    h = b_img.height
    threshold = int(args[4])
    factor = float(args[5])

    for x in range(w):
        for y in range(h):
            pixel = f_img.get_pixel(x, y)
            if detect_green(pixel, threshold, factor) == False:
                set_pixel(b_img.get_pixel(x, y), pixel)

    b_img.save("cached_images/image_cache.png")


def help(args):
    print(
        '''
        '-d' : Display: displays the input image (usage: $file -d <input-image path>)
        '-k' : Darken: darkens the input image by a certain percent value between 0 and 1 (usage: $file -k <input-image path> <output-file name> <percent to darken by>)
        '-s' : Sepia: applies the sepia filter to the input image (usage: $file -s <input-file path>)
        '-g' : Grayscale: changes input image to grayscale (usage: $file -g <input-file path>)
        '-b' : Make Borders: makes a border around the input image with a specified thickness and color (usage: $file -b  <input-file path> <output-file name> <thickness> <border red> <border greem> <border blue>)
        '-f' : Flip: flips the input image upside down (usage: $file -f <input-file path> <output-file name>)
        '-m' : Mirror: flips the input image left to right (usage: $file -m <input-file path> <output-file name>)
        '-c' : Composite: Places 4 images in a grid with an inside border (usage: $file -c <input-file path1> <input-file path2> <input-file path3> <input-file path4> <output-file name> <border thickness>)
        '-y' : Greenscreen: Takes two images, removes green from one and places it on top of other (usage: $file -y <foreground-image path> <background-image path> <output-file name> <threshold> <factor>)
        ''')

# sets pixel colors for red, green. and blue
def set_pixel(pixel, n_pixel):
    pixel.red = n_pixel.red
    pixel.green = n_pixel.green
    pixel.blue = n_pixel.blue

def detect_green(pixel, threshold = 90, factor = 1.3):
    average = (pixel.red + pixel.green + pixel.blue) / 3
    if pixel.green >= factor * average and pixel.green > threshold:
        return True
    else:
        return False

def main():
    args = sys.argv[1:]
    args_func = {
        '-d' : display,
        '-k' : darken,
        '-s' : sepia,
        '-g' : grayscale,
        '-b' : make_borders,
        '-f' : flip,
        '-m' : mirror,
        '-c' : composite,
        '-y' : greenscreen,
        '-h' : help
    }

    # validates the command line arguments and calls the proper function based on the input flag
    if validate_commands(args) == True:
        args_func[args[0]](args)
    else:
        help(args)


if __name__ == '__main__':
    main()