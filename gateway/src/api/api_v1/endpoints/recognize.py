import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.services.crud_person import service_instance as crud_person
from src.services.crud_photo import service_instance as crud_photo
from src.services.media import service_instance as media
from src.services.face import service_instance as face_service
from src.api import dependencies as deps


router = APIRouter()


@router.post('/train')
async def train(db: Session = Depends(deps.get_db)):
    # TODO: back ground tasks
    data = []
    # TODO: handle skip/limit
    people = crud_person.get_multi(db)
    for person in people:
        # get all photos from s3
        photos = crud_photo.get_multiple_by_owner(db, owner_id=person.id)
        bytes_imgs = []
        for photo in photos:
            bytes_img = media.minio.get_object(object_name=photo.object_name, bucket_name=photo.bucket_name)
            bytes_imgs.append(bytes_img)

        # calculate embedding    
        # FIXME: improve this. Avoid directly calling long running blocking operations
        embedding = face_service.get_general_embedding(bytes_imgs)
        data.append({
            'person_id': person.id,
            'person_name': person.full_name,
            'embedding': embedding
        })

    data = json.dumps(data, indent=4)
    data = bytes(data, encoding='utf-8')
    media.minio.put_object(object_name='embedding_data.json', data=data, content_type='application/json')
    
    return 'DONE'
