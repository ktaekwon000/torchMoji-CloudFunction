# Use torchMoji to retrieve emoji most associated with the text.

import json
import numpy as np
import emoji

from torchmoji.sentence_tokenizer import SentenceTokenizer
from torchmoji.model_def import torchmoji_emojis
from torchmoji.global_variables import PRETRAINED_PATH, VOCAB_PATH
from torchmoji.emoji_maps import DEEPMOJI_MAP, EMOJI_TO_EMOTION

DEFAULT_RESPONSE = {
  "emoji0": "",
  "emoji0_emotion": "",
  "emoji1": "",
  "emoji1_emotion": "",
  "emoji2": "",
  "emoji2_emotion": "",
  "emoji3": "",
  "emoji3_emotion": "",
  "emoji4": "",
  "emoji4_emotion": ""
}

def textToEmoji(request):
  """HTTP Cloud function.
  Args: 
    request (flask.Request): The request object.
    <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
  Returns:
    The response text, or any set of values that can be turned into a
    Response object using `make_response`
    <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
  """
  request_json = request.get_json(silent=True)
  request_args = request.args

  if request_json and 'text' in request_json:
    txt = request_json['text']
  elif request_args and 'text' in request_args:
    txt = request_args['text']
  else:
    print("No text provided.")
    return DEFAULT_RESPONSE

  if not txt: 
    print("Empty text provided")
    return DEFAULT_RESPONSE

  def top_elements(array, k):
    ind = np.argpartition(array, -k)[-k:]
    return ind[np.argsort(array[ind])][::-1]
  
  maxlen = 1000
  with open(VOCAB_PATH, 'r') as f:
    vocabulary = json.load(f)
  st = SentenceTokenizer(vocabulary, maxlen)
  
  model = torchmoji_emojis(PRETRAINED_PATH)
  tokenized, _, _ = st.tokenize_sentences([txt])
  prob = model(tokenized)

  result = {}
  t_prob=prob[0]
  ind_top = top_elements(t_prob, 5).tolist()
  for i in range(5):
    key = "emoji" + str(i)
    key2 = key + "_emotion"
    result.update({key: emoji.emojize(DEEPMOJI_MAP[ind_top[i]], use_aliases=True), key2: EMOJI_TO_EMOTION[ind_top[i]]})
  
  print(result)
  return result