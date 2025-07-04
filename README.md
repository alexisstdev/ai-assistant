# LiveKit Assistant

First, create a virtual environment, update pip, and install the required packages:

```
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

export LD_LIBRARY_PATH=`python3 -c 'import os; import nvidia.cublas.lib; import nvidia.cudnn.lib; print(os.path.dirname(nvidia.cublas.lib.__file__) + ":" + os.path.dirname(nvidia.cudnn.lib.__file__))'`

python3.12 assistant.py start
```

Finally, you can load the [hosted playground](https://agents-playground.livekit.io/) and connect it.