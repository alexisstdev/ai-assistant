import asyncio
import os
from livekit.agents import JobContext, WorkerOptions, AgentSession, Agent, cli
from livekit.agents.voice.room_io import RoomOutputOptions
from livekit.plugins import openai, silero
from dotenv import load_dotenv
from livekit.plugins import elevenlabs

load_dotenv()

def load_prompt(prompt_file="prompt_grosero.txt"):
    prompt_path = os.path.join(os.path.dirname(__file__), prompt_file)
    try:
        with open(prompt_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Warning: {prompt_file} not found, using default prompt")
        return "You are Angel Rogelio, a helpful AI assistant."

async def entrypoint(ctx: JobContext):
    await ctx.connect()
    print(f"Room name: {ctx.room.name}")

    gpt = openai.LLM(model="gpt-4o")
    
    gpt_transcribe = openai.STT(
        model="gpt-4o-transcribe"
    )
    
    tts=elevenlabs.TTS(
      voice_id="BmccncGrL9wwIg0hRofL",
      model="eleven_multilingual_v2"
   )
        
    agent = Agent(
        vad=silero.VAD.load(),
        llm=gpt,
        stt=gpt_transcribe,
        tts=tts,
        instructions=load_prompt(),
        )
    
    session = AgentSession()

    await asyncio.sleep(5)
   
    await session.start(
        agent=agent,
        room=ctx.room,
        room_output_options=RoomOutputOptions(audio_enabled=True, transcription_enabled=True),
    )

    await session.say("Hola, soy Angel Rogelio, tu pinche asistente virtual, ¿Qué vergas quieres?", allow_interruptions=True)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
