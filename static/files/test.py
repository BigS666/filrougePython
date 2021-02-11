import os
import magic


print(magic.from_file("static/files/downld08.pdf"))
print(magic.from_file("static/files/downld08.pdf", mime=True))
print(magic.from_buffer(open("static/files/downld08.pdf", "rb").read(2048)))