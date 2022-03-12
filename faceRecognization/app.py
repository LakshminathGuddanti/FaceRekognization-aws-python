import boto3
import streamlit as st
from PIL import Image
import os

def load_image(image_file):
    img=Image.open(image_file)
    return img

st.header("Face matching project using python and aws")
col1,col2 = st.columns(2)

col1.subheader('Enter Source Image')
src_image_file = col1.file_uploader('uploadImage',type=['png','jpg','jpeg'],key=1)

col2.subheader("Enter Target Image")
trg_image_file = col2.file_uploader('uploadImage',type=['png','jpg','jpeg'],key=2)

if src_image_file is not None:
    filedetails = {
        'filename':src_image_file,
        'filetype':src_image_file.type,
        'filesize':src_image_file.size
    }
    col1.write(filedetails)
    col1.image(load_image(src_image_file),width=250)
    with open(os.path.join("uploads",'src.jpg'),'wb') as f:
        f.write(src_image_file.getbuffer())
        col1.success("file uploaded")

if trg_image_file is not None:
    filedetails1 = {
        'filename':trg_image_file,
        'filetype':trg_image_file.type,
        'filesize':trg_image_file.size
    }
    col2.write(filedetails1)
    col2.image(load_image(trg_image_file),width=250)
    with open(os.path.join("uploads",'trg.jpg'),'wb') as f:
        f.write(trg_image_file.getbuffer())
        col2.success("file uploaded")

if st.button("compare Faces"):
    imageSource=open('uploads/src.jpg','rb')
    imageTarget=open('uploads/trg.jpg','rb')
    client = boto3.client('rekognition')
    responce = client.compare_faces(SimilarityThreshold=70,SourceImage={'Bytes':imageSource.read()},TargetImage={'Bytes':imageTarget.read()})
    try:
        print(responce['FaceMatches'][0])
        st.success('Faces matched')
    except:
        st.error("Faces are not matched")