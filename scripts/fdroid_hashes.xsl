<?xml version="1.0"?>

<!--
  .. Extract hashes in sha256sum compatible format
  -->

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:output method="text"/>

<xsl:template match="/">
    <xsl:apply-templates select="fdroid/application/package"/>
</xsl:template>

<xsl:template match="package">
<xsl:value-of select="hash"/>
<xsl:text>  </xsl:text>
<xsl:value-of select="apkname"/>
<xsl:text>&#xa;</xsl:text>
</xsl:template>

</xsl:stylesheet> 
