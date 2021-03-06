from rete import Rule, Has, Ncc, Filter, Bind, Neg
from rete.utils import parse_xml


def test_xml():
    s = """<?xml version="1.0"?>
    <data version="0.0.2">
        <production>
            <lhs>
                <has F1="$x" F2="on" F3="$y" />
                <bind to="$test">1+1</bind>
                <filter>$y != "table"</filter>
                <ncc>
                    <has F1="$z" F2="color" F3="red" />
                    <has F1="$z" F2="on" F3="$w" />
                </ncc>
            </lhs>
            <rhs></rhs>
        </production>
    </data>"""
    result = parse_xml(s)
    assert result[0][0] == Rule(
        Has('$x', 'on', '$y'),
        Bind('1+1', '$test'),
        Filter('$y != "table"'),
        Ncc(Has('$z', 'color', 'red'),
            Has('$z', 'on', '$w')))
