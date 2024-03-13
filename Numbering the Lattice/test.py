import NumerateHoneycomb
hc = NumerateHoneycomb.NumerateHoneycomb(4)

vertexToLink = hc.vertexToLink
linkToVertex = hc.linkToVertex
plaquetteToLink = hc.plaquetteToLink
plaquetteToVertex = hc.plaquetteToVertex
vertexToPlaquette = hc.vertexToPlaquette
linkToPlaquette = hc.linkToPlaquette

for key, item in vertexToLink.items():
    print(key, item)