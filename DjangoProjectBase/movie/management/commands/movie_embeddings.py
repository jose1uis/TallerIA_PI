import os
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI
from django.core.management.base import BaseCommand
from movie.models import Movie


class Command(BaseCommand):
    help = "Generate and store embeddings for all movies"

    def handle(self, *args, **kwargs):
        load_dotenv()
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies")

        for movie in movies:
            try:
                response = client.embeddings.create(
                    input=[movie.description],
                    model="text-embedding-3-small"
                )

                emb = np.array(response.data[0].embedding, dtype=np.float32)

                # guardar como binario
                movie.emb = emb.tobytes()
                movie.save()

                self.stdout.write(self.style.SUCCESS(f"Embedding saved: {movie.title}"))

            except Exception as e:
                self.stderr.write(f"Error for {movie.title}: {e}")

        self.stdout.write(self.style.SUCCESS("Finished generating embeddings"))