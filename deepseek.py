import aiohttp
from hikka import loader, utils

class DeepSeekMod(loader.Module):
    """Неофициальный модуль для DeepSeek API"""
    strings = {"name": "DeepSeekHack"}

    async def deepcmd(self, message):
        """Отправь запрос в DeepSeek: .deep <вопрос>"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "❌ Введи вопрос, дебил")
            return

        API_KEY = "sk-aad8fa6fed574e95a5f6a4d4c9f7216c"  # Твой ключ (рискуешь им)
        API_URL = "https://api.deepseek.com/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": args}],
            "temperature": 0.7
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(API_URL, json=payload, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        answer = data["choices"][0]["message"]["content"]
                        await utils.answer(message, f"🤖 Ответ:\n{answer}")
                    else:
                        error = await resp.text()
                        await utils.answer(message, f"💥 Ошибка {resp.status}:\n{error}")
        except Exception as e:
            await utils.answer(message, f"🔥 Полный пиздец: {str(e)}")