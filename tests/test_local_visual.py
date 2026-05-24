"""Client-side mini-update between authoritative snapshots.

`World.update_local_visual` is what the networked client calls each
frame; it must move non-ship entities and let particle ttl decay
without otherwise touching simulation state.
"""

from core.entities import Bullet, Particle
from core.utils import Vec
from core.world import World


def test_advances_asteroid_position_by_velocity_times_dt():
    w = World(spawn_default_player=False)
    w.spawn_asteroid(Vec(100, 200), Vec(10, 20), "L")

    w.update_local_visual(0.5)

    a = w.asteroids[0]
    assert (a.pos.x, a.pos.y) == (105, 210)


def test_advances_bullet_position_by_velocity_times_dt():
    w = World(spawn_default_player=False)
    w.bullets.append(Bullet(1, Vec(0, 0), Vec(40, -20)))

    w.update_local_visual(0.25)

    b = w.bullets[0]
    assert (b.pos.x, b.pos.y) == (10, -5)


def test_decays_particle_ttl_and_advances_position():
    w = World(spawn_default_player=False)
    w.particles.append(Particle(Vec(50, 50), Vec(10, 0), ttl=1.0))

    w.update_local_visual(0.4)

    p = w.particles[0]
    assert p.ttl == 0.6
    assert (p.pos.x, p.pos.y) == (54, 50)


def test_purges_dead_particles():
    w = World(spawn_default_player=False)
    w.particles.append(Particle(Vec(0, 0), Vec(0, 0), ttl=0.1))
    w.particles.append(Particle(Vec(0, 0), Vec(0, 0), ttl=2.0))

    w.update_local_visual(0.5)

    assert len(w.particles) == 1
    assert w.particles[0].ttl == 1.5


def test_does_not_touch_match_state_or_scores():
    w = World(spawn_default_player=False, deathmatch=True)
    w.spawn_player(1)
    w.spawn_player(2)
    w.scores[1] = 100
    w.frags[2] = 3
    pre_state = w.match_state

    w.update_local_visual(1.0)

    assert w.match_state == pre_state
    assert w.scores == {1: 100, 2: 0}
    assert w.frags == {1: 0, 2: 3}
