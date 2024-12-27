from PIL import Image
import glob

# Znajdź wszystkie obrazki zaczynające się od "img"
image_files = glob.glob("./img*.png")
# Otwórz obrazki i załaduj je do listy
images = [Image.open(img) for img in image_files]

# Utwórz GIF-a
if images:
    images[0].save(
        './waTor_animacja.gif',
        save_all=True,
        append_images=images[1:],
        duration=50,  # Czas trwania klatki w milisekundach
        loop=0         # Pętla nieskończona
    )
    print("GIF został utworzony jako 'waTor_animacja.gif'")
else:
    print("Nie znaleziono żadnych plików obrazów.")