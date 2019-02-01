import geopandas as gpd
import osmnx as ox
import google_streetview.api
import urllib, os
import urllib.parse

def getStreetCentroid(row):
    obj = row['geometry']
    centroid = obj.centroid
    return centroid

def GetStreet(Add,SaveLoc,orientation):
    skeleton = 'https://maps.googleapis.com/maps/api/streetview?size=640x640&fov=120&pitch=-0.76&heading='+orientation+'&location='
    ThisUrl = skeleton + urllib.parse.quote(Add) + "&key="+"YOUR-API_KEY"  
    filePath = Add +'_facing='+orientation+'.jpg'
    urllib.request.urlretrieve(ThisUrl, os.path.join(SaveLoc,filePath))

G_dublin = ox.graph_from_place('Dublin, County Dublin, Leinster, Ireland', network_type='drive') #drivable roads
ox.save_graph_shapefile(G_dublin, filename='dublin_network') #save to disk
dublin = gpd.read_file('data/dublin_network/edges/edges.shp')

dublin['streetCentroid']  = dublin.apply(getStreetCentroid,axis=1)
orientation = ['0','125','250']



try:
	for index, row in dublin.iterrows(): 
	    points = (dublin.loc[index,'streetCentroid'])
	    pointList = list(points.coords)
	    locationCoordinate = str(pointList[0][1])+','+str(pointList[0][0])
	    for j in orientation:
	    	# change the value in SaveLoc to the folder you want to save the images
	        GetStreet(Add=locationCoordinate,SaveLoc = 'dublinImages',orientation = j)
	print('Finished downloading images for dublin')
except:
	print('error')
