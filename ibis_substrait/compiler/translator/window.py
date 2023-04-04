from __future__ import annotations

import functools

from ibis import util

from ibis_substrait.proto.substrait.ibis import algebra_pb2 as stalg


def _translate_window_bounds(
    precedes: tuple[int, int] | int | None,
    follows: tuple[int, int] | int | None,
) -> tuple[
    stalg.Expression.WindowFunction.Bound,
    stalg.Expression.WindowFunction.Bound,
]:
    # all preceding or all following or one or the other
    preceding = util.promote_list(precedes)
    following = util.promote_list(follows)

    # Change in behavior of `promote_list` in Ibis 4.x so we do this for now
    preceding = [None] if precedes is None else preceding
    following = [None] if follows is None else following

    if len(preceding) == 2:
        if following and following != [None]:
            raise ValueError(
                "`following` not allowed when window bounds are both preceding"
            )

        lower, upper = preceding
        return translate_preceding(lower), translate_preceding(upper)

    if len(preceding) != 1:
        raise ValueError(f"preceding must be length 1 or 2 got: {len(preceding)}")

    if len(following) == 2:
        if preceding and preceding != [None]:
            raise ValueError(
                "`preceding` not allowed when window bounds are both following"
            )

        lower, upper = following
        return translate_following(lower), translate_following(upper)
    elif len(following) != 1:
        raise ValueError(f"following must be length 1 or 2 got: {len(following)}")

    return translate_preceding(*preceding), translate_following(*following)


# Window Functions
@functools.singledispatch
def translate_preceding(value: int | None) -> stalg.Expression.WindowFunction.Bound:
    raise NotImplementedError()


@translate_preceding.register
def _preceding_none(_: None) -> stalg.Expression.WindowFunction.Bound:
    return stalg.Expression.WindowFunction.Bound(
        unbounded=stalg.Expression.WindowFunction.Bound.Unbounded()
    )


@translate_preceding.register
def _preceding_int(offset: int) -> stalg.Expression.WindowFunction.Bound:
    return stalg.Expression.WindowFunction.Bound(
        preceding=stalg.Expression.WindowFunction.Bound.Preceding(offset=offset)
    )


@functools.singledispatch
def translate_following(value: int | None) -> stalg.Expression.WindowFunction.Bound:
    raise NotImplementedError()


@translate_following.register
def _following_none(_: None) -> stalg.Expression.WindowFunction.Bound:
    return translate_preceding(_)


@translate_following.register
def _following_int(offset: int) -> stalg.Expression.WindowFunction.Bound:
    return stalg.Expression.WindowFunction.Bound(
        following=stalg.Expression.WindowFunction.Bound.Following(offset=offset)
    )
