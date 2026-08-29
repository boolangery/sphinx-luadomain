"""
Tests exercise the `sphinxcontrib.luadomain` extension against real
signatures/behavior transcribed from the official Lua 5.4 Reference Manual
(https://www.lua.org/manual/5.4/manual.html), rather than invented examples.
See tests/roots/test-lua-domain/index.rst for the source citations.
"""
import pytest
from sphinx import addnodes

from sphinxcontrib.luadomain import _split_top_level_types


def test_split_top_level_types_simple():
    assert _split_top_level_types('integer') == ['integer']


def test_split_top_level_types_multi_return():
    # Lua manual §6.7 math.modf: "Returns the integral part of x and the
    # fractional part of x."
    assert _split_top_level_types('number, number') == ['number', 'number']


def test_split_top_level_types_keeps_generic_brackets_intact():
    # existing `.. lua:alias:: Bar = table<string, number>` convention:
    # the inner comma must not be split.
    assert _split_top_level_types('table<string, number>') == ['table<string, number>']


def _find_signature(doctree, fullname):
    for node in doctree.findall(addnodes.desc_signature):
        if node.get('fullname') == fullname:
            return node
    raise AssertionError('no desc_signature with fullname=%r' % fullname)


def _return_targets(sig_node):
    returns = list(sig_node.findall(addnodes.desc_returns))
    assert len(returns) == 1
    return [x['reftarget'] for x in returns[0].findall(addnodes.pending_xref)]


@pytest.mark.sphinx('html', testroot='lua-domain')
def test_multi_return_split_in_string_find_signature(app):
    app.build()
    doctree = app.env.get_doctree('index')
    sig_node = _find_signature(doctree, 'string.find')
    assert _return_targets(sig_node) == ['integer', 'integer']


@pytest.mark.sphinx('html', testroot='lua-domain')
def test_multi_return_split_in_math_modf_signature(app):
    app.build()
    doctree = app.env.get_doctree('index')
    sig_node = _find_signature(doctree, 'math.modf')
    assert _return_targets(sig_node) == ['number', 'number']


@pytest.mark.sphinx('html', testroot='lua-domain')
def test_rtype_field_splits_multi_return_types(app):
    app.build()
    doctree = app.env.get_doctree('index')
    sig_node = _find_signature(doctree, 'string.find')
    # walk up to the whole object description, :rtype: is a sibling field
    desc = sig_node.parent
    field_bodies = [n.astext() for n in desc.findall(addnodes.desc_content)]
    assert any('integer' in body for body in field_bodies)
    xrefs = list(desc.findall(addnodes.pending_xref))
    rtype_targets = [x['reftarget'] for x in xrefs if x['reftarget'] == 'integer']
    # two from the signature `-> integer, integer`, two from `:rtype:`
    assert len(rtype_targets) == 4


@pytest.mark.sphinx('html', testroot='lua-domain')
def test_metamethod_registered_and_return_type_links(app):
    app.build()
    objects = app.env.domaindata['lua']['objects']
    assert objects['Vector.__add'][1] == 'metamethod'

    content = (app.outdir / 'index.html').read_text()
    # the __add metamethod's "-> Vector" return type must resolve to the
    # documented Vector class, not render as plain unlinked text
    assert (
        '<a class="reference internal" href="#Vector" title="Vector">'
        '<span class="pre">Vector</span></a>'
    ) in content


@pytest.mark.sphinx('html', testroot='lua-domain', freshenv=True)
def test_unknown_metamethod_name_warns(app):
    app.build()
    warnings = app._warning.getvalue()
    assert '__ad' in warnings
    assert 'not a known Lua metamethod' in warnings


@pytest.mark.sphinx('html', testroot='lua-domain', freshenv=True)
def test_known_metamethod_name_does_not_warn(app):
    app.build()
    warnings = app._warning.getvalue()
    assert "'__add'" not in warnings
