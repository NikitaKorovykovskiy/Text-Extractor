from django.shortcuts import render
from django.contrib import messages
import pytesseract
import numpy as np
import base64
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = (
    r"D:\Dev\Проекты\Фото_в_текст\tesseract.exe"
)


def index(request):
    print(request)
    if request.method == "POST":
        try:
            image = request.FILES["imagefile"]
            # encode image to base64 string
            image_base64 = base64.b64encode(image.read()).decode("utf-8")
        except:
            messages.add_message(
                request, messages.ERROR, "No image selected or uploaded"
            )
            return render(request, "photo/home.html")
        lang = request.POST["language"]
        img = np.array(Image.open(image))
        custom_config = r"--oem 3 --psm 6"
        text = pytesseract.image_to_string(
            img, lang=lang, config=custom_config
        )
        # return text to html
        return render(
            request,
            "photo/home.html",
            {"ocr": text, "image": image_base64},
        )

    return render(request, "photo/home.html")
