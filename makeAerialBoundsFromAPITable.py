# Parse a delimited text file of volcano data and create a shapefile

import ogr as ogr
import osr as osr

# use a dictionary reader so we can access by field name
#reader = csv.DictReader(open("g:/temp/topoReportBounds/bounds.txt","rb"),    delimiter='\t',    quoting=csv.QUOTE_NONE)

infile = open('E:/workspace/AerialPhotosIndex/20150130/export20150130.txt','r')

# set up the shapefile driver
driver = ogr.GetDriverByName("ESRI Shapefile")

# create the data source
data_source = driver.CreateDataSource('e:/workspace/aerialPhotosIndex/20150130/coverage.shp')

# create the spatial reference, WGS84
srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)

# create the layer
layer = data_source.CreateLayer("bounds", srs, ogr.wkbPolygon)

# Add the fields we're interested in
#NB - field names can only be 10 characters wide for shape files

field_id = ogr.FieldDefn("IndexID", ogr.OFTInteger)
layer.CreateField(field_id)

field_name = ogr.FieldDefn("Photo_ID", ogr.OFTString)
field_name.SetWidth(50)
layer.CreateField(field_name)

fieldIndex = ogr.FieldDefn("ImageIndex",ogr.OFTString)
fieldIndex.SetWidth(5)
layer.CreateField(fieldIndex)

field_Year = ogr.FieldDefn("ImageDate", ogr.OFTDateTime)
layer.CreateField(field_Year)

field_scale = ogr.FieldDefn("ImageScale",ogr.OFTInteger)
layer.CreateField(field_scale)

fieldPrintScale = ogr.FieldDefn("PrintScale",ogr.OFTInteger)
layer.CreateField(fieldPrintScale)

fieldSource = ogr.FieldDefn("Source",ogr.OFTString)
fieldSource.SetWidth(75)
layer.CreateField(fieldSource)

fieldTimeStamp = ogr.FieldDefn("InputStamp",ogr.OFTDateTime)
layer.CreateField(fieldTimeStamp)

fieldDPI = ogr.FieldDefn("ImageDPI",ogr.OFTInteger)
layer.CreateField(fieldDPI)

fieldFIPS = ogr.FieldDefn("FIPS",ogr.OFTString)
fieldFIPS.SetWidth(5)
layer.CreateField(fieldFIPS)

fieldARTID = ogr.FieldDefn("ARTID",ogr.OFTInteger)
layer.CreateField(fieldARTID)

fieldCenterLat = ogr.FieldDefn("CenterLat",ogr.OFTReal)
layer.CreateField(fieldCenterLat)

fieldCenterLon = ogr.FieldDefn("CenterLon",ogr.OFTReal)
layer.CreateField(fieldCenterLon)

fieldMinLat = ogr.FieldDefn("MinLat",ogr.OFTReal)
layer.CreateField(fieldMinLat)

fieldMinLon = ogr.FieldDefn("MinLon",ogr.OFTReal)
layer.CreateField(fieldMinLon)

fieldMaxLat = ogr.FieldDefn("MaxLat",ogr.OFTReal)
layer.CreateField(fieldMaxLat)

fieldMaxLon = ogr.FieldDefn("MaxLon",ogr.OFTReal)
layer.CreateField(fieldMaxLon)

fieldSourceAbbrev = ogr.FieldDefn("SourceAbbrev",ogr.OFTString)
fieldSourceAbbrev.SetWidth(10)
layer.CreateField(fieldSourceAbbrev)

fieldSourceDescrip = ogr.FieldDefn("SourceDescrip",ogr.OFTString)
fieldSourceDescrip.SetWidth(75)
layer.CreateField(fieldSourceDescrip)

fieldFullPath = ogr.FieldDefn("FullPath",ogr.OFTString)
fieldFullPath.SetWidth(500)
layer.CreateField(fieldFullPath)


# Process the text file and add the attributes and features to the shapefile
for myline in infile:
  # create the feature
  #split the line:
  #topodataid,state,county,quad_name,years,minlat,minlon,maxlat,maxlon = myline.split('\t')
  indexid,photo_id,imageindex,imagedate,imagescale,imageprintscale,imagesource,inputtimestamp,imagedpi,fips,artid,centerlat,centerlon,minlat,minlon,maxlat,maxlon,sourceabbrev,sourcedesc,fullpath = myline.split(',')
  
  print indexid
  
  feature = ogr.Feature(layer.GetLayerDefn())
  # Set the attributes using the values from the delimited text file
  feature.SetField("IndexID",indexid)
  feature.SetField("Photo_ID",photo_id)
  feature.SetField("ImageIndex",imageindex)
  feature.SetField("ImageDate",imagedate)
  feature.SetField("ImageScale",imagescale)
  feature.SetField("PrintScale",imageprintscale)
  feature.SetField("Source",imagesource)
  feature.SetField("InputStamp",inputtimestamp)
  feature.SetField("ImageDPI",imagedpi)
  feature.SetField("FIPS",fips)
  feature.SetField("ARTID",artid)
  feature.SetField("CenterLat",centerlat)
  feature.SetField("CenterLon",centerlon)
  feature.SetField("MinLat",minlat)
  feature.SetField("MinLon",minlon)
  feature.SetField("MaxLat",maxlat)
  feature.SetField("MaxLon",maxlon)
  feature.SetField("SourceAbbrev",sourceabbrev)
  feature.SetField("SourceDescrip",sourcedesc)
  feature.SetField("FullPath",fullpath)
  
  # create the WKT for the feature using Python string formatting
  #wkt = "POINT(%f %f)" %  (float(row['Longitude']) , float(row['Latitude']))
  wkt = "POLYGON((%f %f, %f %f,%f %f, %f %f,%f %f))" % (float(minlon), float(minlat), float(minlon), float(maxlat), float(maxlon), float(maxlat), float(maxlon), float(minlat), float(minlon), float(minlat))

  # Create the point from the Well Known Txt
  poly = ogr.CreateGeometryFromWkt(wkt)

  # Set the feature geometry using the point
  feature.SetGeometry(poly)
  # Create the feature in the layer (shapefile)
  layer.CreateFeature(feature)
  # Destroy the feature to free resources
  feature.Destroy()

# Destroy the data source to free resources
data_source.Destroy()

print 'done'