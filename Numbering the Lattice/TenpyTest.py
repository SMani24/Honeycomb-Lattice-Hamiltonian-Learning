import matplotlib.pyplot as plt
from tenpy.models import lattice

plt.figure(figsize=(5, 6))
ax = plt.gca()
lat = lattice.Honeycomb(Lx=2, Ly=2, sites=None, bc_MPS='finite', bc=['periodic', 'periodic'])
lat.plot_coupling(ax)
lat.plot_order(ax, linestyle=':')
lat.plot_sites(ax)
lat.plot_basis(ax, origin=-0.5*(lat.basis[0] + lat.basis[1]))
ax.set_aspect('equal')
ax.set_xlim(-1)
ax.set_ylim(-1)
plt.show()