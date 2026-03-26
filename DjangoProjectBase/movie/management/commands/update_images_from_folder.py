import os
import re
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Assign images from local folder to movies"

    def handle(self, *args, **kwargs):
        images_folder = 'media/movie/images/'

        if not os.path.exists(images_folder):
            self.stderr.write(f"Folder not found: {images_folder}")
            return

        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies")

        updated_count = 0

        for movie in movies:
            try:
                # 🔤 Normalizar título para comparar con nombre de archivo
                normalized_title = self.clean_text(movie.title)

                # 🔍 Buscar imagen que coincida
                matched_image = None
                for filename in os.listdir(images_folder):
                    name_without_ext = os.path.splitext(filename)[0]
                    normalized_filename = self.clean_text(name_without_ext)

                    if normalized_title in normalized_filename:
                        matched_image = filename
                        break

                if matched_image:
                    # 📌 Guardar ruta relativa en la BD
                    movie.image = os.path.join('movie/images', matched_image)
                    movie.save()

                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(f"Updated: {movie.title}"))

                else:
                    self.stderr.write(f"No image found for: {movie.title}")

            except Exception as e:
                self.stderr.write(f"Failed for {movie.title}: {str(e)}")

        self.stdout.write(self.style.SUCCESS(f"Finished updating {updated_count} movies."))

    def clean_text(self, text):
        """
        Limpia texto para comparar nombres (sin espacios, símbolos, etc.)
        """
        text = text.lower()
        text = re.sub(r'[^a-z0-9]', '', text)
        return text