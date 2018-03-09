<?xml version="1.0"?>

<!--
  .. Extract all APK URLs from F-Droid index file
  -->

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:output method="text"/>

<xsl:template match="/">
    <xsl:apply-templates select="fdroid/application/package/apkname"/>
</xsl:template>

<!--
<xsl:template match="application">
    <xsl:apply-templates select="package/apkname"/>
</xsl:template>
-->

<xsl:template match="apkname">
<xsl:text>https://f-droid.org/repo/</xsl:text>
<xsl:value-of select="text()"/>
<xsl:text>&#xa;</xsl:text>
</xsl:template>

</xsl:stylesheet> 
