EXTENSIONS = [".jpg", ".png", ".pdf", ".docx", ".doc", ".xlsx", ".xls", ".txt"]


async def is_file_url(url: str) -> bool:
    return any(extension in url for extension in EXTENSIONS)
