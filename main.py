from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TYER, TCON, APIC, COMM
import io

app = FastAPI()

@app.post("/tag-mp3")
async def tag_mp3(
    file: UploadFile = File(...),
    cover: UploadFile = File(None),  # La carátula es opcional
    title: str = Form(...),
    artist: str = Form(...),
    album: str = Form(...),
    year: str = Form(None),
    genre: str = Form(None)
):
    # 1. Leer el archivo MP3 en memoria
    audio_content = await file.read()
    audio_stream = io.BytesIO(audio_content)
    
    # 2. Cargar etiquetas ID3 (o crearlas si no existen)
    try:
        tags = ID3(audio_stream)
    except:
        tags = ID3()
        tags.save(audio_stream)
    
    # 3. Asignar metadatos de texto
    tags.add(TIT2(encoding=3, text=title))
    tags.add(TPE1(encoding=3, text=artist))
    tags.add(TALB(encoding=3, text=album))
    
    if year:
        tags.add(TYER(encoding=3, text=year))
    if genre:
        tags.add(TCON(encoding=3, text=genre))

    # 4. Incrustar la carátula (Cover Art) si se envía
    # Esto es vital para que Navidrome muestre la imagen bonita
    if cover:
        cover_content = await cover.read()
        tags.add(APIC(
            encoding=3,
            mime=cover.content_type,  # ej: 'image/jpeg'
            type=3,  # 3 es "Front Cover"
            desc=u'Cover',
            data=cover_content
        ))

    # 5. Guardar cambios en el stream
    tags.save(audio_stream)
    
    # Rebobinar el stream para enviarlo de vuelta
    audio_stream.seek(0)

    # 6. Devolver el archivo modificado
    return StreamingResponse(
        audio_stream, 
        media_type="audio/mpeg",
        headers={"Content-Disposition": f"attachment; filename={file.filename}"}
    )
