# Metamethod directive + multi-return xref-linking

Date: 2026-08-29
Status: approved

## Context

Gap review of `sphinxcontrib/luadomain.py` against the official Lua 5.4
reference manual (https://www.lua.org/manual/5.4/manual.html) found two
missing features:

1. No directive exists for documenting metamethods (`__add`, `__index`,
   `__call`, etc. — listed in manual §2.4 "Metatables and Metamethods").
2. Multi-value returns (e.g. `string.find` returning start+end indices,
   `math.modf` returning integral+fractional parts) render as one flat,
   unlinked text blob in both the signature `-> t1, t2` line and the
   `:rtype:` field body, instead of per-value cross-referenced types.

Reference data pulled verbatim from the manual (MIT-licensed, reproduction
with credit permitted — https://www.lua.org/license.html):

- Metamethods (§2.4): `__add`, `__sub`, `__mul`, `__div`, `__mod`, `__pow`,
  `__unm`, `__idiv`, `__band`, `__bor`, `__bxor`, `__bnot`, `__shl`, `__shr`,
  `__concat`, `__len`, `__eq`, `__lt`, `__le`, `__index`, `__newindex`,
  `__call`, plus `__gc`, `__close`, `__mode`, `__name` (26 total).
- Multi-return stdlib functions used as test fixtures: `string.find (s,
  pattern [, init [, plain]])`, `table.unpack (list [, i [, j]])`,
  `math.modf (x)`, `next (table [, index])`, `pcall (f [, arg1, ···])`.

## Design

### 1. Shared helper — `_split_top_level_types(s)`

Splits a type string on commas that are not nested inside `()`, `[]`,
`<>`, or `{}`. Required because the domain already supports generic-alias
syntax such as `table<string, number>` (`.. lua:alias::`) whose inner
comma must not be split. Pure function — testable without a Sphinx build.

### 2. Multi-return / union xref-linking in fields

`LuaField` and `LuaTypedField` currently just inherit `Field`/`TypedField`
unchanged. Override `make_xrefs` on both to split the target via the
helper and emit one clickable `pending_xref` per type, joined by `", "`
text nodes. This is a single fix point that covers:

- `:rtype:` (currently would try to resolve `"integer, integer"` as one
  broken xref target)
- `:type:` / `:paramtype:` (bonus: fixes union parameter types too)

### 3. Multi-return xref-linking in the signature arrow

`LuaObject.handle_signature` currently does
`sig_node += addnodes.desc_returns(ret_ann, ret_ann)` — flat text. Replace
with a helper that splits `ret_ann` via `_split_top_level_types` and
builds a `desc_returns` node containing one `pending_xref` per type
(`refdomain='lua', reftype='obj'`), joined by `, ` text nodes — mirroring
the existing base-class-linking pattern in `LuaClassLike.handle_signature`.
Applies to every subclass of `LuaObject` (function/method/staticmethod/
classmethod/metamethod) since they all funnel through this method.

### 4. `metamethod` directive

- `KNOWN_LUA_METAMETHODS`: frozenset of the 26 names above, defined near
  the top of `luadomain.py` with a comment citing the manual URL/section.
- `LuaDomain.object_types['metamethod'] = ObjType(_('metamethod'), 'meth', 'obj')`
  and `LuaDomain.directives['metamethod'] = LuaClassMember` — same pattern
  as method/staticmethod/classmethod, reusing the `meth` role.
- `LuaClassMember.get_signature_prefix` gains a `metamethod` branch
  returning `'metamethod '`; `get_index_text` gains a matching branch
  returning `'%s (metamethod)'`.
- `LuaClassMember.handle_signature` override: call `super().handle_signature(...)`,
  then if `self.objtype == 'metamethod'` and the bare method name isn't in
  `KNOWN_LUA_METAMETHODS`, emit a warning via
  `self.state_machine.reporter.warning(...)` — same style as the existing
  duplicate-object-description warning already in this file.

### 5. Testing

No test infrastructure exists yet in this repo. Add:

- `tests/conftest.py` registering `pytest_plugins = 'sphinx.testing.fixtures'`
- `tests/roots/test-lua-domain/` — a minimal Sphinx test project
  (`conf.py` + `index.rst`) whose fixture RST embeds the **verbatim
  official signatures/descriptions** fetched above for `string.find`,
  `table.unpack`, `math.modf` (multi-return case) and the **official
  metamethod names** for the metamethod directive (including one
  deliberately misspelled name, e.g. `__ad`, to assert the validation
  warning fires) — each fixture carries a comment citing its manual
  source/section instead of inventing signatures.
- `tests/test_luadomain.py`: builds the test app (`app.build()`) and
  asserts against the resulting doctree/env:
  - `pending_xref` nodes exist with the correct `reftarget` for each
    split return type (both signature-arrow and `:rtype:` cases)
  - the metamethod object is registered in `app.env.domaindata['lua']['objects']`
    under objtype `'metamethod'`
  - `app._warning.getvalue()` contains the expected warning text for the
    deliberately-misspelled metamethod case, and does NOT for valid ones
- `requirements-test.txt` (new file, `pytest` + `Sphinx` already a runtime
  dep) — kept separate from `setup.py` since this repo has no
  `extras_require`/`pyproject.toml` yet and this is out of scope to add.

## Out of scope

- No pyproject.toml / extras_require restructuring.
- No CI workflow file (not requested).
- No changes to existing directives' behavior beyond the two additive
  fixes above (no rename/removal of existing objtypes or roles).
