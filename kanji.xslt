<xsl:transform xmlns="http://www.w3.org/2000/svg" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

<xsl:variable name="key_small" select="/row/value[@colname='grade']"/>

<xsl:template match="row">
	<svg width="64" height="68">
		<rect x="0" y="0" width="100%" height="100%" fill='#fff'/>
		<text x="0" y="0" font-size="64" dominant-baseline="text-before-edge" font-family="Meiryo, Noto Sans CJK, MS Gothic, sans">
			<xsl:apply-templates select="value[@colname='grade']"/>
			<xsl:apply-templates select="value[@colname='id']"/>
		</text>
	</svg>
</xsl:template>

<xsl:template match="row[@size = 'small']">
	<svg width="32" height="32">
		<rect x="0" y="0" width="100%" height="100%" fill='#fff'/>
		<rect x="8" y="8" width="16" height="16">
			<xsl:apply-templates select="value[@colname='grade']"/>
		</rect>
	</svg>
</xsl:template>

<xsl:template match="row/value[@colname='grade']">
	<xsl:variable name="n" select="number(.)"/>
	<xsl:attribute name="fill">
		<xsl:choose>
			<xsl:when test="$n = 10">#005</xsl:when>
			<xsl:when test="$n = 9">#006</xsl:when>
			<xsl:when test="$n = 8">#500</xsl:when>
			<xsl:when test="$n = 6">#800</xsl:when>
			<xsl:when test="$n = 5">#900</xsl:when>
			<xsl:when test="$n = 4">#A00</xsl:when>
			<xsl:when test="$n = 3">#B00</xsl:when>
			<xsl:when test="$n = 2">#C00</xsl:when>
			<xsl:when test="$n = 1">#D00</xsl:when>
			<xsl:otherwise>#000</xsl:otherwise>
		</xsl:choose>
	</xsl:attribute>
</xsl:template>

</xsl:transform>
