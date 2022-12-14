import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from Resources.Speech.utils import *
from Resources.Text.utils import *
from Resources.Text.model import *
import speech_recognition as sr
from pydub import AudioSegment
from tensorflow.keras.models import load_model
from transformers import TFRobertaModel
import emoji
import re

roberta_model = TFRobertaModel.from_pretrained('roberta-base')

#edf = pd.read_csv("EmoTag/data/EmoTag1200-scores.csv")

labels = ['Angry', 'Fear', 'Happy', 'Neutral', 'Sad']

def roberta_predict(text_sentence):
    max_len = 75
    preprocessed_text = preprocess(text_sentence)
    input_ids, attention_masks = roberta_inference_encode(preprocessed_text, maximum_length = max_len)
    model = roberta_create_model(roberta_model, max_len)
    model.load_weights('Emotion-Recognition-using-Text-with-Emojis-and-Speech/model/roberta.h5')
    result = model.predict([input_ids, attention_masks])
    emotion = labels[np.argmax(result)]
    return emotion

def predict_speech(raw_speech):
    r = sr.Recognizer()
    rs = sr.AudioFile('Data/audio.wav')
    with rs as source:
        audio = r.record(source)
    try:
        text_input = r.recognize_google(audio, language='en-IN', show_all=True)
        print("Google Speech Working")
    except:
        print('Google Speech Recognition Failed')
    text_sentence = text_input['alternative'][0]['transcript']
    print("Transcript : ",text_sentence)
    preprocessed_text = preprocess(text_sentence)
    input_ids, attention_masks = roberta_inference_encode(
        preprocessed_text, maximum_length=max_len)
    roberta_text_model = load_model(
        "Emotion-Recognition-using-Text-with-Emojis-and-Speech\model\\roberta-hybrid-model.h5",
        custom_objects={'TFRobertaModel': TFRobertaModel})
    emotion_text = roberta_text_model.predict([input_ids, attention_masks])

    speech_model = load_model("Emotion-Recognition-using-Text-with-Emojis-and-Speech/model/new_speech_86.h5", compile=False)
    test_feature = get_features(raw_speech)
    temp = np.resize(test_feature, (4, 2388))
    test_final = np.expand_dims(temp, axis=2)

    emotion_speech = speech_model.predict(test_final)
    result = []
    for e in emotion_speech:
        result.append(e)

    print("\n\n*****************\n")
    print("Emotion Speech: ", emotion_speech)
    
    print("\n\n*****************\n")
    # result.append(emotion_text[0])
    # result = np.array(result)
    # print("\n\n*****************\n")
    # print("Result: ", result)
    # print("\n\n*****************\n")
    # final_speech_emotion = np.argmax(np.average(result, axis=0), axis=0)
    print("emotion_text", emotion_text)
    final_speech_emotion = np.argmax(emotion_text[0], axis=0)
    print("final_speech_emotion", final_speech_emotion)
    return labels[final_speech_emotion]

def hybrid_predict_text(text_sentence):
    preprocessed_text = preprocess(text_sentence)
    input_ids, attention_masks = roberta_inference_encode(
        preprocessed_text, maximum_length=max_len)
    roberta_text_model = load_model(
        'Emotion-Recognition-using-Text-with-Emojis-and-Speech/model/roberta-hybrid-model.h5',
        custom_objects={'TFRobertaModel': TFRobertaModel})
    result = roberta_text_model.predict([input_ids, attention_masks])
    emotion = labels[np.argmax(result)]
    return emotion

# def hybrid_predict_text(text_sentence):
#     #edf = pd.read_csv("EmoTag/data/EmoTag1200-scores.csv")
#     preprocessed_text = preprocess(text_sentence)
#     input_ids, attention_masks = roberta_inference_encode(
#         preprocessed_text, maximum_length=max_len)
#     roberta_text_model = load_model(
#         'Emotion-Recognition-using-Text-with-Emojis-and-Speech/model/roberta-hybrid-model.h5',
#         custom_objects={'TFRobertaModel': TFRobertaModel})
#     result = roberta_text_model.predict([input_ids, attention_masks])
    
#     '''#emoji2vec code
#     neutral_col = []
#     for rec in edf.values:
#         temp = (rec[4]+rec[5]+rec[9]+rec[10])/4
#         neutral_col.append(temp)
#         edf['neutral'] = neutral_col
        
#     labels = ['angry','fear','neutral','happy','sad']
        
#     edf = edf.drop(['anticipation','disgust','surprise','trust'],axis = 1)
#     edf.rename(columns = {'anger':'angry','joy':'happy','sadness':'sad'}, inplace = True)
#     edf['sum'] = edf['angry'] + edf['fear'] + edf['sad'] + edf['neutral'] + edf['happy']
#     for label in labels:
#         edf[label] = edf[label]/edf['sum']
#     edf = edf.drop(['sum'], axis=1)
        
#     emoji_data = re.findall(r"[^\u0000-\uFFFF]", text_sentence)
#     print(emoji_data)
#     for emo in emoji_data:
#         if emo in edf['emoji'].values:
#             temp = edf[edf['emoji']==emo].values
#             result.append(list(temp)[0][3:])
#     print(result)
#     final_text_emotion = np.argmax(np.average(np.array(result), axis=0), axis=0)'''

    
#     final_text_emotion = labels[np.argmax(result[0])]
#     return labels[final_text_emotion]

def bilstm_predict_text(text_sentence):
    return bilstm_predict(text_sentence)

def bert_predict_text(text_sentence):
    return bert_predict(text_sentence)