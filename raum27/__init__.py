"""RAUM27 mathematical core: rational-space geometry and fractal attractors.

This package implements the parts of the RAUM27 notes that are ordinary,
checkable mathematics (a multiplicative group of positive rationals, a
3-adic/9-adic scale hierarchy, cube symmetry, iterated function systems,
and a rational Taylor approximation of sine).

It deliberately does NOT implement the predictive or metaphysical claims
found in the source notes (forecasting random draws, "resonance",
"consciousness", or any claim of physical signal transfer). Those claims
are either unfalsifiable or contradict basic probability theory, and are
out of scope for a benchmarkable codebase.
"""

from raum27.rational_space import involution, is_fixed_point
from raum27.scale_hierarchy import area_scale, digital_root, linear_scale, volume_scale
from raum27.cube_symmetry import (
    axis_cross_product,
    corner_directions,
    coupling_constant,
    cube_center,
    cube_volume,
    face_diagonal_midpoint,
    face_diagonal_squared,
    face_directions,
    pyramid_apex_to_corner_squared,
    pyramid_base_half_diagonal_squared,
    pyramid_height,
    pyramid_volume,
    space_diagonal_midpoint,
    space_diagonal_squared,
    space_diagonals,
    vector_equilibrium,
)
from raum27.ifs_attractor import AffineMap, IFS
from raum27.taylor import sin_taylor
from raum27.lotto_benchmark import (
    FingerprintKNNPredictor,
    RandomPredictor,
    backtest,
    expected_matches,
    match_probability,
    permutation_test,
)
from raum27.autocorrelation_control import (
    PersistencePredictor,
    permutation_test_continuous,
    simulate_ar1,
)
from raum27.q144 import (
    NUM_STATES,
    State,
    all_states,
    operator_period,
    orbit,
    phi,
)
from raum27.clockfree_scheduler import (
    Process,
    Schedule,
    ScheduleResult,
    schedule_round_robin,
    schedule_run_to_completion,
)
from raum27.rubik_state import (
    axis_is_solved,
    axis_pairs,
    face_is_uniform,
    is_solved,
)
from raum27.phase_sync import (
    beat_period,
    is_synchronized,
    phase_angle,
    phase_difference,
)
from raum27.octahedron import (
    vertices as octahedron_vertices,
    faces as octahedron_faces,
    edges as octahedron_edges,
    euler_characteristic as octahedron_euler_characteristic,
    dual_cube_corners as octahedron_dual_cube_corners,
)
from raum27.cube_projection import (
    incidence_matrix as cube_incidence_matrix,
    m_6to8,
    m_8to6,
    composed_kernel as cube_projection_kernel,
    apply as apply_matrix,
)

__all__ = [
    "involution",
    "is_fixed_point",
    "linear_scale",
    "area_scale",
    "volume_scale",
    "digital_root",
    "face_directions",
    "corner_directions",
    "vector_equilibrium",
    "coupling_constant",
    "axis_cross_product",
    "cube_center",
    "face_diagonal_midpoint",
    "face_diagonal_squared",
    "space_diagonal_midpoint",
    "space_diagonal_squared",
    "space_diagonals",
    "cube_volume",
    "pyramid_apex_to_corner_squared",
    "pyramid_base_half_diagonal_squared",
    "pyramid_height",
    "pyramid_volume",
    "AffineMap",
    "IFS",
    "sin_taylor",
    "FingerprintKNNPredictor",
    "RandomPredictor",
    "backtest",
    "expected_matches",
    "match_probability",
    "permutation_test",
    "PersistencePredictor",
    "permutation_test_continuous",
    "simulate_ar1",
    "NUM_STATES",
    "State",
    "all_states",
    "operator_period",
    "orbit",
    "phi",
    "Process",
    "Schedule",
    "ScheduleResult",
    "schedule_round_robin",
    "schedule_run_to_completion",
    "axis_is_solved",
    "axis_pairs",
    "face_is_uniform",
    "is_solved",
    "beat_period",
    "is_synchronized",
    "phase_angle",
    "phase_difference",
    "octahedron_vertices",
    "octahedron_faces",
    "octahedron_edges",
    "octahedron_euler_characteristic",
    "octahedron_dual_cube_corners",
    "cube_incidence_matrix",
    "m_6to8",
    "m_8to6",
    "cube_projection_kernel",
    "apply_matrix",
]
