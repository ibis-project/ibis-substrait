# [Ibis](https://ibis-project.org) + [Substrait](https://substrait.io)

This repo houses the Substrait compiler for ibis.

We're just getting started here, so stay tuned!

# Usage

```python
>>> import ibis

>>> t = ibis.table(
    [("a", "string"), ("b", "float"), ("c", "int32"), ("d", "int64"), ("e", "int64")],
    "t",
)

>>> expr = t.group_by(["a", "b"]).aggregate([t.c.sum().name("sum")]).select("b", "sum")
>>> expr
r0 := UnboundTable: t
  a string
  b float64
  c int32
  d int64
  e int64

r1 := Aggregation[r0]
  metrics:
    sum: Sum(r0.c)
  by:
    a: r0.a
    b: r0.b

Selection[r1]
  selections:
    b:   r1.b
    sum: r1.sum


>>> ibis.show_sql(expr)
SELECT
  t0.b,
  t0.sum
FROM (
  SELECT
    t1.a AS a,
    t1.b AS b,
    SUM(t1.c) AS sum
  FROM t AS t1
  GROUP BY
    t1.a,
    t1.b
) AS t0

>>> from ibis_substrait.compiler.core import SubstraitCompiler

>>> compiler = SubstraitCompiler()

>>> proto = compiler.compile(expr)
```
