"""Observer table: predicted transits of TIC 308184057 for the next ~6 months and whether each is observable
(Sun < -12 deg and target altitude > 30 deg through ingress-to-egress) from southern observatories.
Usage: python observability_308184057.py [P T0 sigP sigT0]  (defaults: provisional ephemeris)"""
import sys, numpy as np, pandas as pd, datetime as dt
from astropy.utils import iers
iers.conf.auto_download = False; iers.conf.auto_max_age = None
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, get_sun
import astropy.units as u
P, T0, sP, sT = (float(a) for a in sys.argv[1:5]) if len(sys.argv) > 4 else (6.119015, 1356.2511, 2e-5, 0.005)
T14 = float(sys.argv[5]) / 24 if len(sys.argv) > 5 else 2.0 / 24
star = SkyCoord(130.410329720449 * u.deg, -68.9673754253933 * u.deg)
sites = {"CTIO (Chile)": (-30.1690, -70.8063, 2207), "La Silla (Chile)": (-29.2563, -70.7380, 2400),
         "Las Campanas (Chile)": (-29.0146, -70.6926, 2380), "SAAO Sutherland (S. Africa)": (-32.3794, 20.8107, 1798),
         "Siding Spring (Australia)": (-31.2733, 149.0643, 1165)}
locs = {k: EarthLocation(lat=a * u.deg, lon=b * u.deg, height=h * u.m) for k, (a, b, h) in sites.items()}
now = Time(dt.datetime.utcnow()); btjd_now = now.jd - 2457000
n0 = int(np.ceil((btjd_now - T0) / P)); rows = []
for n in range(n0, n0 + int(182 / P) + 1):
    tc = T0 + n * P; sig = np.hypot(sT, n * sP) * 24
    tmid = Time(tc + 2457000, format="jd")
    times = tmid + np.linspace(-T14 / 2 - 0.02, T14 / 2 + 0.02, 7) * u.day
    ok_sites = []
    for name, loc in locs.items():
        fr = AltAz(obstime=times, location=loc)
        alt = star.transform_to(fr).alt.deg; sun = get_sun(times).transform_to(fr).alt.deg
        if np.all(alt > 30) and np.all(sun < -12): ok_sites.append(f"{name.split(' (')[0]} (alt {alt.min():.0f}-{alt.max():.0f})")
    ist = (tmid.datetime + dt.timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d %H:%M")
    rows.append(dict(epoch=n, mid_UTC=tmid.datetime.strftime("%Y-%m-%d %H:%M"), mid_IST=ist, BTJD=round(tc, 4),
                     sigma_min=round(sig * 60, 1), ingress_UTC=(tmid - T14 / 2 * u.day).datetime.strftime("%H:%M"),
                     egress_UTC=(tmid + T14 / 2 * u.day).datetime.strftime("%H:%M"), observable_from="; ".join(ok_sites) or "-"))
df = pd.DataFrame(rows); df.to_csv("results_summary/TIC308184057_ephemeris_observability.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 120)
print(df.to_string(index=False)); print(f"\n{(df.observable_from != '-').sum()} of {len(df)} transits fully observable from at least one site")
