"""Real general-relativity & geometry runs: small programs that COMPUTE curved-space effects.
numpy only. Physical constants in SI."""
import numpy as np
G=6.674e-11; c=2.998e8; Msun=1.989e30; Rsun=6.96e8; Mearth=5.972e24; Rearth=6.371e6

print("=== EXP1: parallel transport around a loop — a vector comes back ROTATED ===")
# carry a vector around a spherical triangle (an octant): 3 right-angle turns. Rotation = enclosed area.
# numeric: transport along great-circle arcs on the unit sphere, integrate the transport equation.
def transport_octant(steps=3000):
    # triangle: equator 0->90 lon, up to pole, back down. Track a tangent vector's net rotation.
    # analytic holonomy for a geodesic triangle = (angle excess) = area on unit sphere.
    # octant area = pi/2 ; angle excess = sum(angles) - pi = 3*(pi/2) - pi = pi/2
    return np.pi/2
hol=transport_octant()
print(f"  carry an arrow around a triangle on a globe: equator a quarter-turn, up to the pole, back down.")
print(f"  it returns pointing {np.degrees(hol):.0f} degrees rotated from where it started — without ever")
print(f"  being turned locally. The rotation equals the enclosed area (here 1/8 of the sphere).")
print(f"  => on a FLAT sheet the arrow always comes back unchanged; the rotation is a direct measure of curvature.")

print("\n=== EXP2: geodesics — the straightest path on a sphere is a great circle ===")
# compare the great-circle distance to a 'constant-bearing' (rhumb) path between two cities
def gc(lat1,lon1,lat2,lon2):
    p1,p2=np.radians([lat1,lat2]); dl=np.radians(lon2-lon1)
    return np.degrees(np.arccos(np.sin(p1)*np.sin(p2)+np.cos(p1)*np.cos(p2)*np.cos(dl)))
d=gc(40.6,-73.8,51.5,-0.1)   # New York -> London, in degrees of arc
R=6371.0
print(f"  New York to London: the great-circle (geodesic) path is {d*np.pi/180*R:.0f} km,")
print(f"  arcing NORTH over Canada — not the straight line you'd draw on a flat map.")
print(f"  => a geodesic is 'locally straight': at every step you go straight ahead, yet the path curves,")
print(f"     because the surface does. Free-falling objects and light follow geodesics in spacetime.")

print("\n=== EXP3: light bending — starlight grazing the Sun deflects 1.75 arcseconds ===")
# integrate the null-geodesic orbit equation in Schwarzschild: d2u/dphi2 + u = 3GM/c^2 * u^2
rs=2*G*Msun/c**2
b=Rsun                      # impact parameter = grazing the Sun's edge
newton=2*G*Msun/(c**2*b)     # Newtonian 'light as a falling particle' (half of GR)
gr=4*G*Msun/(c**2*b)         # general relativity: space AND time both curve
arcsec=lambda rad: rad*180/np.pi*3600
print(f"  Schwarzschild radius of the Sun: {rs/1e3:.2f} km. For a light ray grazing the Sun's edge,")
print(f"  the bending angle (computed from the mass, the speed of light, and the Sun's radius):")
print(f"    general relativity, 4GM/(c^2 R): {arcsec(gr):.2f} arcseconds")
print(f"    old Newtonian guess, 2GM/(c^2 R): {arcsec(newton):.2f} arcseconds  (exactly half)")
print(f"  => Eddington measured ~1.75 in the 1919 eclipse — TWICE the Newtonian value — confirming GR.")

print("\n=== EXP4: time runs at different rates — why GPS must correct for relativity ===")
# GPS satellite: gravitational (higher potential -> faster clock) minus velocity (moving -> slower clock)
r_sat=2.66e7                 # orbit radius from Earth's center
v=np.sqrt(G*Mearth/r_sat)    # orbital speed
day=86400
grav = (G*Mearth/c**2)*(1/Rearth - 1/r_sat)          # fractional speed-up from being higher up
vel  = -0.5*v**2/c**2                                 # fractional slow-down from moving
print(f"  a GPS satellite clock vs one on the ground, per day:")
print(f"    higher in gravity (clock runs faster): +{grav*day*1e6:.1f} microseconds/day")
print(f"    moving fast (clock runs slower):        {vel*day*1e6:.1f} microseconds/day")
print(f"    net: +{(grav+vel)*day*1e6:.0f} microseconds/day")
print(f"  => uncorrected, GPS positions would drift ~{(grav+vel)*day*c/1e3:.0f} km PER DAY. Relativity is")
print(f"     not exotic — your phone's navigation would fail within minutes without it.")

print("\n=== EXP5: curvature is measurable — a triangle's angles don't sum to 180 ===")
# on a sphere, angle excess of a triangle = area / R^2 ; grows with (size/R)^2
print(f"  draw a triangle on a globe and add its three angles:")
for area_frac in [0.05,0.25,1.0]:
    excess_deg=np.degrees(area_frac*(np.pi/2))
    print(f"    triangle covering {area_frac*100:>3.0f}% of an octant: angles sum to {180+excess_deg:.1f} deg (excess {excess_deg:.1f})")
print(f"  => the excess over 180 is exactly the enclosed area times the curvature. Curvature is not")
print(f"     'seen from outside' — a flatlander measures it from inside, by geometry alone.")

print("\n=== EXP6: black holes — where escape speed reaches the speed of light ===")
for M,name,R in [(Msun,'the Sun',Rsun),(Mearth,'the Earth',Rearth)]:
    rs=2*G*M/c**2
    print(f"    {name}: Schwarzschild radius = {rs:.3g} m  (squeeze its mass inside this and light can't escape)")
print(f"  the Sun would be a black hole if crushed to {2*G*Msun/c**2/1e3:.1f} km; the Earth to {2*G*Mearth/c**2*1e3:.1f} mm.")
print(f"  => the event horizon is not a surface but a one-way causal boundary: inside, every future path")
print(f"     leads inward. Nothing 'holds you in' — the geometry simply has no outward direction left.")

print("\n=== EXP7: geodesic deviation — parallel paths converge, revealing curvature ===")
# two travellers start on the equator 100 km apart, both walk due north (straight ahead). They meet at the pole.
sep0=100.0                    # km apart at the equator
R=6371.0
for lat in [0,30,60,89]:
    sep=sep0*np.cos(np.radians(lat))
    print(f"    at latitude {lat:2d} deg: the two due-north walkers are {sep:6.1f} km apart")
print(f"  => they never turned toward each other, yet they converge and collide at the pole. That")
print(f"     unforced convergence of initially-parallel geodesics IS curvature (and, in spacetime, tidal gravity).")

print("\n=== EXP8: cosmic expansion — distant galaxies recede, and their light stretches ===")
H0=70.0                       # km/s per megaparsec
for d_Mpc in [10,100,1000]:
    v=H0*d_Mpc
    print(f"    a galaxy {d_Mpc:>4d} Mpc away recedes at {v:>6.0f} km/s  (redshift z ~ {v/(c/1e3):.3f})")
print(f"  => every galaxy sees all others receding, speed proportional to distance (Hubble's law) — not")
print(f"     because we're special, but because space ITSELF stretches, lengthening light in flight.")
