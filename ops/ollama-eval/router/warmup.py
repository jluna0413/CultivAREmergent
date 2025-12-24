import asyncio
import httpx

OLLAMA = "http://127.0.0.1:11436/v1"

WARMUP_PROMPTS = [
    {"model": "gemma3:1b", "prompt": "Please respond with the single word: alive", "temperature": 0.0},
    {"model": "gemma3:270m", "prompt": "Please respond with the single word: alive", "temperature": 0.0},
    {"model": "cogito:3b-v1-preview-llama-q4_K_M", "prompt": "Please respond with the single word: alive", "temperature": 0.0}
]

async def warm_one(client, spec):
    url = OLLAMA.rstrip('/') + '/completions'
    try:
        r = await client.post(url, json={"model": spec['model'], "prompt": spec['prompt'], "max_tokens": 8, "temperature": spec.get('temperature',0.0)})
        print(spec['model'], r.status_code)
    except Exception as e:
        print('warmup error', spec['model'], e)

async def main():
    async with httpx.AsyncClient(timeout=10) as client:
        await asyncio.gather(*(warm_one(client, s) for s in WARMUP_PROMPTS))

if __name__ == '__main__':
    asyncio.run(main())
