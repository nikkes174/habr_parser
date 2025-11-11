from parsing_service import HTMLParser


def main():
    parser = HTMLParser(None, None)
    parser.input_url()
    parser.input_selector()
    parser.get_result()


if __name__ == '__main__':
    main()
