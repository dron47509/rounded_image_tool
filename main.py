from PIL import Image, ImageDraw
import os

def crop_to_square(image):
 
    width, height = image.size

    # Выбираем минимальную сторону
    min_side = min(width, height)

    # Вычисляем координаты обрезки для создания квадрата
    left = (width - min_side) // 2
    top = (height - min_side) // 2
    right = (width + min_side) // 2
    bottom = (height + min_side) // 2

    # Обрезаем изображение
    cropped_image = image.crop((left, top, right, bottom))

    return cropped_image


def add_corners(im, rad):
    w, h = im.size
    rad = int(min(w, h) * rad / 100.0)
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, "white")
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im


def make_images_round(input_folder, output_folder):
    # Проверяем, существует ли папка для вывода, и создаем ее, если нет
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Получаем список файлов в указанной папке
    files = os.listdir(input_folder)

    # Обрабатываем каждый файл
    for file_name in files:
        # Полный путь к файлу
        input_path = os.path.join(input_folder, file_name)

        # Пропускаем не-изображения
        if not file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            continue

        # Открываем изображение с помощью Pillow
        image = Image.open(input_path)
        cropted_image = crop_to_square(image)
        rounded_image = add_corners(cropted_image, 50)

        output_path = os.path.join(output_folder, f"rounded_{file_name}")
        print(output_path)
        rounded_image.save(output_path, format="png")

if __name__ == "__main__":
    # Укажите папку с изображениями и папку для сохранения результатов
    input_folder = "Сырые"
    output_folder = "Обработанные"

    make_images_round(input_folder, output_folder)
