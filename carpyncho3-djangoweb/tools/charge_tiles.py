from carpyncho.navigator import models

names = ["b{}".format(n) for n in range(201, 397)]


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

names = list(chunks(names, 14))

names = list(map(lambda n: list(reversed(n)), names))

names = list(reversed(names))

for idx_row, row in enumerate(names):
    for idx_col, name in enumerate(row):
        models.Tile.objects.create(
            name=name, row=idx_row, column=idx_col)



print(names)

