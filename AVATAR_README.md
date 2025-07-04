# Avatar Integration Guide

This guide explains how to use the avatar functionality with your LiveKit assistant.

## Overview

The avatar integration uses Simli AI to provide a visual avatar that lip-syncs with the assistant's speech. The system consists of:

1. **dispatcher.py** - FastAPI service that manages avatar worker processes
2. **simli_avatar_runner.py** - The avatar worker that handles Simli integration
3. **assistant.py** - Main assistant with avatar support
4. **start_avatar.sh** - Convenience script to start everything

## Environment Variables

Make sure your `.env` file includes these variables:

```bash
# LiveKit credentials
LIVEKIT_URL=wss://your-livekit-server.com
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret

# OpenAI for LLM
OPENAI_API_KEY=your-openai-key

# Simli AI for avatar
SIMLI_API_KEY=your-simli-api-key
SIMLI_FACE_ID=your-face-id
```

## Quick Start

### Option 1: Use the convenience script (recommended)
```bash
./start_avatar.sh
```

### Option 2: Manual startup
```bash
# Terminal 1 - Start the avatar dispatcher
python3 dispatcher.py

# Terminal 2 - Start the main assistant
python3 assistant.py start
```

## How It Works

1. When the assistant starts, it attempts to connect to the avatar dispatcher at `http://localhost:8089/launch`
2. If successful, the dispatcher launches a Simli avatar worker process
3. The assistant routes its audio output to the avatar worker instead of directly to the room
4. The avatar worker receives the audio, sends it to Simli, and streams back the lip-synced video
5. If the avatar fails to launch, the assistant falls back to audio-only mode

## Features

- **Automatic fallback**: If avatar service is unavailable, assistant works normally with audio only
- **Lip-sync**: Avatar mouth movements match the assistant's speech
- **Real-time**: Low-latency video streaming
- **Process management**: Dispatcher automatically manages avatar worker lifecycle

## Troubleshooting

### Avatar not appearing
1. Check that dispatcher is running on port 8089
2. Verify SIMLI_API_KEY and SIMLI_FACE_ID are set correctly
3. Check network connectivity to Simli services

### Audio issues
1. Ensure your TTS service (Kokoro) is running on localhost:8880
2. Check CUDA drivers if using GPU for faster-whisper

### Performance
- Avatar video is 512x512 at 30fps
- Adjust video settings in `simli_avatar_runner.py` if needed
- Consider using smaller faster-whisper model for lower latency

## Customization

### Change avatar face
1. Get a new face ID from [Simli Dashboard](https://app.simli.com)
2. Update SIMLI_FACE_ID in your .env file

### Modify video settings
Edit the `AvatarOptions` in `simli_avatar_runner.py`:
```python
avatar_options = AvatarOptions(
    video_width=512,    # Adjust resolution
    video_height=512,
    video_fps=30,       # Adjust framerate
    audio_sample_rate=48000,
    audio_channels=2,
)
```
