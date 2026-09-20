"""RED before GREEN: the declared normalisation and the number grammar.

Every fixture string here is one the task named, or one the capture actually
holds. Written before ``normalise.py`` existed.
"""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path
import sys

import pytest

HERE = Path(__file__).resolve().parent

# This cell's own module, the way bridge-01 and fault-injection-02 reach
# theirs. The paper gate collects paper-v4/experiment-v4 as a directory and
# runs pytest from the repository root, so a bare import does not resolve.
sys.path.insert(0, str(HERE))

import normalise  # noqa: E402


# ---------------------------------------------------------------------------
# The normaliser
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("ﬀ", "ff"),
        ("ﬁ", "fi"),
        ("ﬂ", "fl"),
        ("ﬃ", "ffi"),
        ("ﬄ", "ffl"),
        ("ﬅ", "st"),
        ("ﬆ", "st"),
        ("ﬁve", "five"),
        ("conﬁrmed", "confirmed"),
    ],
)
def test_the_seven_ligatures_become_their_letters(raw, expected):
    assert normalise.normalise(raw) == expected


def test_a_hyphen_space_break_inside_a_word_closes():
    assert normalise.normalise("sig- ni") == "signi"
    assert normalise.normalise("signi-\nficant") == "significant"


def test_a_hyphen_between_two_words_survives():
    assert normalise.normalise("mid-atlantic") == "mid-atlantic"


def test_a_spaced_decimal_point_closes():
    assert normalise.normalise("1 . 5") == "1.5"
    assert normalise.normalise("1. 5") == "1.5"
    assert normalise.normalise("1 .5") == "1.5"


def test_a_space_inside_a_digit_run_closes():
    assert normalise.normalise("1 5 0") == "150"


def test_letter_to_digit_gluing_is_the_glued_profile_only():
    assert normalise.normalise("CO 2", profile=normalise.GLUED) == "co2"
    assert normalise.normalise("CO 2", profile=normalise.UNGLUED) == "co 2"
    assert normalise.normalise("H 2O", profile=normalise.GLUED) == "h2o"


def test_gluing_is_letter_to_digit_only_and_never_digit_to_letter():
    assert normalise.normalise("H 2 O", profile=normalise.GLUED) == "h2 o"


def test_gluing_also_closes_an_honest_standalone_number():
    """Recorded, not repaired: this is why both profiles are measured."""

    assert normalise.normalise("at 1 km", profile=normalise.GLUED) == "at1 km"
    assert normalise.normalise("at 1 km", profile=normalise.UNGLUED) == "at 1 km"


def test_whitespace_runs_collapse_and_the_ends_are_stripped():
    assert normalise.normalise("  a\t\n\r\v\f  b  ") == "a b"


def test_case_folds():
    assert normalise.normalise("MgO") == "mgo"


def test_the_default_profile_is_glued():
    assert normalise.normalise("CO 2") == normalise.normalise(
        "CO 2", profile=normalise.GLUED
    )


def test_the_profiles_are_the_two_declared_names():
    assert normalise.PROFILES == (normalise.GLUED, normalise.UNGLUED)


# ---------------------------------------------------------------------------
# The number grammar
# ---------------------------------------------------------------------------


def numbers(text, profile=None, attached=False):
    kwargs = {"attached": attached}
    if profile is not None:
        kwargs["profile"] = profile
    return normalise.numbers_in(text, **kwargs)


def test_a_plain_integer_is_parsed():
    assert Decimal("991") in numbers("a value of 991 metres")


def test_a_decimal_is_parsed():
    assert Decimal("1.5") in numbers("a value of 1.5")


def test_a_spaced_decimal_is_parsed_after_normalisation():
    assert Decimal("1.5") in numbers("a value of 1 . 5")


def test_an_integral_float_equals_its_integer_spelling():
    assert normalise.as_decimal(991.0) == Decimal("991")
    assert normalise.as_decimal(991.0) in numbers("a value of 991")


def test_a_trailing_zero_decimal_equals_its_shorter_spelling():
    assert normalise.as_decimal(1.50) in numbers("a value of 1.5")


def test_a_negative_number_is_parsed_with_its_sign():
    assert Decimal("-5") in numbers("a shift of -5 units")


def test_an_en_dash_range_is_two_ends_and_never_a_sign():
    parsed = numbers("between 1.5–2.0 kilometres")
    assert Decimal("1.5") in parsed
    assert Decimal("2.0") in parsed
    assert Decimal("-2.0") not in parsed


def test_an_em_dash_range_is_two_ends():
    parsed = numbers("between 10—20")
    assert Decimal("10") in parsed and Decimal("20") in parsed
    assert Decimal("-20") not in parsed


def test_a_word_range_is_two_ends():
    parsed = numbers("from 10 to 20 kilometres")
    assert Decimal("10") in parsed and Decimal("20") in parsed


def test_plus_or_minus_yields_four_numbers():
    parsed = numbers("4.5 ± 0.3")
    for expected in ("4.5", "0.3", "4.2", "4.8"):
        assert Decimal(expected) in parsed, expected


def test_plus_or_minus_survives_the_text_layer_spacing():
    parsed = numbers("1 . 5 ± 0 . 2")
    for expected in ("1.5", "0.2", "1.3", "1.7"):
        assert Decimal(expected) in parsed, expected


@pytest.mark.parametrize(
    ("word", "value"),
    [
        ("zero", 0),
        ("one", 1),
        ("two", 2),
        ("three", 3),
        ("four", 4),
        ("five", 5),
        ("six", 6),
        ("seven", 7),
        ("eight", 8),
        ("nine", 9),
        ("ten", 10),
        ("eleven", 11),
        ("twelve", 12),
        ("thirteen", 13),
        ("fourteen", 14),
        ("fifteen", 15),
        ("sixteen", 16),
        ("seventeen", 17),
        ("eighteen", 18),
        ("nineteen", 19),
        ("twenty", 20),
        ("thirty", 30),
        ("forty", 40),
        ("fifty", 50),
        ("sixty", 60),
        ("seventy", 70),
        ("eighty", 80),
        ("ninety", 90),
    ],
)
def test_every_declared_number_word_is_parsed(word, value):
    assert Decimal(value) in numbers(f"we ran {word} iterations")


def test_a_number_word_carrying_a_ligature_is_parsed():
    assert Decimal(5) in numbers("we ran ﬁve iterations")


def test_a_number_word_inside_a_longer_word_is_not_parsed():
    assert Decimal(1) not in numbers("the oneness of it")
    assert Decimal(10) not in numbers("a tendency")


def test_a_compound_number_word_yields_its_parts_not_its_sum():
    parsed = numbers("twenty-five samples")
    assert Decimal(20) in parsed and Decimal(5) in parsed
    assert Decimal(25) not in parsed


def test_a_percentage_yields_its_number():
    assert Decimal(5) in numbers("a 5% increase")


def test_a_unit_is_left_aside():
    assert Decimal(12) in numbers("12 km")


def test_a_thousands_separator_is_not_read_as_one_number():
    parsed = numbers("1,234 events")
    assert Decimal(1) in parsed and Decimal(234) in parsed
    assert Decimal(1234) not in parsed


def test_gluing_removes_a_standalone_number_the_sentence_states():
    """The measured ambiguity, asserted rather than described."""

    assert Decimal(2) in numbers("CO 2 uptake", profile=normalise.UNGLUED)
    assert Decimal(2) not in numbers("CO 2 uptake", profile=normalise.GLUED)


def test_the_default_number_reading_is_free_standing_and_unglued():
    assert numbers("a value of 991 metres") == normalise.numbers_in(
        "a value of 991 metres", profile=normalise.UNGLUED, attached=False
    )


def test_gluing_a_number_onto_the_word_before_it_loses_it_when_free_standing():
    """The second half of the same ambiguity, on the numeric side."""

    assert Decimal(991) in numbers("a value of 991 metres", profile=normalise.UNGLUED)
    assert Decimal(991) not in numbers("a value of 991 metres", profile=normalise.GLUED)


def test_the_attached_reading_keeps_a_digit_run_written_against_a_letter():
    assert Decimal(3) not in numbers("segment RC3 of the ridge")
    assert Decimal(3) in numbers("segment RC3 of the ridge", attached=True)


def test_the_attached_reading_does_not_depend_on_the_profile():
    for text in (
        "a value of 991 metres",
        "CO 2 uptake",
        "segment RC3",
        "1 . 5 ± 0 . 2",
    ):
        assert numbers(text, profile=normalise.GLUED, attached=True) == numbers(
            text, profile=normalise.UNGLUED, attached=True
        ), text


def test_the_attached_reading_never_starts_inside_a_digit_run():
    assert numbers("991 metres", attached=True) == frozenset({Decimal(991)})


def test_a_subscript_formula_matches_only_under_gluing():
    assert normalise.contains("CO2", "CO 2 uptake", profile=normalise.GLUED)
    assert not normalise.contains("CO2", "CO 2 uptake", profile=normalise.UNGLUED)


def test_containment_is_substring_containment_after_normalisation():
    assert normalise.contains("MgO", "the  MgO   content")
    assert normalise.contains("go con", "the MgO content")
    assert not normalise.contains("CaO", "the MgO content")


def test_an_empty_value_is_never_compared():
    assert normalise.contains("", "anything") is True
