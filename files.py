from faker import Faker
import requests

fake = Faker()

url = fake.image_url(184, 184)

s = requests.get('https://picsum.photos/184/184')

print(s.url)