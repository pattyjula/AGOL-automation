# -*- coding: utf-8 -*-
"""
        @Author: Patty Jula
        @Date created: 3/2022
        @Date updated: 6/21/2023
        @Description: This script takes a data wrangled shapefile, converts to
        a json and overwrites an existing feature layer on ArcGIS Online.
"""

import os
import sys

import arcgis
import arcpy
from arcgis.gis import GIS
import logging
# Set up logging
results =  "E:/batch/logging/arl.log"
logging.basicConfig(
    filename=results, format="%(asctime)s %(message)s", filemode="w"
    )
# Create a logging object
logger = logging.getLogger()
# Set to debug or info
logger.setLevel(logging.INFO)
logging.info(
    "^^^^^") 
logging.info(
    "^^^^^^^^^^^")  
logging.info(
    "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")  
logging.info(
    "~~~~~~~~~~~ARL Procedures~~~~~~~~~~~~")
logging.info(
    "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")  
logging.info(
    "^^^^^^^^^^^")  
logging.info(
    "^^^^^") 

arcpy.env.overwriteOutput = True

ws = sys.argv[1]
loc = ws
pth = os.chdir(loc)
output_feature_class = "ARL_data.shp"
localJSON = ws + "./arl_content.json"

# Helper function for logging
def logstuff(statement):
    logging.info("~~~~~~~~~~~~~~~~~")
    logging.info(statement)
    
    
    
try:
    if os.path.isfile(localJSON):
        os.remove(localJSON)

except FileNotFoundError:
    print("Wrong file or file path")


# Truncate the existing feature layer
def TruncateWebLayer(gis, target):

    try:
        lyr = arcgis.features.FeatureLayer(target, gis)
        lyr.manager.truncate()
        print("Successfully truncated layer: " + str(target))
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])

#try:

# LAPD log in, create a profile so you don't need to show un/pw
mygis = GIS("https://lapd.maps.arcgis.com/", profile="python_playground_prof")
#mygis = GIS("https://lapd.maps.arcgis.com/", client_id='3uVopa3aWCKGsDwf')


# publishedWebLayer is the URL of a single feature layer within a collection in
# an AGOL portal
#publishedWebLayer = mygis.content.get("28c41e431bee478793c94dcb865cd40e")
publishedWebLayer = "https://services6.arcgis.com/Q18o8KwHjFGbEc4j/arcgis/rest/services/ARL_data/FeatureServer/0"

# a feature class on the local system with the same schema as the
# portal layer
updateFeatures = os.path.join("E:/batch/arl/content/" + output_feature_class)

# remove all features from the already published feature layer

feature_layer_item = mygis.content.search("arl whole file")[0]
flayers = feature_layer_item.layers
logging.info(arcpy.GetMessages(0))
flayer = flayers[0]

flayer.delete_features(where="area > 0 OR area =0")

# reference the empty layer as FeatureLayer object from the ArcGIS Python API
fl = arcgis.features.FeatureLayer(publishedWebLayer, mygis)

# create a JSON object from the local features
jSON = arcpy.FeaturesToJSON_conversion(updateFeatures, localJSON)


    
# create a FeatureSet object from the JSON

fs = arcgis.features.FeatureSet.from_json(open(localJSON).read())
logstuff("Creating a featureset from the JSON")

# add/append the local features to the hosted feature layer

fl.edit_features(adds=fs)
logstuff("Appending latest data to the hosted feature layer")
logging.info(arcpy.GetMessages(0))


