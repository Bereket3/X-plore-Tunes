import os
from pathlib import Path
from importlib.util import find_spec
from typing import Annotated


from fastapi import Header
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi import Request, Response
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles


from django.core.wsgi import get_wsgi_application
from django.conf import settings
from project_006.settings import BASE_DIR


# Export Django settings env variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_006.settings')

# Get Django WSGI app
django_app = get_wsgi_application()

# Import a model
# And always import your models after you export settings
# and you get Django WSGI app
from root_music_config.models import MusicContainer as Music



# Create FasatAPI instance
app = FastAPI()

# Serve Django static files
app.mount('/static',
    StaticFiles(
        directory=os.path.normpath(
            os.path.join(find_spec('django.contrib.admin').origin, '..', 'static')
        )
   ),
   name='static',
)

# Mount Django app
app.mount('/django-test', WSGIMiddleware(django_app))


@app.get("/audio/{_path}")
async def video_endpoint(_path: str, Range : Annotated[str | None, Header()] = None):
    video_path = Path(BASE_DIR / f'media/music_files/audio/{_path}.mp3')
    try:
        start, end = Range.replace("bytes=", "").split("-")
        start = int(start)
        end = int(end)
    except:
        start = 0
        end = 0

    with open(video_path, "rb") as audio:
        audio.seek(start)
        filesize = str(video_path.stat().st_size)
        if end == 0:
            data = audio.read(int(filesize) - start)
        else:
            data = audio.read(end - start)
        
        headers = {
            'Content-Range': f'bytes {start}-{end}/{filesize}',
            'Accept-Ranges': 'bytes'
        }
        
        return Response(data, status_code=200, headers=headers, media_type="audio/mpeg")