import json

import click


@click.command()
@click.option('-f')
def jsonconv(f):
    with open(f, 'r+') as fo2:
        json.dump(json.loads(fo2.read().replace('\\xf9', '\\t')), fo2, ensure_ascii=False)
        print('OK WRITING!')


jsonconv()
