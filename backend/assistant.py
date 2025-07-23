import asyncio
import os
import sys
from livekit.agents import JobContext, WorkerOptions, AgentSession, Agent, cli
from livekit.agents.voice.room_io import RoomOutputOptions
from livekit.plugins import openai, silero
from dotenv import load_dotenv
from livekit.plugins import elevenlabs

load_dotenv()

# Global variable to store the personality mode
PERSONALITY_MODE = "adaptativo"  # default 

def load_prompt(mode):
    """Load prompt based on personality mode"""
    prompt_files = {
        "grosero": "prompt_grosero.txt",
        "adaptativo": "prompt_adaptativo.txt"
    }
    
    prompt_file = prompt_files.get(mode, "prompt_grosero.txt")
    prompt_path = os.path.join(os.path.dirname(__file__), prompt_file)
    
    try:
        with open(prompt_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Warning: {prompt_file} not found, using default prompt")
        return "You are Angel Rogelio, a helpful AI assistant."

def get_initial_message(mode):
    """Get initial message based on personality mode"""
    messages = {
        "grosero": "Hola, soy Angel Rogelio, tu pinche asistente virtual, ¿Qué vergas quieres?",
        "adaptativo": "¡Hola! Soy Angel Rogelio, tu asistente virtual adaptable. Puedo ajustar mi personalidad según prefieras. ¿En qué puedo ayudarte?"
    }
    return messages.get(mode, messages["grosero"])

async def entrypoint(ctx: JobContext):
    await ctx.connect()
    print(f"Room name: {ctx.room.name}")

    gpt = openai.LLM(model="gpt-4o")
    
    gpt_transcribe = openai.STT(
        model="gpt-4o-transcribe"
    )
    
    tts=elevenlabs.TTS(
      voice_id="BmccncGrL9wwIg0hRofL",
      model="eleven_flash_v2_5"
   )
        
    agent = Agent(
        vad=silero.VAD.load(),
        llm=gpt,
        stt=gpt_transcribe,
        tts=tts,
        instructions=load_prompt(PERSONALITY_MODE),
        )
    
    session = AgentSession()

    await asyncio.sleep(5)
   
    await session.start(
        agent=agent,
        room=ctx.room,
        room_output_options=RoomOutputOptions(audio_enabled=True, transcription_enabled=True),
    )

    await session.say(get_initial_message(PERSONALITY_MODE), allow_interruptions=True)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "download-files":
        print("Downloading model files...")
        # Download Silero VAD model
        try:
            silero.VAD.load()
            print("Silero VAD model downloaded successfully")
        except Exception as e:
            print(f"Error downloading models: {e}")
            sys.exit(1)
        print("All model files downloaded successfully")
    else:
        # Check for personality mode parameter
        if len(sys.argv) > 1 and sys.argv[1] in ["grosero", "adaptativo"]:
            PERSONALITY_MODE = sys.argv[1]
            print(f"Starting with personality mode: {PERSONALITY_MODE}")
        
        cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
