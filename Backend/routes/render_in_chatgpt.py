import uuid
import requests
import os
import subprocess
from playwright.async_api import async_playwright

def ensure_chromium_installed():
    """
    Проверяет, установлен ли Chromium для Playwright.
    Если нет — автоматически устанавливает его.
    """
    browser_path = os.path.expanduser("~/.cache/ms-playwright/chromium-1161/chrome-linux/chrome")
    if not os.path.exists(browser_path):
        print("🚀 Chromium не найден, запускаем установку...")
        try:
            subprocess.run(["playwright", "install", "chromium"], check=True)
            print("✅ Chromium установлен.")
        except subprocess.CalledProcessError as e:
            print("❌ Ошибка установки Chromium:", e)
            raise RuntimeError("Не удалось установить Chromium для Playwright")

async def render_in_chatgpt(image_urls: list[str]) -> str:
    ensure_chromium_installed()  # Добавлена проверка перед запуском

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # или True для сервера
        context = await browser.new_context(storage_state="/www/wwwroot/********/chkaf/routes/cookies.json")
  # авторизованная сессия
        page = await context.new_page()

        print("Открываем ChatGPT...")
        await page.goto("https://chat.openai.com/chat")

        # Ждём поле ввода
        await page.wait_for_selector("textarea")

        # Вводим промпт
        await page.locator("textarea").fill("Please generate a mannequin wearing these clothes.")
        await page.keyboard.press("Enter")

        # Ждём поле загрузки
        print("Загружаем изображения...")
        for image_url in image_urls:
            file_name = f"/tmp/{uuid.uuid4()}.jpg"
            with open(file_name, "wb") as f:
                f.write(requests.get(image_url).content)

            input_elem = await page.query_selector('input[type="file"]')
            if input_elem:
                await input_elem.set_input_files(file_name)

        # Ждём ответа от ChatGPT (где появится изображение)
        print("Ожидание генерации изображения...")
        await page.wait_for_selector("img", timeout=120000)  # 2 минуты

        # Получаем первую картинку
        image_elem = await page.query_selector("img")
        image_url = await image_elem.get_attribute("src")

        await browser.close()
        print(f"Изображение получено: {image_url}")
        return image_url
