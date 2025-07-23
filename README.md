# Angel Rogelio AI

For the backend, first, create a virtual environment, update pip, and install the required packages:

```
cd ./backend

python3.12 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

You need to set up the following environment variables:

```
LIVEKIT_URL=...
LIVEKIT_API_KEY=...
LIVEKIT_API_SECRET=...
DEEPGRAM_API_KEY=...
OPENAI_API_KEY=...
SIMLI_API_KEY=...
SIMLI_FACE_ID=...
ELEVEN_API_KEY
```

Then, run the assistant:

```
python3.12 assistant.py download-files

python3.12 assistant.py start
```

For the frontend, navigate to the frontend directory and run the following commands:

```
cd ./frontend
npm install
npm run dev
```

Finally, you can load the [hosted playground](https://agents-playground.livekit.io/) and connect it.