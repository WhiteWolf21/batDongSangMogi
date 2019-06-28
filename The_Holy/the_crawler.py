import settings
from modules.crawl.sign_in import sign_in

def main():
    for page in settings.GROUPS:
        sign_in(page)

if __name__ == "__main__":
    main()
