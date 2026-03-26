import os
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI
from django.core.management.base import BaseCommand
from movie.models import Movie


class Command(BaseCommand):
    help = "Calculate similarity between movies using embeddings"

    def handle(self, *args, **kwargs):
        # ✅ Cargar API KEY
        load_dotenv()
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # ✅ Seleccionar películas (puedes cambiarlas)
        movie1 = Movie.objects.get(title="The House of the Devil")
        movie2 = Movie.objects.get(title="Cinderella")

        # ✅ Función para obtener embedding
        def get_embedding(text):
            response = client.embeddings.create(
                input=[text],
                model="text-embedding-3-small"
            )
            return np.array(response.data[0].embedding, dtype=np.float32)

        # ✅ Similitud de coseno
        def cosine_similarity(a, b):
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

        # 🎬 Embeddings de películas
        emb1 = get_embedding(movie1.description)
        emb2 = get_embedding(movie2.description)

        similarity = cosine_similarity(emb1, emb2)

        self.stdout.write(f"🎬 {movie1.title} vs {movie2.title}: {similarity:.4f}")

        # 🧠 Prompt de prueba
        prompt = "película sobre romance"
        prompt_emb = get_embedding(prompt)

        sim1 = cosine_similarity(prompt_emb, emb1)
        sim2 = cosine_similarity(prompt_emb, emb2)

        self.stdout.write(f"📝 Prompt vs {movie1.title}: {sim1:.4f}")
        self.stdout.write(f"📝 Prompt vs {movie2.title}: {sim2:.4f}")