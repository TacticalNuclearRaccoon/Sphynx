import requests
import streamlit as st
import pandas as pd
import openai

from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


restart_sequence = "\n"

dys= """Dysfonctionnement: L'équipe n'ose pas.\n
La question dichotomique détecter: Avez-vous le sentiment d'être bloqué ou de ne pas pouvoir prendre des initiatives?\n

---
Dysfonctionnement:{input}\n
---
La question dichotomique détecter: """


def set_openai_key(key):
    """Sets OpenAI key."""
    openai.api_key = key

class GeneralModel:
    def __init__(self):
        print("Model Intilization--->")
        # set_openai_key(API_KEY)

    def query(self, prompt, myKwargs={}):
        """
        wrapper for the API to save the prompt and the result
        """

        # arguments to send the API
        kwargs = {
            "engine": "text-davinci-003",
            "temperature": temp,
            "max_tokens": 500,
            "best_of": 1,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "stop": ["\n"],
        }


        for kwarg in myKwargs:
            kwargs[kwarg] = myKwargs[kwarg]
            
        r = openai.Completion.create(prompt=prompt, **kwargs)["choices"][0][
            "text"
        ].strip()
        return r

    def model_prediction(self, input, api_key):
        """
        wrapper for the API to save the prompt and the result
        """
        # Setting the OpenAI API key got from the OpenAI dashboard
        set_openai_key(api_key)
        output = self.query(dys.format(input = input))
        
        return output



def app():

    # Creating an object of prediction service
    pred = GeneralModel()
    result =[]
    api_key = st.sidebar.text_input("APIkey", type="password")
    # Using the streamlit cache
    @st.cache(allow_output_mutation=True)
   
    def process_prompt(input):

        return pred.model_prediction(input=input.strip() , api_key=api_key)

    if api_key:

        s_example = "En l'absence d'un membre, l'équipe est fortement ralentie. "
        input = st.text_area(
            "Le dysfonctionnement : ",
            value=s_example,
            max_chars=100,
            height=200,
        )
        

        if st.button("Submit"):
            with st.spinner(text="In progress"):
                report_text = process_prompt(input)
                st.markdown(report_text)
                
                result.append({"dys": input, "question": report_text})
                st.dataframe(data=result)
                output = pd.DataFrame(result)
                out = output.to_csv(index=False).encode('utf-8')
                st.download_button(label="Click to Download",
                                   data=out,
                                   file_name="template.csv",
                                   mime="text/csv")
    else:
        st.error("🔑 Please enter API Key")

header = st.container()
features = st.container()

with header:
    st.title("Sphynx")
    st.text('Le génértateur de questions')
    

    temp = st.select_slider(
    'Température du modèle',
    options=[0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.22, 0.24, 0.26, 0.28, 0.3,
             0.32, 0.34, 0.36, 0.38, 0.4, 0.42, 0.44, 0.46, 0.48, 0.5,
            0.52, 0.54, 0.56, 0.58, 0.6, 0.62, 0.64, 0.66, 0.68, 0.7,
             0.72, 0.74, 0.76, 0.78, 0.8, 0.82, 0.84, 0.86, 0.88, 0.9, 1, 1.02, 1.04, 1.06, 1.08, 1.1,
             1.2, 1.22, 1.24, 1.26, 1.28, 1.3, 1.32, 1.34, 1.36, 1.38, 1.4,
             1.42, 1.44, 1.46, 1.48, 1.5])
    st.write('La température choisie', temp)

    app()
    

with features:
    
    lottie_url_hello = "https://assets7.lottiefiles.com/packages/lf20_hjgzcyui.json"
    #lottie_url_download = "https://assets4.lottiefiles.com/private_files/lf30_t26law.json"
    lottie_hello = load_lottieurl(lottie_url_hello)
    #lottie_download = load_lottieurl(lottie_url_download)
    
    
    st_lottie(lottie_hello, key="hello")




