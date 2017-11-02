import lupa

from lupa import LuaRuntime
lua = LuaRuntime(unpack_returned_tuples=True)

_ = lua.require("lua-parser.parser")

print("ok")

