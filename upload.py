import argparse
import sys
import uuid

from sqlalchemy import create_engine

CONN_STR = """postgresql://codephil:codephil!@lavazares-db1.cnodp99ehkll.us-west-2.rds.amazonaws.com:5432/lavazaresdb"""

parser = argparse.ArgumentParser()
engine = create_engine(CONN_STR)
conn = engine.connect()


class GameContentTypes():
    """
    Game content types.
    PSQL Requires commas to be doubled ie. Won't -> Won''t
    """
    WORD = "word"
    SENTENCE = "sentence"
    PASSAGE = "passage"


def upload_content_from_file(file_path, upload_type):
    with open(file_path) as file:
        if upload_type == GameContentTypes.WORD:
            words = newline_splitter(file)
            word_uploader(words)
        elif upload_type == GameContentTypes.SENTENCE:
            sentences = newline_splitter(file)
            sentence_uploader(sentences)
        else:
            passages = passage_splitter(file)
            passage_uploader(passages)


def newline_splitter(file):
    return [line.rstrip('\n') for line in file]


def passage_splitter(file):
    """// is the delimiter
    line right after // is the title of the passage
    everything else after that is the body of the passage
    """
    data = file.read().split("//")[1:]
    passages = []
    for passage in data:
        lines = passage.splitlines()[1:]
        passage_content = {}
        passage_content["name"] = lines[0]
        passage_content["body"] = "".join(lines[1:])
        passages.append(passage_content)

    return passages


def passage_uploader(passages):
    for passage in passages:
        conn.execute(
            """INSERT INTO game_content(id, content, title, type)
            VALUES('{}', '{}', '{}', '{}')
            """.format(
                uuid.uuid4(),
                passage["body"],
                passage["name"],
                GameContentTypes.PASSAGE
            )
        )


def word_uploader(words):
    for word in words:
        conn.execute(
            """INSERT INTO game_content(id, content, type)
            VALUES('{}', '{}', '{}')
            """.format(uuid.uuid4(), word, GameContentTypes.WORD)
        )


def sentence_uploader(sentences):
    for sentence in sentences:
        conn.execute(
            """INSERT INTO game_content(id, content, type)
            VALUES('{}', '{}', '{}')
            """.format(uuid.uuid4(), sentence, GameContentTypes.SENTENCE)
        )


if __name__ == "__main__":
    parser.add_argument("-f", "--filepath", help="Path of file to upload")
    parser.add_argument("-t", "--type", help="Content type being uploaded")

    args = parser.parse_args()
    if (
        args.type != GameContentTypes.WORD
        and args.type != GameContentTypes.SENTENCE
        and args.type != GameContentTypes.PASSAGE
    ):
        print("Invalid GameContentType")
        sys.exit(1)

    upload_content_from_file(args.filepath, args.type)
