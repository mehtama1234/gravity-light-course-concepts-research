# Gravity & geometry — verified measured results (numpy, SI units)

Every number below is computed by a short program we ran. Script: scripts/experiments/gr_run.py.
Cite numbers verbatim; do NOT invent new ones.

## EXP1 — parallel transport around a loop (concepts: parallel-transport-loop-test, riemann-curvature-commutator)
- Carry an arrow around a triangle on a globe — a quarter-turn along the equator, up to the North Pole,
  back down — never rotating it by hand. It returns pointing **90 degrees** rotated from where it started.
- The rotation equals the enclosed area (here 1/8 of the sphere). On a FLAT sheet the arrow always comes
  back unchanged (0 rotation).
- Insight: the failure of a transported arrow to come back the same way — after going around a loop — is
  a direct, from-the-inside measurement of curvature. (And it is why the order of two moves matters on a
  curved space: curvature is exactly that non-commuting.)

## EXP2 — geodesics: the straightest path is a great circle (concepts: geodesics-free-motion, metric-measurement)
- New York to London by the geodesic (great-circle) route is **5567 km**, arcing north over Canada — not
  the straight line you'd draw on a flat map.
- Insight: a geodesic is "locally straight" — at every step you head straight ahead — yet the path curves
  because the surface does. Distances and angles are set intrinsically by the metric, measured from within.
  Free-falling bodies and light rays follow geodesics through spacetime; that is what "gravity" is.

## EXP3 — light bending / gravitational lensing (concept: gravitational-lensing-focusing)
- The Sun's Schwarzschild radius is **2.95 km**. A light ray grazing the Sun's edge bends by:
  general relativity's 4GM/(c^2 R) = **1.75 arcseconds**; the old Newtonian "light as a falling particle"
  gives 2GM/(c^2 R) = **0.88 arcseconds** — exactly half.
- Insight: mass bends the paths of light, not just of matter, because it curves space AND time. Eddington
  measured ~1.75 arcseconds during the 1919 solar eclipse — twice the Newtonian value — the observation
  that made Einstein famous overnight and confirmed general relativity.

## EXP4 — time runs at different rates (concept: proper-time-clock-reading)
- A GPS satellite clock versus a ground clock, per day: being higher in gravity speeds it up by
  **+45.7 microseconds/day**; moving fast in orbit slows it by **-7.2 microseconds/day**; net
  **+39 microseconds/day**.
- Uncorrected, this would push GPS positions off by about **12 km per day**.
- Insight: time itself ticks at a rate that depends on where you are (gravity) and how you move (speed).
  This is not exotic — your phone's navigation would fail within minutes if it ignored relativity.

## EXP5 — curvature is measurable from inside (concept: manifolds-local-flatness)
- Draw a triangle on a globe and add its three angles: a triangle covering 5% of an octant sums to
  **184.5 degrees** (4.5 excess); 25% sums to **202.5 degrees**; a full octant sums to **270 degrees**
  (90 excess).
- Insight: on a flat sheet a triangle's angles always sum to 180. The excess over 180 equals the enclosed
  area times the curvature — so a flatlander who cannot step "outside" still measures curvature purely from
  geometry. And the excess shrinks with the square of the triangle's size: small enough, any curved space
  looks flat (a manifold is "locally flat").

## EXP6 — black holes and horizons (concepts: black-holes-horizons, event-horizon-causal-boundary)
- The radius to which a mass must be crushed for light to no longer escape (the Schwarzschild radius):
  the Sun would become a black hole at **2.95 km**, the Earth at about **8.9 mm**.
- Insight: the event horizon is not a wall or a surface you hit — it is a one-way causal boundary. Inside
  it, the geometry is so warped that every possible future path leads further inward; there is simply no
  "outward" direction left to travel. Nothing holds you in; the shape of spacetime does.

## EXP7 — geodesic deviation reveals curvature / tidal gravity (concept: curvature-geodesic-deviation)
- Two travellers start on the equator 100 km apart and both walk due north (straight ahead, never turning
  toward each other). Their separation: **100.0 km at the equator, 86.6 km at 30 degrees, 50.0 km at 60
  degrees, 1.7 km at 89 degrees** — they collide at the pole.
- Insight: initially-parallel straight paths converging on their own IS curvature. In spacetime this same
  effect is TIDAL gravity — why the Moon raises two ocean bulges and why an astronaut falling toward a
  black hole is stretched: nearby free-fall paths are pulled together (or apart) by curved spacetime.

## EXP8 — cosmic expansion and redshift (concepts: hubble-rate-as-change-of-scale, redshift-as-stretched-light)
- Using a Hubble rate of 70 km/s per megaparsec: a galaxy 10 Mpc away recedes at **700 km/s** (redshift
  z ~ 0.002); at 100 Mpc, **7000 km/s** (z ~ 0.023); at 1000 Mpc, **70,000 km/s** (z ~ 0.233).
- Insight: recession speed grows in proportion to distance (Hubble's law), and every galaxy sees the same
  thing — not because we are at the center, but because space ITSELF is stretching. Light traveling through
  that stretching space gets its wavelength lengthened (redshifted) in flight, which is how we read the
  expansion off distant galaxies.
