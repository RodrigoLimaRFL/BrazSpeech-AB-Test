<h1> Braz Speech Accent Evaluation </h1>
<h2> Introduction </h2>
<p> This is a website designed to help the BrazSpeech project evaluate its synthetic audios with accent from all brazilian states. It has support for an ABX test, to determine if the accent is adequate, and a MOS evaluation, to rate the quality of the audio. </p>
<p> It was built using the Flask library for python. </p>
<h2> Installation </h2>
<h3> 1. Clone the repository </h3>

```
git clone https://github.com/RodrigoLimaRFL/BrazSpeech-AB-Test
```

<h3> 2. Create a virtual environment </h3>

```
cd BrazSpeechAccent/BrazSpeech_AB_Test
python -m venv .venv
source .venv/bin/activate
```

<h3> 3. Install dependencies </h3>

```
cd ..
pip install -r requirements.txt
```

<h4> 4. Run app </h4>

```
flask --app BrazSpeech_AB_Test run
```

<p> To deploy to a production server, run the folloowing code: </p>

```
uwsgi --http [IP_ADDRESS]:[PORT] --mastes -p [NUMBER_OF_PROCESSES] -w app:app
```
