"""
Tests for the domain's original, pre-existing directives and roles
(class/method/staticmethod/classmethod/attribute/alias/exception/
module/function/data/currentmodule, cross-references, inheritance
linking, method modifiers, duplicate-object warning, module index).

The class/method/staticmethod/inheritance/alias/module/function fixtures
are the project's own documented examples (copied verbatim from
README.rst), not invented ones.
"""
import pytest
from sphinx import addnodes


def _objects(app):
    return app.env.domaindata['lua']['objects']


@pytest.mark.sphinx('html', testroot='lua-domain-core')
def test_class_attribute_method_staticmethod_classmethod_registered(app):
    app.build()
    objects = _objects(app)
    assert objects['pl.List'][1] == 'class'
    assert objects['pl.List.size'][1] == 'attribute'
    assert objects['pl.List.append'][1] == 'method'
    assert objects['pl.List.fromArray'][1] == 'staticmethod'
    assert objects['pl.List.default'][1] == 'classmethod'


@pytest.mark.sphinx('html', testroot='lua-domain-core')
def test_class_inheritance_links_base_class(app):
    app.build()
    content = (app.outdir / 'index.html').read_text()
    # `.. lua:class:: Car: ITransport` must link Car's base to ITransport
    assert (
        '<a class="reference internal" href="#ITransport" title="ITransport">'
        '<span>ITransport</span>'
    ) in content or 'href="#ITransport"' in content


@pytest.mark.sphinx('html', testroot='lua-domain-core')
def test_method_modifiers_reflected_in_prefix(app):
    app.build()
    doctree = app.env.get_doctree('index')
    for node in doctree.findall(addnodes.desc_signature):
        if node.get('fullname') == 'foo':
            prefix = ''.join(
                n.astext() for n in node.findall(addnodes.desc_annotation)
            )
            # get_signature_prefix only renders virtual/protected/abstract;
            # :deprecated: is accepted as an option but not shown in the
            # prefix text (pre-existing behavior).
            for modifier in ('virtual', 'abstract', 'protected'):
                assert modifier in prefix
            return
    raise AssertionError('foo() signature not found')


@pytest.mark.sphinx('html', testroot='lua-domain-core')
def test_module_and_function_and_data_registered(app):
    app.build()
    objects = _objects(app)
    assert 'pl.path' in app.env.domaindata['lua']['modules']
    assert objects['pl.path.join'][1] == 'function'
    assert objects['pl.path.sep'][1] == 'data'


@pytest.mark.sphinx('html', testroot='lua-domain-core')
def test_currentmodule_qualifies_without_registering_a_module(app):
    app.build()
    objects = _objects(app)
    assert objects['pl.dir.makepath'][1] == 'function'
    # currentmodule must not create a module page of its own
    assert 'pl.dir' not in app.env.domaindata['lua']['modules']


@pytest.mark.sphinx('html', testroot='lua-domain-core')
def test_currentmodule_none_clears_context(app):
    app.build()
    objects = _objects(app)
    # PathError declared after `.. lua:currentmodule:: None` must not be
    # qualified by the previously-active pl.dir module
    assert 'PathError' in objects
    assert objects['PathError'][1] == 'exception'


@pytest.mark.sphinx('html', testroot='lua-domain-core')
def test_alias_preserves_generic_type_verbatim(app):
    app.build()
    doctree = app.env.get_doctree('index')
    for node in doctree.findall(addnodes.desc_signature):
        if node.get('alias') == 'Packet':
            assert node['type_alias'] == 'table<string, number>'
            return
    raise AssertionError('Packet alias signature not found')


@pytest.mark.sphinx('html', testroot='lua-domain-core')
def test_cross_reference_roles_resolve(app):
    app.build()
    content = (app.outdir / 'index.html').read_text()
    assert '<a class="reference internal" href="#pl.List" title="pl.List">' in content
    assert (
        '<a class="reference internal" href="#pl.List.append" '
        'title="pl.List.append">'
    ) in content


@pytest.mark.sphinx('html', testroot='lua-domain-core')
def test_module_index_lists_registered_modules(app):
    app.build()
    index_cls = app.env.domains['lua'].indices[0]
    content, collapse = index_cls(app.env.domains['lua']).generate()
    all_entries = [entry[0] for _, entries in content for entry in entries]
    assert 'pl.path' in all_entries


@pytest.mark.sphinx('html', testroot='lua-domain-duplicate', freshenv=True)
def test_duplicate_object_description_warns(app):
    app.build()
    warnings = app._warning.getvalue()
    assert 'duplicate object description of pl.path.join' in warnings
