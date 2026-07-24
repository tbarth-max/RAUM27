import pytest

from raum27.scale_hierarchy import area_scale, digital_root, linear_scale, volume_scale


@pytest.mark.parametrize("k", range(6))
def test_area_is_linear_squared(k):
    assert area_scale(k) == linear_scale(k) ** 2


@pytest.mark.parametrize("k", range(6))
def test_volume_is_linear_cubed(k):
    assert volume_scale(k) == linear_scale(k) ** 3


@pytest.mark.parametrize("k", range(1, 8))
def test_digital_root_of_power_of_nine_is_nine(k):
    assert digital_root(area_scale(k)) == 9


def test_digital_root_known_values():
    assert digital_root(9) == 9
    assert digital_root(18) == 9
    assert digital_root(123) == 6
    assert digital_root(1) == 1


def test_digital_root_rejects_non_positive():
    with pytest.raises(ValueError):
        digital_root(0)
