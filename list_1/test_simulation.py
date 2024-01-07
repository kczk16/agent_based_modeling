import numpy as np
from unittest.mock import Mock, patch, call
from pytest import mark
from abmocn.list_1.simulation import _generate_start_state_of_trees, simulate, simulate_monte_carlo


def test_simulate():
    lattice_mock = Mock()
    lattice_mock.get_opposite_edge = Mock(return_value=['opposite cords'])
    lattice_mock.change_state = Mock(side_effect=[['burnt tree'], ['burnt tree'], []])
    lattice_mock.start_fire = Mock()
    expected = True
    lattice_mock.check_if_burnt = Mock(return_value=expected)
    start_mock = Mock(return_value=lattice_mock)
    with patch("abmocn.list_1.simulation._generate_start_state_of_trees", start_mock):
        result = simulate(size=20, p=0.5)

    start_mock.assert_called_once_with(20, 0.5, False)
    lattice_mock.get_opposite_edge.assert_called_once_with(edge='left')
    lattice_mock.start_fire.assert_called_once_with(edge='left')
    lattice_mock.change_state.assert_has_calls([call(), call(), call()])
    assert result == expected


def test_simulate_with_gif_and_clusters():
    lattice_mock = Mock()
    lattice_mock.get_opposite_edge = Mock(return_value=['opposite cords'])
    lattice_mock.change_state = Mock(side_effect=[['burnt tree'], ['burnt tree'], []])
    lattice_mock.start_fire = Mock()
    tree_instance = Mock()
    tree_instance.cluster_type = Mock()
    lattice_mock.hoshen_kopelman = Mock(return_value=[tree_instance])
    expected = True
    lattice_mock.check_if_burnt = Mock(return_value=expected)
    start_mock = Mock(return_value=lattice_mock)
    del_mock, plot_mock = Mock(), Mock()
    with patch("abmocn.list_1.simulation._generate_start_state_of_trees", start_mock), \
         patch("abmocn.list_1.simulation._del_remained_pngs", del_mock), \
         patch("abmocn.list_1.simulation.plot_fire", plot_mock):
        result, cluster = simulate(size=20, p=0.5, gif=True, clusters=True)

    start_mock.assert_called_once_with(20, 0.5, True)
    lattice_mock.get_opposite_edge.assert_called_once_with(edge='left')
    lattice_mock.start_fire.assert_called_once_with(edge='left')
    lattice_mock.change_state.assert_has_calls([call(), call(), call()])
    del_mock.assert_called_once()
    plot_mock.assert_has_calls([call(lattice_mock.grid, '1'), call(lattice_mock.grid, '2'),
                                call(lattice_mock.grid, '3')])
    lattice_mock.hoshen_kopelman.assert_called_once()

    assert result == expected


@mark.parametrize("p, N", [([0.5], 2), ([0.25, 0.75], 2)])
def test_simulate_monte_carlo(p, N):
    simulate_mock = Mock(return_value=2)
    p_range = Mock(return_value=p)
    with patch('abmocn.list_1.simulation.simulate', simulate_mock), \
         patch('abmocn.list_1.simulation.np.linspace', p_range):
        simulate_monte_carlo(N=N)

    calls = [call(size=20, p=value, edge='left') for value in p]
    simulate_mock.assert_has_calls(calls)


def test__generate_start_state_of_trees(size=5):
    lattice_instance_mock = Mock()
    lattice_instance_mock._configure = Mock()
    lattice_instance_mock.grid = np.zeros(shape=[size, size])
    lattice_mock = Mock(return_value=lattice_instance_mock)
    with patch("abmocn.list_1.simulation.Lattice", lattice_mock):
        _generate_start_state_of_trees(size, p=0.5)
    lattice_instance_mock._configure.assert_called_once_with(size=size)


def test__generate_start_state_of_trees_with_gif(size=5):
    lattice_instance_mock = Mock()
    lattice_instance_mock._configure = Mock()
    lattice_instance_mock.grid = np.zeros(shape=[size, size])
    lattice_mock = Mock(return_value=lattice_instance_mock)
    gif_mock = Mock()
    with patch("abmocn.list_1.simulation.Lattice", lattice_mock), \
         patch("abmocn.list_1.simulation.plot_fire", gif_mock):
        _generate_start_state_of_trees(size, p=0.5, gif=True)
    lattice_instance_mock._configure.assert_called_once_with(size=size)
    gif_mock.assert_called_once_with(lattice_instance_mock.grid, '0')
