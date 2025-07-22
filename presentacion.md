---
marp: true
theme: rose-pine-moon
paginate: true
---

# Asistente Virtual de Voz
## Arquitectura y Funcionamiento

- Angel Rogelio
- Adai Diaz
- Carlos ...
- Alexis Sanmiguel

---

## Resumen del Sistema

- **Asistente de voz conversacional** con avatar visual
- **Comunicación en tiempo real** usando WebRTC
- **Pipeline completo**: Voz → Texto → LLM → TTS (Texto to speech) → Avatar

```python
# Flujo principal
Audio Input → STT → LLM → TTS → Avatar → Video/Audio Output
```

---

## Modelos de IA Utilizados

### **LLM: GPT-4o**
```python
gpt = openai.LLM(model="gpt-4o")
```
- Procesamiento de lenguaje natural
- Generación de respuestas conversacionales
- Personalidad del asistente

---

## Modelos de IA Utilizados

### **STT: GPT-4o-Transcribe**
```python
gpt_transcribe = openai.STT(model="gpt-4o-transcribe")
```
- Speech-to-Text de alta calidad
- Transcripción en tiempo real
- Soporte multiidioma

---

## Modelos de IA Utilizados

### **TTS: ElevenLabs**
```python
tts = elevenlabs.TTS(
    voice_id="BmccncGrL9wwIg0hRofL",
    model="eleven_multilingual_v2"
)
```
- Text-to-Speech de alta calidad
- Voz personalizada (clonación de voz)
- Modelo multilingüe

---

## Modelos de IA Utilizados

### **VAD: Silero**
```python
vad = silero.VAD.load()
```
- Voice Activity Detection
- Detecta cuando el usuario habla
- Reduce ruido de fondo

---

## Inicialización del Sistema

```python
async def entrypoint(ctx: JobContext):
    await ctx.connect()
    print(f"Room name: {ctx.room.name}")
    
    # Configuración de modelos
    gpt = openai.LLM(model="gpt-4o")
    gpt_transcribe = openai.STT(model="gpt-4o-transcribe")
    tts = elevenlabs.TTS(
        voice_id="BmccncGrL9wwIg0hRofL",
        model="eleven_multilingual_v2"
    )
    
    # Creación del agente
    agent = Agent(
        vad=silero.VAD.load(),
        llm=gpt,
        stt=gpt_transcribe,
        tts=tts,
        instructions="..." # Personalidad del asistente
    )
```

---

## Proceso de Comunicación

1. **Usuario habla** → VAD detecta actividad vocal
2. **STT procesa** → Convierte audio a texto
3. **LLM genera respuesta** → GPT-4o procesa y responde
4. **TTS sintetiza** → ElevenLabs convierte texto a audio
5. **Avatar genera video** → Simli crea video sincronizado
6. **LiveKit transmite** → WebRTC envía video/audio al cliente

---

## Casos de Uso

- **Asistentes virtuales personalizados**
- **Educación interactiva**
- **Atención al cliente automatizada**
- **Entretenimiento conversacional**
- **Interfaces de voz para aplicaciones**

