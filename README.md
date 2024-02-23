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

<h3> 4. Add credentials </h3>

```
cd static
mkdir json
cd json
touch credentials.json
```
<p> Then, add all desired credentials to the json file, as per this example: </p>

```
{
    "accounts": [
        {
            "username": "email@email.com",
            "password": "password",
            "xab_number": 1,
            "mos_number": 1
        },
        {
            "username": "email2@email.com",
            "password": "password2",
            "xab_number": 2,
            "mos_number": 2
        },
    ]
}
```

<p> "username" refers to the users email, "password" refers to their password, "xab_number" refers to their current ABX test and "mos_number" refers to their current MOS questionaire. </p>

<h3> 5. Create csv </h3>

```
cd ../../csv
```

Within the folder, edit the createCsv.py file with the current credentials and desired number of tests, then run with:

```
python createCSV.py
```

<h3> 6. Run app </h4>

```
cd ../..
flask --app BrazSpeech_AB_Test run
```

<p> To deploy to a production server, run the folloowing code: </p>

```
uwsgi --http [IP_ADDRESS]:[PORT] --master -p [NUMBER_OF_PROCESSES] -w app:app
```
