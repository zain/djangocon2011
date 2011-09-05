{% extends "gis/admin/openlayers.js" %}
{% block base_layer %}
new OpenLayers.Layer.Google("Google Streets", {'sphericalMercator': true});
{% endblock %}
